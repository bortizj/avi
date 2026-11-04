"""Figure 15: lens distortion correction and pixel-to-mm mapping (simulated, then calibrated with OpenCV)."""
import json
import sys

import cv2
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = sys.argv[1]
for f in font_manager.findSystemFonts():
    if "Inter" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 11})
BG, TXT, BLUE, AMBER, RED = "#fbfbf8", "#2f2e2b", "#2a78d6", "#eea200", "#d94848"

rng = np.random.default_rng(7)
W, H = 1280, 960
K_true = np.array([[1150.0, 0, 652.0], [0, 1150.0, 474.0], [0, 0, 1]])
D_true = np.array([-0.30, 0.12, 0.0012, -0.0008, 0.0])

# planar checkerboard: 11 x 8 squares of 10 mm -> 10 x 7 inner corners
SQ, NX, NY = 10.0, 11, 8
PAT = (NX - 1, NY - 1)


def render(rvec, tvec, K=K_true, D=D_true, w=W, h=H, ss=2):
    """Render a distorted image of the board by back-projecting every pixel onto the board plane (supersampled)."""
    uu, vv = np.meshgrid((np.arange(w * ss) + 0.5) / ss, (np.arange(h * ss) + 0.5) / ss)
    pts = np.stack([uu.ravel(), vv.ravel()], 1).reshape(-1, 1, 2).astype(np.float64)
    n = cv2.undistortPoints(pts, K, D).reshape(-1, 2)
    rays = np.c_[n, np.ones(len(n))]
    R, _ = cv2.Rodrigues(rvec)
    # board plane z=0 in board frame -> in camera frame: normal R[:,2], point t
    nrm, t = R[:, 2], tvec.ravel()
    s = (nrm @ t) / (rays @ nrm)
    Xc = rays * s[:, None]
    Xb = (Xc - t) @ R  # back to board frame
    x, y = Xb[:, 0], Xb[:, 1]
    inside = (x >= -SQ) & (x < (NX - 1) * SQ) & (y >= -SQ) & (y < (NY - 1) * SQ) & (s > 0)
    chk = ((np.floor(x / SQ) + np.floor(y / SQ)) % 2 == 0)
    img = np.where(inside, np.where(chk, 30, 225), 150).astype(np.float32)
    img = cv2.resize(img.reshape(h * ss, w * ss), (w, h), interpolation=cv2.INTER_AREA)
    img = cv2.GaussianBlur(img, (0, 0), 0.7)
    img += rng.normal(0, 2.0, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


obj = np.zeros((PAT[0] * PAT[1], 3), np.float32)
obj[:, :2] = np.mgrid[0:PAT[0], 0:PAT[1]].T.reshape(-1, 2) * SQ

# calibration poses: board at ~250 mm, tilted +-35 deg, spread over the field of view
poses = []
for ax, ay, dx, dy in [(0, 0, 0, 0), (25, 0, 0, 0), (-25, 0, 0, 0), (0, 25, 0, 0), (0, -25, 0, 0),
                       (30, 20, 0, 0), (-30, 20, 0, 0), (30, -20, 0, 0), (-30, -20, 0, 0),
                       (0, 0, -60, -40), (0, 0, 60, -40), (0, 0, -60, 40), (0, 0, 60, 40),
                       (15, -15, -40, 30), (-15, 15, 40, -30), (35, 0, 30, 0), (0, -35, 0, 20)]:
    R = cv2.Rodrigues(np.deg2rad([ax, 0, 0]))[0] @ cv2.Rodrigues(np.deg2rad([0, ay, 0]))[0]
    rvec = cv2.Rodrigues(R)[0]
    centre = np.array([(NX - 2) * SQ / 2, (NY - 2) * SQ / 2, 0])
    tvec = (np.array([dx, dy, 190.0]) - R @ centre).reshape(3, 1)
    poses.append((rvec, tvec))

imgpts, objpts, imgs = [], [], []
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1e-4)
for rvec, tvec in poses:
    im = render(rvec, tvec)
    ok, c = cv2.findChessboardCorners(im, PAT, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
    if not ok:
        continue
    c = cv2.cornerSubPix(im, c, (7, 7), (-1, -1), crit)
    imgpts.append(c)
    objpts.append(obj)
    imgs.append(im)

rms, K, D, rv, tv = cv2.calibrateCamera(objpts, imgpts, (W, H), None, None)
stats = {"views_used": len(imgpts), "rms_px": round(float(rms), 3),
         "fx_est": round(float(K[0, 0]), 1), "fy_est": round(float(K[1, 1]), 1),
         "cx_est": round(float(K[0, 2]), 1), "cy_est": round(float(K[1, 2]), 1),
         "k1_est": round(float(D.ravel()[0]), 4), "k2_est": round(float(D.ravel()[1]), 4)}

# showcase view: large, slightly tilted board filling the image, at a longer distance
R = cv2.Rodrigues(np.deg2rad([-12, 0, 0]))[0] @ cv2.Rodrigues(np.deg2rad([0, 10, 0]))[0]
rvec_s = cv2.Rodrigues(R)[0]
centre = np.array([(NX - 2) * SQ / 2, (NY - 2) * SQ / 2, 0])
tvec_s = (np.array([0, 0, 100.0]) - R @ centre).reshape(3, 1)
raw = render(rvec_s, tvec_s)
und = cv2.undistort(raw, K, D)

# pixel-to-mm: detect corners on undistorted view, fit homography to board coordinates, warp to 0.1 mm/px
ok, cu = cv2.findChessboardCorners(und, PAT)
cu = cv2.cornerSubPix(und, cu, (7, 7), (-1, -1), crit)
MMPX = 0.1
dst = (obj[:, :2] + SQ) / MMPX  # board origin shifted by one square, 0.1 mm per pixel
Hm, _ = cv2.findHomography(cu.reshape(-1, 2), dst)
out_w, out_h = int((NX) * SQ / MMPX), int((NY) * SQ / MMPX)
rect = cv2.warpPerspective(und, Hm, (out_w, out_h), borderValue=150)

# measurement check on the rectified image: distance between first and last corner of row 0
p = cv2.perspectiveTransform(cu.reshape(-1, 1, 2), Hm).reshape(-1, 2)
row_len_mm = np.linalg.norm(p[PAT[0] - 1] - p[0]) * MMPX
# naive single scale factor on the raw image (no calibration): mean square size in px from central row
ok_r, cr = cv2.findChessboardCorners(raw, PAT)
cr = cv2.cornerSubPix(raw, cr, (7, 7), (-1, -1), crit).reshape(-1, 2)
mid = PAT[1] // 2
row = cr[mid * PAT[0]:(mid + 1) * PAT[0]]
scale_naive = SQ / np.mean(np.linalg.norm(np.diff(row[3:7], axis=0), axis=1))  # mm/px from centre squares
edge_row = cr[0:PAT[0]]
naive_len = np.linalg.norm(edge_row[-1] - edge_row[0]) * scale_naive
stats.update({"true_row_len_mm": (PAT[0] - 1) * SQ, "calibrated_row_len_mm": round(float(row_len_mm), 3),
              "naive_edge_row_len_mm": round(float(naive_len), 2)})

fig, axs = plt.subplots(1, 3, figsize=(16, 4.9), facecolor=BG, gridspec_kw={"width_ratios": [1, 1, 1.03]})
for a in axs:
    a.set_facecolor(BG)
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values():
        s.set_visible(False)

axs[0].imshow(raw, cmap="gray", vmin=0, vmax=255)
a, b = edge_row[0], edge_row[-1]
axs[0].plot([a[0], b[0]], [a[1], b[1]], "--", color=AMBER, lw=2)
axs[0].plot(edge_row[:, 0], edge_row[:, 1], "o", color=RED, ms=4)
axs[0].set_title("(a) Captured image", color=TXT, fontsize=13, fontweight="bold")
axs[0].set_xlabel("barrel distortion bends straight rows (red)\naway from the straight reference (dashed)", color=TXT)

ok_u, cu2 = cv2.findChessboardCorners(und, PAT)
cu2 = cv2.cornerSubPix(und, cu2, (7, 7), (-1, -1), crit).reshape(-1, 2)
er = cu2[0:PAT[0]]
axs[1].imshow(und, cmap="gray", vmin=0, vmax=255)
axs[1].plot([er[0, 0], er[-1, 0]], [er[0, 1], er[-1, 1]], "--", color=AMBER, lw=2)
axs[1].plot(er[:, 0], er[:, 1], "o", color=BLUE, ms=4)
axs[1].set_title("(b) After distortion correction", color=TXT, fontsize=13, fontweight="bold")
axs[1].set_xlabel(f"rows are straight again; calibration from {len(imgpts)} views,\nRMS reprojection error {rms:.2f} px", color=TXT)

ext = [-SQ, out_w * MMPX - SQ, out_h * MMPX - SQ, -SQ]
axs[2].imshow(rect, cmap="gray", vmin=0, vmax=255, extent=ext)
axs[2].set_xticks(np.arange(0, 101, 20)); axs[2].set_yticks(np.arange(0, 71, 20))
axs[2].tick_params(colors=TXT, labelsize=9)
axs[2].set_title("(c) Pixel-to-mm mapping", color=TXT, fontsize=13, fontweight="bold")
axs[2].set_xlabel(f"rectified to the measurement plane at {MMPX} mm/px (axes in mm);\n"
                  f"9 squares measure {row_len_mm:.2f} mm (nominal 90.00 mm)", color=TXT)
plt.tight_layout()
plt.savefig(OUT, dpi=110, facecolor=BG)
print(json.dumps(stats, indent=1))
