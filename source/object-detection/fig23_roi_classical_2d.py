"""Figure 23 of 05_object_detection.md (roi-classical-2d.png).

Classical 2D detection on a simulated backlit image: Otsu threshold and blob analysis,
distance transform and watershed for touching parts, Canny edges and Hough circles.

Run:  python fig23_roi_classical_2d.py
Output: roi-classical-2d.png in the current folder; the numbers quoted in the text are printed to the console.
"""
import numpy as np, cv2
from style import *
rng = np.random.default_rng(7)
H, W = 360, 600
# ground truth objects on a backlight: washers (rings) and rectangular plates
mask = np.zeros((H, W), np.uint8)
inst = np.zeros((H, W), np.int32)
washers = [(110, 120, 46, 18), (196, 126, 46, 18), (110, 262, 40, 15)]  # cx, cy, R, r  (first two touch)
plates = [(400, 110, 150, 60, 20.0), (470, 255, 120, 70, -35.0), (290, 270, 90, 45, 62.0)]  # cx,cy,w,h,angle
k = 0
for cx, cy, R, r in washers:
    k += 1
    m = np.zeros_like(mask); cv2.circle(m, (cx, cy), R, 1, -1); cv2.circle(m, (cx, cy), r, 0, -1)
    inst[m > 0] = k
for cx, cy, w, h, a in plates:
    k += 1
    m = np.zeros_like(mask)
    box = cv2.boxPoints(((cx, cy), (w, h), a)).astype(np.int32)
    cv2.fillPoly(m, [box], 1)
    # two holes
    th = np.deg2rad(a)
    for s in (-0.3, 0.3):
        hx = int(round(cx + s * w * np.cos(th))); hy = int(round(cy + s * w * np.sin(th)))
        cv2.circle(m, (hx, hy), 9, 0, -1)
    inst[m > 0] = k
mask = (inst > 0).astype(np.uint8)
n_true = k
# backlit image: bright background with mild fall-off, dark parts, noise
yy, xx = np.mgrid[0:H, 0:W]
bg = 215 - 35 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 4
img = np.where(mask > 0, 40.0, bg)
img = cv2.GaussianBlur(img, (0, 0), 1.0)
img = img + rng.normal(0, 6, img.shape)
img = np.clip(img, 0, 255).astype(np.uint8)

# (b) Otsu + connected components
t, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
ncc, lab, stats, cent = cv2.connectedComponentsWithStats(bw)
blobs = [i for i in range(1, ncc) if stats[i, cv2.CC_STAT_AREA] > 200]
# pixel accuracy of the foreground
fg_iou = ((bw > 0) & (mask > 0)).sum() / ((bw > 0) | (mask > 0)).sum()

# (c) watershed on distance transform (fill holes first)
filled = bw.copy()
cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(filled, cnts, -1, 255, -1)
dist = cv2.distanceTransform(filled, cv2.DIST_L2, 5)
ncomp, comp = cv2.connectedComponents(filled)
peaks = np.zeros_like(filled, bool)
for c in range(1, ncomp):
    m = comp == c
    peaks |= m & (dist > 0.7 * dist[m].max())
nm, markers = cv2.connectedComponents(peaks.astype(np.uint8))
markers = markers + 1
markers[filled == 0] = 1  # background marker
unknown = (filled > 0) & (~peaks)
markers[unknown] = 0
from skimage.segmentation import watershed as skws
pk = cv2.connectedComponents(peaks.astype(np.uint8))[1]
ws = skws(-dist, pk, mask=filled > 0) + 1  # 1 = background, 2.. = objects
regions = [l for l in np.unique(ws) if l > 1]
regions = [l for l in regions if ((ws == l) & (bw > 0)).sum() > 200]
# oriented boxes and angle errors for plates
rects = []
for l in regions:
    pts = np.column_stack(np.where((ws == l) & (filled > 0)))[:, ::-1].astype(np.float32)
    rects.append(cv2.minAreaRect(pts))
def angerr(a_est, a_true):
    d = (a_est - a_true) % 90
    return min(d, 90 - d)
plate_err = []
for cx, cy, w, h, a in plates:
    r = min(rects, key=lambda r: (r[0][0] - cx) ** 2 + (r[0][1] - cy) ** 2)
    plate_err.append((np.hypot(r[0][0] - cx, r[0][1] - cy), angerr(r[2], a)))

# (d) Canny + Hough circles on the image
blur = cv2.GaussianBlur(img, (0, 0), 1.5)
edges = cv2.Canny(blur, 40, 100)
circ = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=30, param1=100, param2=30, minRadius=35, maxRadius=55)
circ = circ[0] if circ is not None else np.zeros((0, 3))
c_err = []
for cx, cy, R, r in washers:
    if len(circ):
        j = np.argmin((circ[:, 0] - cx) ** 2 + (circ[:, 1] - cy) ** 2)
        c_err.append((np.hypot(circ[j, 0] - cx, circ[j, 1] - cy), abs(circ[j, 2] - R)))
print("otsu t", t, "blobs", len(blobs), "true", n_true, "fg IoU", round(fg_iou, 4))
print("watershed regions", len(regions))
print("plate center/angle err", [(round(a, 2), round(b, 2)) for a, b in plate_err])
print("hough circles", len(circ), "errors", [(round(a, 2), round(b, 2)) for a, b in c_err])

fig, axs = plt.subplots(1, 4, figsize=(16, 3.6))
for ax in axs: img_ax(ax)
axs[0].imshow(img, cmap="gray", vmin=0, vmax=255)
axs[0].set_title("(a) backlit image with %d parts" % n_true)
axs[1].imshow(img, cmap="gray", vmin=0, vmax=255, alpha=0.55)
for i in blobs:
    x, y, w, h = stats[i, :4]
    axs[1].add_patch(plt.Rectangle((x, y), w, h, fill=False, ec=ORANGE, lw=1.8))
axs[1].set_title("(b) Otsu threshold and blobs\n%d blobs found" % len(blobs))
over = np.zeros((H, W, 4))
for j, l in enumerate(regions):
    c = matplotlib.colors.to_rgba(PALETTE[j % len(PALETTE)], 0.55)
    over[(ws == l) & (bw > 0)] = c
axs[2].imshow(img, cmap="gray", vmin=0, vmax=255)
axs[2].imshow(over)
for r in rects:
    b = cv2.boxPoints(r)
    axs[2].add_patch(plt.Polygon(b, fill=False, ec=DARK, lw=1.4))
axs[2].set_title("(c) distance transform and watershed\n%d regions with oriented boxes" % len(regions))
axs[3].imshow(255 - edges, cmap="gray", vmin=0, vmax=255)
for cx, cy, R in circ:
    axs[3].add_patch(plt.Circle((cx, cy), R, fill=False, ec=ORANGE, lw=2))
    axs[3].plot(cx, cy, "+", color=ORANGE, ms=9, mew=2)
axs[3].set_title("(d) Canny edges and Hough circles\n%d circles found" % len(circ))
plt.tight_layout()
plt.savefig("roi-classical-2d.png", bbox_inches="tight", facecolor="white")
