"""Figure 26 of 05_object_detection.md (roi-pointcloud-segmentation.png).

3D detection in a simulated height scan: RANSAC plane fit of the conveyor, DBSCAN clustering,
oriented bounding boxes, and the sensitivity of the number of clusters to eps.

Run:  python fig26_roi_pointcloud_segmentation.py
Output: roi-pointcloud-segmentation.png in the current folder; the numbers quoted in the text are printed to the console.
"""
import numpy as np
from sklearn.cluster import DBSCAN
from style import *
rng = np.random.default_rng(5)
step = 1.0
xs = np.arange(0, 300, step); ys = np.arange(0, 200, step)
X, Y = np.meshgrid(xs, ys)
tilt = np.array([0.03, -0.015])          # conveyor plane z = a x + b y + 5
Zp = tilt[0] * X + tilt[1] * Y + 5
Z = Zp.copy(); lab = np.zeros(X.shape, int)
def box(cx, cy, L, Wd, Hh, ang, k):
    th = np.deg2rad(ang); u = (X - cx) * np.cos(th) + (Y - cy) * np.sin(th); v = -(X - cx) * np.sin(th) + (Y - cy) * np.cos(th)
    m = (np.abs(u) <= L / 2) & (np.abs(v) <= Wd / 2)
    Z[m] = Zp[m] + Hh; lab[m] = k
def cyl(cx, cy, r, Hh, k):
    m = (X - cx) ** 2 + (Y - cy) ** 2 <= r * r
    Z[m] = Zp[m] + Hh; lab[m] = k
parts = {1: ("box", 60, 40, 30, 20), 2: ("box", 50, 30, 15, -40), 3: ("cyl", 40, 40, 35, 0), 4: ("box", 40, 25, 10, 0), 5: ("box", 40, 25, 10, 0)}
box(70, 60, 60, 40, 30, 20, 1); box(200, 55, 50, 30, 15, -40, 2); cyl(80, 145, 20, 35, 3)
box(200, 140, 40, 25, 10, 0, 4); box(243, 140, 40, 25, 10, 0, 5)   # 3 mm gap between parts 4 and 5
P = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()]); L = lab.ravel()
P[:, 2] += rng.normal(0, 0.3, len(P))
# a few outliers (reflections)
no = 300; out = np.column_stack([rng.uniform(0, 300, no), rng.uniform(0, 200, no), rng.uniform(0, 60, no)])
P = np.vstack([P, out]); L = np.concatenate([L, -np.ones(no, int)])
print("points", len(P))

# RANSAC plane
best = (0, None)
for it in range(300):
    s = P[rng.choice(len(P), 3, replace=False)]
    n = np.cross(s[1] - s[0], s[2] - s[0]); nn = np.linalg.norm(n)
    if nn < 1e-9: continue
    n /= nn; d = -n @ s[0]
    inl = np.abs(P @ n + d) < 1.0
    if inl.sum() > best[0]: best = (inl.sum(), (n, d))
n, d = best[1]
inl = np.abs(P @ n + d) < 1.0
# least-squares refinement
A = np.column_stack([P[inl, 0], P[inl, 1], np.ones(inl.sum())]); coef, *_ = np.linalg.lstsq(A, P[inl, 2], rcond=None)
n = np.array([-coef[0], -coef[1], 1.0]); n /= np.linalg.norm(n); d = -n @ np.array([0, 0, coef[2]])
ntrue = np.array([-tilt[0], -tilt[1], 1.0]); ntrue /= np.linalg.norm(ntrue)
ang_err = np.degrees(np.arccos(abs(n @ ntrue)))
h = P @ n + d
plane_pts = np.abs(h) < 1.0
print("plane inliers %.3f of points, normal error %.4f deg" % (plane_pts.mean(), ang_err))
print("true plane points", (L == 0).mean())
obj = h > 2.0
Q = P[obj]; Hq = h[obj]; Lq = L[obj]
# coordinates in the plane frame (u, v along the plane)
e1 = np.cross([0, 1, 0], n); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
uv = np.column_stack([Q @ e1, Q @ e2])
def run(eps):
    db = DBSCAN(eps=eps, min_samples=8).fit(np.column_stack([uv, Hq]))
    labs = db.labels_
    k = len(set(labs) - {-1}); noise = (labs == -1).sum()
    return labs, k, noise
