"""Shared plot style for the figures of section (4) Region of interest and object detection."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Inter is used when it is installed; otherwise matplotlib falls back to DejaVu Sans.
plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#BDBDB5", "axes.labelcolor": "#555555",
    "xtick.color": "#555555", "ytick.color": "#555555",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 11, "axes.titlelocation": "left",
    "savefig.dpi": 150, "figure.dpi": 100,
})
ORANGE = "#E8602C"; DARK = "#4A4A4A"; BLUE = "#2F6DB5"; GREEN = "#3A9A5B"; GRAY = "#9A9A92"
PALETTE = [ORANGE, BLUE, GREEN, "#8E5CC4", "#C9A227", "#2BA3A3", "#C0507A", "#6B8E23"]


def img_ax(ax):
    """Image axes without ticks and with a light frame."""
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True); s.set_color("#BDBDB5")
