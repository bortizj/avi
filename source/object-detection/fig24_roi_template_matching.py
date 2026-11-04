"""Figure 24 of 05_object_detection.md (roi-template-matching.png).

Template matching on a simulated scene: normalized cross-correlation (NCC) versus
shape-based matching with a gradient-direction score, over all rotations, with uneven light and occlusion.

Run:  python fig24_roi_template_matching.py
Output: roi-template-matching.png in the current folder; the numbers quoted in the text are printed to the console.
"""
import numpy as np, cv2, time
from style import *
rng = np.random.default_rng(3)
SS = 4
def part_mask(shape, cx, cy, ang):
    """bracket: 110 x 60 plate with a notch and two holes, drawn with 4x supersampling"""
    H, W = shape
    m = np.zeros((H * SS, W * SS), np.uint8)
    poly = np.array([[-55, -30], [55, -30], [55, 30], [5, 30], [5, 5], [-20, 5], [-20, 30], [-55, 30]], float)
    th = np.deg2rad(ang); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    p = (poly @ R.T + [cx, cy]) * SS
    cv2.fillPoly(m, [np.round(p).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    for hx, hy, r in [(-38, -12, 8), (35, 0, 11)]:
        c = (np.array([hx, hy]) @ R.T + [cx, cy]) * SS
        cv2.circle(m, tuple(np.round(c).astype(int)), r * SS, 0, -1, lineType=cv2.LINE_AA)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA) / 255.0

H, W = 400, 640
yy, xx = np.mgrid[0:H, 0:W]
def render(objs, occl=True):
    bg = 70 + 8 * np.sin(xx / 23.0) * np.cos(yy / 31.0)
    img = bg.copy()
    for cx, cy, a, gain in objs:
        m = part_mask((H, W), cx, cy, a)
        shade = gain * (1 - 0.35 * (xx - cx + 60) / 120.0) if gain < 1 else 1.0
        img = img * (1 - m) + m * 185 * shade
    return img
objs = [(110, 110, 0, 1.0), (300, 100, 25, 1.0), (500, 120, 140, 1.0), (150, 290, 70, 0.6), (380, 300, 200, 1.0)]
img = render(objs)
# clutter: screws (bright circles), a wire
for (cx, cy) in [(560, 300), (600, 250), (250, 200)]:
    cv2.circle(img, (cx, cy), 12, 175, -1, lineType=cv2.LINE_AA)
# occluder over 30% of object 5
cv2.rectangle(img, (390, 250), (425, 360), 40, -1)
img = cv2.GaussianBlur(img, (0, 0), 0.8) + rng.normal(0, 5, img.shape)
img = np.clip(img, 0, 255).astype(np.uint8)
occ_frac = (part_mask((H, W), 380, 300, 200) * ((xx >= 390) & (xx <= 425) & (yy >= 250) & (yy <= 360))).sum() / part_mask((H, W), 380, 300, 200).sum()
print("occluded fraction", occ_frac)

# template from a clean 0 deg rendering
T = 141
tm = part_mask((T, T), T // 2, T // 2, 0)
timg = (70 * (1 - tm) + 185 * tm).astype(np.float32)
tmask_full = (np.ones((T, T)) * 255).astype(np.uint8)

def ncc_maps(scene, angles):
    out = []
    for a in angles:
        Rm = cv2.getRotationMatrix2D((T // 2, T // 2), -a, 1.0)
        rt = cv2.warpAffine(timg, Rm, (T, T), flags=cv2.INTER_LINEAR, borderValue=0)
        rm = cv2.warpAffine(np.ones((T, T), np.float32), Rm, (T, T), flags=cv2.INTER_NEAREST)
        # restrict to a disk so all angles use the same support
        disk = ((np.mgrid[0:T, 0:T][0] - T // 2) ** 2 + (np.mgrid[0:T, 0:T][1] - T // 2) ** 2 <= (T // 2) ** 2).astype(np.float32)
        r = cv2.matchTemplate(scene.astype(np.float32), rt, cv2.TM_CCOEFF_NORMED, mask=(rm * disk))
        r = np.nan_to_num(r, nan=-1, posinf=-1, neginf=-1)
        full = -np.ones(scene.shape, np.float32)
        full[T // 2:T // 2 + r.shape[0], T // 2:T // 2 + r.shape[1]] = r
        out.append(full)
    return np.array(out)

# shape-based model: edge points + gradient directions of the template
gx = cv2.Sobel(timg, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(timg, cv2.CV_32F, 0, 1, ksize=3)
e = cv2.Canny(timg.astype(np.uint8), 50, 120) > 0
py, px = np.where(e)
mag = np.hypot(gx[py, px], gy[py, px]) + 1e-9
mdx, mdy = gx[py, px] / mag, gy[py, px] / mag
ox, oy = px - T // 2, py - T // 2
n_model = len(px)
print("model points", n_model)

def grad_unit(scene, thr=10):
    s = cv2.GaussianBlur(scene.astype(np.float32), (0, 0), 1.0)
    gx = cv2.Sobel(s, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(s, cv2.CV_32F, 0, 1, ksize=3)
    m = np.hypot(gx, gy)
    ok = m > thr
    ux = np.where(ok, gx / (m + 1e-9), 0); uy = np.where(ok, gy / (m + 1e-9), 0)
    return ux.astype(np.float32), uy.astype(np.float32)

def shape_maps(scene, angles):
    ux, uy = grad_unit(scene)
    out = []
    K = T + 20
    for a in angles:
        th = np.deg2rad(a); c, s = np.cos(th), np.sin(th)
        rx = np.round(c * ox - s * oy).astype(int) + K // 2
        ry = np.round(s * ox + c * oy).astype(int) + K // 2
        dx = c * mdx - s * mdy; dy = s * mdx + c * mdy
        Kx = np.zeros((K, K), np.float32); Ky = np.zeros((K, K), np.float32)
        np.add.at(Kx, (ry, rx), dx / n_model); np.add.at(Ky, (ry, rx), dy / n_model)
        sc = cv2.filter2D(ux, -1, Kx, borderType=cv2.BORDER_CONSTANT) + cv2.filter2D(uy, -1, Ky, borderType=cv2.BORDER_CONSTANT)
        out.append(sc)
    return np.array(out)

# (c) score vs rotation offset of a single clean part
offs = np.arange(0, 41, 1)
ncc_curve, shp_curve = [], []
for d in offs:
    sc = render([(160, 160, d, 1.0)])[:320, :320]
    sc = np.clip(sc + rng.normal(0, 5, sc.shape), 0, 255).astype(np.uint8)
    ncc_curve.append(ncc_maps(sc, [0])[0][150:171, 150:171].max())
    shp_curve.append(shape_maps(sc, [0])[0][150:171, 150:171].max())
ncc_curve = np.array(ncc_curve); shp_curve = np.array(shp_curve)
def first_below(c, t):
    i = np.where(c < t)[0]; return offs[i[0]] if len(i) else None
print("NCC <0.8 at", first_below(ncc_curve, 0.8), "<0.5 at", first_below(ncc_curve, 0.5))
print("shape <0.8 at", first_below(shp_curve, 0.8), "<0.5 at", first_below(shp_curve, 0.5))

angles = np.arange(0, 360, 2)
t0 = time.time(); N = ncc_maps(img, angles); tn = time.time() - t0
t0 = time.time(); S = shape_maps(img, angles); ts = time.time() - t0
N0 = ncc_maps(img, [0])[0]
print("times", tn, ts)
def at_truth(stack, cx, cy, r=3):
    sub = stack[:, cy - r:cy + r + 1, cx - r:cx + r + 1]
    i = np.unravel_index(np.argmax(sub), sub.shape)
    return sub.max(), angles[i[0]] if stack.shape[0] > 1 else 0
res = []
for k, (cx, cy, a, g) in enumerate(objs):
    n0 = N0[cy - 3:cy + 4, cx - 3:cx + 4].max()
    nm_, na = at_truth(N, cx, cy); sm_, sa = at_truth(S, cx, cy)
    def aerr(x): d = abs((x - a + 180) % 360 - 180); return d
    res.append((n0, nm_, aerr(na), sm_, aerr(sa)))
    print(k + 1, "NCC0 %.2f NCCrot %.2f (err %d) shape %.2f (err %d)" % (n0, nm_, aerr(na), sm_, aerr(sa)))
# detections above threshold with NMS
def detect(stack, thr):
    M = stack.max(0); A = angles[stack.argmax(0)]
    pk = (M == cv2.dilate(M, np.ones((41, 41)))) & (M > thr)
    ys, xs = np.where(pk)
    return [(x, y, A[y, x], M[y, x]) for x, y in zip(xs, ys)]
for name, st, thr in [("ncc", N, 0.5), ("ncc", N, 0.6), ("ncc", N, 0.7), ("shape", S, 0.5), ("shape", S, 0.6), ("shape", S, 0.7)]:
    d = detect(st, thr)
    tp = sum(any(np.hypot(x - cx, y - cy) < 6 for cx, cy, _, _ in objs) for x, y, _, _ in d)
    print(name, "thr", thr, "detections", len(d), "true", tp, "false", len(d) - tp)
dets = detect(S, 0.6)

fig = plt.figure(figsize=(16, 4.3))
gs = fig.add_gridspec(1, 4, width_ratios=[0.62, 1.45, 1.0, 1.0], wspace=0.28)
ax = fig.add_subplot(gs[0]); img_ax(ax)
ax.imshow(timg, cmap="gray", vmin=0, vmax=255)
ax.plot(px, py, ".", ms=1.2, color=ORANGE)
ax.set_title("(a) template and\nmodel edge points")
ax = fig.add_subplot(gs[1]); img_ax(ax)
ax.imshow(img, cmap="gray", vmin=0, vmax=255)
for x, y, a, s in dets:
    th = np.deg2rad(a); c, s_ = np.cos(th), np.sin(th)
    ex = c * ox - s_ * oy + x; ey = s_ * ox + c * oy + y
    ax.plot(ex, ey, ".", ms=0.8, color=ORANGE)
    ax.text(x, y - 48, "%d°, %.2f" % (a, s), color="white", fontsize=9, ha="center",
            bbox=dict(fc=DARK, ec="none", alpha=0.75, pad=1.5))
ax.set_title("(b) shape-based matching over 0–358°\n%d parts found, labeled with angle and score" % len(dets))
ax = fig.add_subplot(gs[2])
ax.plot(offs, ncc_curve, color=BLUE, lw=2, label="normalized cross-correlation")
ax.plot(offs, shp_curve, color=ORANGE, lw=2, label="gradient-direction score")
ax.set_xlabel("rotation of the part (°)"); ax.set_ylabel("best score"); ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=9, loc="lower left")
ax.set_title("(c) score of a 0° model vs. part rotation")
ax = fig.add_subplot(gs[3])
lab = ["1\n0°", "2\n25°", "3\n140°", "4\n70°\ndim", "5\n200°\nhidden"]
xi = np.arange(5); w = 0.27
ax.bar(xi - w, [r[0] for r in res], w, color=GRAY, label="NCC, 0° only")
ax.bar(xi, [r[1] for r in res], w, color=BLUE, label="NCC, all angles")
ax.bar(xi + w, [r[3] for r in res], w, color=ORANGE, label="gradient direction, all angles")
ax.set_xticks(xi); ax.set_xticklabels(lab, fontsize=8.5); ax.set_ylim(0, 1.42); ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_ylabel("score at the true position")
ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=1)
ax.set_title("(d) score per part")
plt.savefig("roi-template-matching.png", bbox_inches="tight", facecolor="white")
