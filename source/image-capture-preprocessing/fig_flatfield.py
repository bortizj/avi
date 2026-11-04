"""Figure 16: dark-frame and flat-field correction (simulated sensor, lens and illumination)."""
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
BG, TXT, BLUE, AMBER, RED, GRAY = "#fbfbf8", "#2f2e2b", "#2a78d6", "#eea200", "#d94848", "#8a867e"
rng = np.random.default_rng(3)
W, H = 640, 480
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

# lens vignetting (cos^4-like) and off-centre illumination gradient from one side light
r2 = ((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (0.62 * W) ** 2
vignette = 1.0 / (1 + r2) ** 2
light = 0.70 + 0.30 * np.exp(-(((xx - 0.30 * W) / (0.55 * W)) ** 2 + ((yy - 0.35 * H) / (0.75 * H)) ** 2))
gain_field = vignette * light
prnu = 1 + rng.normal(0, 0.012, (H, W)).astype(np.float32)           # pixel sensitivity spread
dsnu = 6 + rng.normal(0, 1.2, (H, W)).astype(np.float32) + 1.5 * np.sin(xx / 7.0)  # dark offset + column pattern

# scene: uniform brushed surface (reflectance 0.62) with a faint stain (-12 %) and a thin scratch (-12 %)
refl = np.full((H, W), 0.62, np.float32)
stain = np.exp(-(((xx - 520) / 26) ** 2 + ((yy - 380) / 20) ** 2))
refl *= 1 - 0.12 * stain
scratch = (np.abs((yy - 150) - 0.18 * (xx - 120)) < 1.6) & (xx > 120) & (xx < 330)
refl[scratch] *= 0.88
truth = (stain > 0.6) | scratch

FULL = 255 / 0.62 * 0.95  # exposure so that the brightest good area sits near 95 % of full scale


def capture(reflectance, n=1, light_on=True):
    acc = np.zeros((H, W), np.float32)
    for _ in range(n):
        sig = FULL * reflectance * gain_field * prnu if light_on else 0
        img = sig + dsnu + rng.normal(0, 1.5, (H, W))
        acc += np.clip(img, 0, 255)
    return acc / n


raw = capture(refl)
dark = capture(refl, n=32, light_on=False)
flat = capture(np.full((H, W), 0.55, np.float32), n=32)  # uniform white/grey reference, 32 frames averaged
corr = (raw - dark) / np.maximum(flat - dark, 1) * np.mean(flat - dark)

# same fixed rule on both images: a pixel is a defect if it is >6 % darker than the median good level
def detect(img):
    ref = np.median(img)
    m = img < 0.94 * ref
    return cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)).astype(bool)


d_raw, d_corr = detect(raw), detect(corr)
area = H * W
stats = {
    "raw_brightest_to_darkest_ratio": round(float(np.percentile(raw[~truth], 99.5) / np.percentile(raw[~truth], 0.5)), 2),
    "corr_brightest_to_darkest_ratio": round(float(np.percentile(corr[~truth], 99.5) / np.percentile(corr[~truth], 0.5)), 3),
    "raw_false_alarm_area_pct": round(float((d_raw & ~truth).sum() / area * 100), 1),
    "corr_false_alarm_area_pct": round(float((d_corr & ~truth).sum() / area * 100), 2),
    "corr_defect_recall_pct": round(float((d_corr & truth).sum() / truth.sum() * 100), 1),
    "raw_defect_recall_pct": round(float((d_raw & truth).sum() / truth.sum() * 100), 1),
}

fig = plt.figure(figsize=(16, 9.2), facecolor=BG)
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], hspace=0.32, wspace=0.08)


def show(ax, img, title, xlabel, cmap="gray", vmin=0, vmax=255):
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(title, color=TXT, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel, color=TXT)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


show(fig.add_subplot(gs[0, 0]), raw, "(a) Captured image",
     "vignetting and uneven light: corners are\nmuch darker than the stain and the scratch")
show(fig.add_subplot(gs[0, 1]), flat, "(b) Flat-field reference",
     "uniform target, 32 frames averaged;\na dark frame (not shown) is recorded with the light off")
show(fig.add_subplot(gs[0, 2]), np.clip(corr, 0, 255), "(c) Corrected image",
     "(raw − dark) / (flat − dark) × mean;\nonly the stain and the scratch remain")


def overlay(m):
    rgb = np.dstack([np.full((H, W), 0.93)] * 3)
    rgb[m & truth] = [0.16, 0.47, 0.84]
    rgb[m & ~truth] = [0.85, 0.28, 0.28]
    rgb[truth & ~m] = [0.93, 0.64, 0.0]
    return rgb


ax = fig.add_subplot(gs[1, 0]); ax.imshow(overlay(d_raw))
ax.set_title("(d) Fixed threshold on (a)", color=TXT, fontsize=13, fontweight="bold")
ax.set_xlabel(f"false alarms (red) cover {stats['raw_false_alarm_area_pct']} % of the image", color=TXT)
ax.set_xticks([]); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
ax = fig.add_subplot(gs[1, 1]); ax.imshow(overlay(d_corr))
ax.set_title("(e) Same threshold on (c)", color=TXT, fontsize=13, fontweight="bold")
ax.set_xlabel(f"defects found (blue): {stats['corr_defect_recall_pct']:.0f} % of defect pixels;\n"
              f"false alarms: {stats['corr_false_alarm_area_pct']} % of the image", color=TXT)
ax.set_xticks([]); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]

ax = fig.add_subplot(gs[1, 2]); ax.set_facecolor(BG)
row = 380
ax.plot(raw[row], color=GRAY, lw=1, label="captured (a)")
ax.plot(corr[row], color=BLUE, lw=1, label="corrected (c)")
ax.axhline(0.94 * np.median(corr), color=RED, ls="--", lw=1.2, label="threshold on (c)")
ax.annotate("stain", xy=(520, corr[row, 515:525].mean()), xytext=(545, 185),
            color=TXT, arrowprops=dict(arrowstyle="->", color=TXT))
ax.set_ylim(0, 255); ax.set_xlim(0, W)
ax.set_title("(f) Gray values along the row of the stain", color=TXT, fontsize=13, fontweight="bold")
ax.set_xlabel("pixel column", color=TXT); ax.set_ylabel("gray value (8 bit)", color=TXT)
ax.tick_params(colors=TXT, labelsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="lower left")
fig.text(0.5, 0.015, "legend for (d) and (e):   blue = defect found   red = false alarm   amber = defect missed",
         ha="center", color=TXT)
plt.savefig(OUT, dpi=105, facecolor=BG, bbox_inches="tight")
print(json.dumps(stats, indent=1))
