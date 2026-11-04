"""Figure 17: color calibration with a generic 24-patch reference chart and a 3x3 color correction matrix."""
import json
import sys

import matplotlib
import numpy as np
from skimage.color import deltaE_ciede2000, lab2rgb, rgb2lab

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle

OUT = sys.argv[1]
for f in font_manager.findSystemFonts():
    if "Inter" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 11})
BG, TXT, BLUE, GRAY, RED = "#fbfbf8", "#2f2e2b", "#2a78d6", "#a9a49b", "#d94848"
rng = np.random.default_rng(11)

# generic reference chart (own design): 18 chromatic patches on a hue circle at two lightness/chroma levels + 6 neutrals
labs = []
for i, h in enumerate(np.linspace(0, 360, 9, endpoint=False)):
    labs.append([62, 48 * np.cos(np.deg2rad(h)), 48 * np.sin(np.deg2rad(h))])
for h in np.linspace(20, 380, 9, endpoint=False):
    labs.append([42, 30 * np.cos(np.deg2rad(h)), 30 * np.sin(np.deg2rad(h))])
for L in [95, 80, 65, 50, 35, 20]:
    labs.append([L, 0, 0])
labs = np.array(labs, float)
ref_srgb = np.clip(lab2rgb(labs[None])[0], 0, 1)
ref_lab = rgb2lab(ref_srgb[None])[0]


def to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


ref_lin = to_lin(ref_srgb)
# simulated camera: sensor spectral crosstalk + warm LED illuminant + exposure + noise
M_cam = np.array([[0.82, 0.22, 0.02], [0.12, 0.78, 0.16], [0.03, 0.20, 0.80]])
illum = np.array([1.18, 1.0, 0.72])
cam = (ref_lin * illum) @ M_cam.T * 0.92
cam = np.clip(cam + rng.normal(0, 0.003, cam.shape), 0, 1)

# least-squares 3x3 colour correction matrix (camera linear RGB -> reference linear RGB)
CCM, *_ = np.linalg.lstsq(cam, ref_lin, rcond=None)
corr = np.clip(cam @ CCM, 0, 1)

cam_srgb, corr_srgb = to_srgb(cam), to_srgb(corr)
dE_raw = deltaE_ciede2000(ref_lab, rgb2lab(cam_srgb[None])[0])
dE_cor = deltaE_ciede2000(ref_lab, rgb2lab(corr_srgb[None])[0])
stats = {"dE00_raw_mean": round(float(dE_raw.mean()), 1), "dE00_raw_max": round(float(dE_raw.max()), 1),
         "dE00_corr_mean": round(float(dE_cor.mean()), 2), "dE00_corr_max": round(float(dE_cor.max()), 2),
         "CCM": np.round(CCM.T, 3).tolist()}

fig = plt.figure(figsize=(16, 4.4), facecolor=BG)
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.25], wspace=0.12)


def chart(ax, cols, title, xlabel):
    ax.set_facecolor(BG)
    ax.add_patch(Rectangle((-0.15, -0.15), 6.3, 4.3, color="#3d3b38"))
    for k in range(24):
        r, c = divmod(k, 6)
        ax.add_patch(Rectangle((c + 0.06, 3 - r + 0.06), 0.88, 0.88, color=cols[k]))
        ax.add_patch(Rectangle((c + 0.32, 3 - r + 0.32), 0.36, 0.36, color=ref_srgb[k], ec="white", lw=0.6))
    ax.set_xlim(-0.3, 6.3); ax.set_ylim(-0.3, 4.3); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
    ax.set_title(title, color=TXT, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel, color=TXT)


chart(fig.add_subplot(gs[0]), cam_srgb, "(a) Captured chart",
      f"warm light and sensor crosstalk shift all colors;\nmean ΔE00 = {stats['dE00_raw_mean']} (inner squares = reference)")
chart(fig.add_subplot(gs[1]), corr_srgb, "(b) After color correction",
      f"3 × 3 color correction matrix fitted to the chart;\nmean ΔE00 = {stats['dE00_corr_mean']}")
ax = fig.add_subplot(gs[2]); ax.set_facecolor(BG)
x = np.arange(24)
ax.bar(x - 0.2, dE_raw, 0.4, color=GRAY, label="captured")
ax.bar(x + 0.2, dE_cor, 0.4, color=BLUE, label="corrected")
ax.axhline(2.0, color=RED, ls="--", lw=1.2, label="example tolerance ΔE00 = 2")
ax.set_xticks(x[::1]); ax.set_xticklabels([str(i + 1) for i in x], fontsize=8)
ax.set_xlabel("patch number (left to right, top to bottom)", color=TXT)
ax.set_ylabel("color difference ΔE00", color=TXT)
ax.set_title("(c) Color error per patch", color=TXT, fontsize=13, fontweight="bold")
ax.tick_params(colors=TXT, labelsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=9)
plt.savefig(OUT, dpi=105, facecolor=BG, bbox_inches="tight")
print(json.dumps(stats, indent=1))