eps_list = [0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
counts = []
for e in eps_list:
    _, k, noise = run(e); counts.append(k); print("eps", e, "clusters", k, "noise", noise)
labs, k, noise = run(2.0)
# oriented boxes from PCA in the plane frame + height
boxes = []
for c in sorted(set(labs) - {-1}):
    m = labs == c
    if m.sum() < 100: continue
    pts = uv[m]; mu = pts.mean(0); C = np.cov((pts - mu).T); w, V = np.linalg.eigh(C)
    R = V[:, ::-1]; loc = (pts - mu) @ R
    lo, hi = loc.min(0), loc.max(0); ctr = mu + R @ ((lo + hi) / 2)
    ang = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    height = np.median(Hq[m])
    true_k = np.bincount(Lq[m][Lq[m] > 0]).argmax()
    boxes.append((c, ctr, hi - lo, ang, height, R, lo, hi, mu, true_k))
    print("cluster", c, "n", m.sum(), "size %.1f x %.1f, h %.1f, true part %d" % ((hi - lo)[0], (hi - lo)[1], height, true_k))

fig = plt.figure(figsize=(16, 3.9))
gs = fig.add_gridspec(1, 4, width_ratios=[1.15, 1.0, 1.15, 0.9], wspace=0.32)
ax = fig.add_subplot(gs[0]); sub = rng.choice(len(P), 30000, replace=False)
sc = ax.scatter(P[sub, 0], P[sub, 1], c=P[sub, 2], s=0.6, cmap="viridis", vmin=0, vmax=45, rasterized=True)
ax.set_aspect("equal"); ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)"); ax.set_title("(a) raw point cloud, top view\ncolor = height z (0 to 45 mm)")
ax = fig.add_subplot(gs[1]); sub2 = rng.choice(len(P), 25000, replace=False)
ax.scatter(P[sub2, 0][plane_pts[sub2]], P[sub2, 2][plane_pts[sub2]], s=0.5, color=GRAY, rasterized=True, label="plane inliers")
ax.scatter(P[sub2, 0][~plane_pts[sub2]], P[sub2, 2][~plane_pts[sub2]], s=0.8, color=ORANGE, rasterized=True, label="other points")
ax.set_xlabel("x (mm)"); ax.set_ylabel("z (mm)"); ax.set_title("(b) RANSAC plane, side view\nnormal error %.3f°" % ang_err)
ax.legend(frameon=False, fontsize=9, markerscale=8, loc="upper left")
ax = fig.add_subplot(gs[2])
ax.scatter(uv[:, 0], uv[:, 1], s=0.3, color="#DDDDD6", rasterized=True)
for j, (c, ctr, sz, ang, height, R, lo, hi, mu, tk) in enumerate(boxes):
    m = labs == c
    ax.scatter(uv[m, 0], uv[m, 1], s=0.4, color=PALETTE[j % len(PALETTE)], rasterized=True)
    corners = np.array([[lo[0], lo[1]], [hi[0], lo[1]], [hi[0], hi[1]], [lo[0], hi[1]], [lo[0], lo[1]]])
    cw = mu + corners @ R.T
    ax.plot(cw[:, 0], cw[:, 1], color=DARK, lw=1)
    yoff = (0.62 * max(sz) + 4) * (-1.35 if tk == 5 else 1)
    ax.text(ctr[0], ctr[1] + yoff, "%.0f×%.0f×%.0f" % (sz[0], sz[1], height), ha="center", fontsize=8.5, color=DARK)
ax.set_aspect("equal"); ax.set_xlabel("u (mm)"); ax.set_ylabel("v (mm)")
ax.set_title("(c) DBSCAN with eps = 2 mm\n%d clusters, oriented boxes in mm" % len(boxes))
ax = fig.add_subplot(gs[3])
ax.plot(eps_list, counts, "o-", color=ORANGE, lw=2)
ax.axhline(5, color=GRAY, ls="--", lw=1.2); ax.text(4.9, 5.3, "5 parts", ha="right", color="#555555", fontsize=9)
ax.set_ylim(-0.3, 8); ax.set_xlabel("eps (mm)"); ax.set_ylabel("number of clusters")
ax.set_title("(d) clusters vs. eps\n(point spacing 1 mm, gap 3 mm)")
plt.savefig("roi-pointcloud-segmentation.png", bbox_inches="tight", facecolor="white")
