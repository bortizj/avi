"""
Simulated examples for step (3) Image enhancement and pre-processing
of the AVI course document (bortizj/avi).

Generates Figures 18-22 in ./assets and prints every number quoted in the text.
Requires: numpy, scipy, opencv-python, scikit-image, matplotlib.
Run: python preprocessing_figures.py
"""
import os
import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.spatial import cKDTree

rng = np.random.default_rng(7)
OUT = "assets"
os.makedirs(OUT, exist_ok=True)

INK = "#0b0b0b"
INK2 = "#52514e"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9, "text.color": INK,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": "#c3c2b7", "figure.facecolor": "white",
})


def show(ax, img, title, vmin=0, vmax=255, cmap="gray"):
    ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_title(title, loc="left")
    ax.set_xticks([]); ax.set_yticks([])


# ---------------------------------------------------------------------------
# Figure 18 - noise reduction: frame averaging and spatial filters
# ---------------------------------------------------------------------------
def fig18():
    H, W = 200, 300
    yy, xx = np.mgrid[0:H, 0:W]
    # brushed-metal-like surface: mild horizontal streaks around 130 gray values
    streak = ndimage.gaussian_filter1d(rng.normal(0, 1, (H, W)), 25, axis=1)
    clean = 130 + 2.0 * streak / streak.std()
    # thin scratch (about 1.5 px wide), 12 gray values darker
    d = np.abs((yy - 0.25 * xx) - 60) / np.sqrt(1 + 0.25 ** 2)
    scratch = np.clip(1.5 - d, 0, 1)
    scratch_mask = d < 0.75
    clean -= 12 * scratch
    # small pit, radius 3 px, 25 gray values darker
    pit_mask = (yy - 140) ** 2 + (xx - 220) ** 2 <= 9
    clean[pit_mask] -= 25

    hot = rng.random(clean.shape) < 0.001  # 0.1 % hot pixels, fixed on the sensor

    def capture():
        # signal-dependent (shot) plus signal-independent (read) noise
        var = 0.5 * clean + 9.0
        img = clean + rng.normal(0, 1, clean.shape) * np.sqrt(var)
        img[hot] = 255
        return np.clip(img, 0, 255), hot

    frame, hot = capture()
    frames = [frame] + [capture()[0] for _ in range(7)]
    avg8 = np.mean(frames, axis=0)

    f8 = frame.astype(np.float32)
    gauss = cv2.GaussianBlur(f8, (0, 0), 1.5)
    median = cv2.medianBlur(frame.astype(np.uint8), 3).astype(float)
    bilat = cv2.bilateralFilter(f8, 7, 25, 3)
    nlm = cv2.fastNlMeansDenoising(frame.astype(np.uint8), None, h=10,
                                   templateWindowSize=7, searchWindowSize=21).astype(float)

    # evaluation masks
    band = (d > 4) & (d < 10)                      # background next to scratch
    flat = (~scratch_mask) & (d > 10) & ~ndimage.binary_dilation(pit_mask, iterations=8)
    results = {}
    for name, img in [("single frame", frame), ("average of 8 frames", avg8),
                      ("Gaussian, sigma 1.5 px", gauss), ("median 3x3", median),
                      ("bilateral", bilat), ("non-local means", nlm)]:
        resid = (img - clean)[flat & ~ndimage.binary_dilation(hot, iterations=3)]
        noise = resid.std()
        contrast = img[band].mean() - img[scratch_mask].mean()
        cnr = contrast / noise
        # bright false alarms: blobs brighter than background + 40 gray values
        bright = img > 170
        nblobs = ndimage.label(bright)[1]
        results[name] = (contrast, noise, cnr, nblobs)
    print("\nFigure 18 - scratch contrast / residual noise / CNR / bright blobs")
    for k, v in results.items():
        print(f"  {k:24s} C={v[0]:5.1f}  sigma={v[1]:4.1f}  CNR={v[2]:4.2f}  blobs={v[3]}")

    fig, axs = plt.subplots(2, 3, figsize=(10, 4.9))
    titles = ["(a) single frame", "(b) average of 8 frames", "(c) Gaussian, σ = 1.5 px",
              "(d) median 3 × 3", "(e) bilateral", "(f) non-local means"]
    for ax, img, t, key in zip(axs.flat, [frame, avg8, gauss, median, bilat, nlm], titles,
                               results.keys()):
        r = results[key]
        show(ax, img[20:180, 20:280], f"{t}\nCNR {r[2]:.1f}, bright blobs {r[3]}", 80, 170)
    fig.tight_layout()
    fig.savefig(f"{OUT}/preprocessing-denoising.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 19 - contrast enhancement and background normalization
# ---------------------------------------------------------------------------
def fig19():
    H, W = 220, 320
    yy, xx = np.mgrid[0:H, 0:W]
    # curved part: shading from the geometry, not removable by flat-field correction
    shade = 60 + 140 * np.cos((xx - 230) / 210 * np.pi / 2) ** 2
    refl = np.ones((H, W))
    stain = ((yy - 110) ** 2 / 26 ** 2 + (xx - 70) ** 2 / 34 ** 2) <= 1
    refl[stain] *= 0.90                         # faint stain, 10 % darker
    dd = np.abs(yy - (0.6 * xx + 20))
    scr = (dd < 1.0) & (xx > 180) & (xx < 300)
    refl[scr] *= 0.85                           # thin scratch, 15 % darker

    def make(extra_dark=False):
        r = refl.copy()
        if extra_dark:                          # large dark label on a second, good part
            lab = (yy > 20) & (yy < 70) & (xx > 120) & (xx < 220)
            r[lab] = 0.15
        img = shade * r + rng.normal(0, 2.0, (H, W))
        return np.clip(img, 0, 255).astype(np.uint8)

    img = make()
    he = cv2.equalizeHist(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(img)
    # background estimate with a large median filter, then division (flat background = 128)
    bg = cv2.medianBlur(img, 121).astype(float)
    bg = cv2.GaussianBlur(bg, (0, 0), 5)
    norm = np.clip(128 * img.astype(float) / np.maximum(bg, 1), 0, 255)

    good = ~ndimage.binary_dilation(stain | scr, iterations=6)
    ring = ndimage.binary_dilation(stain, iterations=12) & ~ndimage.binary_dilation(stain, iterations=4)

    def stats(x):
        x = x.astype(float)
        c_stain = x[ring].mean() - x[stain].mean()
        p1, p99 = np.percentile(x[good], [1, 99])
        return c_stain, p99 - p1

    print("\nFigure 19 - stain contrast (gray values) / spread of good surface (p99 - p1)")
    out = {}
    for name, x in [("captured", img), ("global HE", he), ("CLAHE", clahe),
                    ("background division", norm)]:
        out[name] = stats(x)
        print(f"  {name:20s} stain contrast={out[name][0]:5.1f}   good spread={out[name][1]:6.1f}")

    # one fixed threshold: dark if more than 6 % below the flat level (128 -> 120.3)
    thr = 128 * 0.94
    det = norm < thr
    tp_stain = det[stain].mean(); tp_scr = det[scr].mean(); fa = det[good].mean()
    print(f"  fixed threshold on normalized image: stain {tp_stain:.0%}, scratch {tp_scr:.0%}, "
          f"false alarms {fa:.2%} of good area")
    left = good & (xx < 107); right = good & (xx >= 107)
    print(f"  false alarms: dark left third {det[left].mean():.2%}, rest {det[right].mean():.2%}; "
          f"shade left {shade[:, :107].mean():.0f}, rest {shade[:, 107:].mean():.0f}")
    detm = 128 * cv2.medianBlur(img, 3).astype(float) / np.maximum(bg, 1) < thr
    print(f"  with 3x3 median first: stain {detm[stain].mean():.0%}, scratch {detm[scr].mean():.0%}, "
          f"false alarms {detm[good].mean():.2%}")

    # instability of global HE: same good patch on two parts
    img2 = make(extra_dark=True)
    he2 = cv2.equalizeHist(img2)
    patch = (slice(150, 200), slice(240, 300))
    shift_he = he2[patch].astype(float).mean() - he[patch].astype(float).mean()
    bg2 = cv2.GaussianBlur(cv2.medianBlur(img2, 121).astype(float), (0, 0), 5)
    norm2 = np.clip(128 * img2.astype(float) / np.maximum(bg2, 1), 0, 255)
    shift_norm = norm2[patch].mean() - norm[patch].mean()
    print(f"  same good patch, part with dark label vs without: HE shift {shift_he:+.1f}, "
          f"background division shift {shift_norm:+.1f} gray values")

    fig, axs = plt.subplots(1, 5, figsize=(12.5, 2.0))
    show(axs[0], img, "(a) captured")
    show(axs[1], he, "(b) global histogram eq.")
    show(axs[2], clahe, "(c) CLAHE")
    show(axs[3], norm, "(d) background division", 90, 150)
    show(axs[4], det.astype(float), "(e) fixed threshold on (d)", 0, 1)
    fig.tight_layout()
    fig.savefig(f"{OUT}/preprocessing-contrast.png", dpi=150)
    plt.close(fig)
    return shift_he, shift_norm


# ---------------------------------------------------------------------------
# Figure 20 - periodic texture removal in the Fourier domain (fabric)
# ---------------------------------------------------------------------------
def fig20():
    H, W = 256, 256
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    weave = 120 + 30 * np.sin(2 * np.pi * xx / 8) * np.sin(2 * np.pi * yy / 6) \
        + 12 * np.sin(2 * np.pi * xx / 8)
    img = weave.copy()
    # defect: slub (thick yarn) - a short bright elongated blob
    slub = ((yy - 150) ** 2 / 3.0 ** 2 + (xx - 90) ** 2 / 14 ** 2) <= 1
    img[slub] += 22
    # defect: small hole, darker
    hole = (yy - 70) ** 2 + (xx - 180) ** 2 <= 16
    img[hole] -= 25
    img += rng.normal(0, 4, img.shape)

    F = np.fft.fftshift(np.fft.fft2(img - img.mean()))
    mag = np.log1p(np.abs(F))
    # notch: zero the strongest spectral peaks (periodic texture), keep low frequencies
    cy, cx = H // 2, W // 2
    r = np.hypot(yy - cy, xx - cx)
    peaks = (np.abs(F) > 0.05 * np.abs(F).max()) & (r > 6)
    notch = ~ndimage.binary_dilation(peaks, iterations=2)
    filt = np.real(np.fft.ifft2(np.fft.ifftshift(F * notch))) + img.mean()

    defect = slub | hole
    inner = np.zeros((H, W), bool); inner[8:-8, 8:-8] = True   # FFT wrap-around affects borders
    good = ~ndimage.binary_dilation(defect, iterations=6) & inner

    def cnr(x, m):
        return abs(x[m].mean() - x[good].mean()) / x[good].std()
    print("\nFigure 20 - CNR (defect vs good fabric) before / after notch filter")
    print(f"  slub: {cnr(img, slub):.2f} -> {cnr(filt, slub):.2f};  hole: {cnr(img, hole):.2f} -> {cnr(filt, hole):.2f}")
    print(f"  spectral peaks removed: {ndimage.label(peaks)[1]}")
    z = (filt - filt[good].mean()) / filt[good].std()
    det = np.abs(z) > 3.5
    print(f"  |z|>3.5: slub {det[slub].mean():.0%}, hole {det[hole].mean():.0%}, false alarms {det[good].mean():.2%}")

    fig, axs = plt.subplots(1, 4, figsize=(11, 3.1))
    show(axs[0], img, "(a) captured fabric", 40, 200)
    show(axs[1], mag, "(b) Fourier magnitude (log)", mag.min(), mag.max())
    axs[1].contour(~notch, levels=[0.5], colors=[ORANGE], linewidths=0.8)
    show(axs[2], filt, "(c) after notch filter", filt[good].mean() - 30, filt[good].mean() + 30)
    show(axs[3], (det & inner).astype(float), "(d) |z| > 3.5 on (c), 8 px border excluded", 0, 1)
    fig.tight_layout()
    fig.savefig(f"{OUT}/preprocessing-texture.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 21 - image alignment before golden-template comparison
# ---------------------------------------------------------------------------
def fig21():
    H, W = 240, 320
    ref = np.full((H, W), 60, np.uint8)
    # PCB-like pattern: pads and traces
    for i in range(6):
        cv2.rectangle(ref, (30 + 45 * i, 40), (52 + 45 * i, 70), 200, -1)
        cv2.rectangle(ref, (30 + 45 * i, 170), (52 + 45 * i, 200), 200, -1)
        cv2.line(ref, (41 + 45 * i, 70), (41 + 45 * i, 170), 170, 4)
    cv2.circle(ref, (160, 120), 18, 210, -1)
    ref = cv2.GaussianBlur(ref, (0, 0), 1.0)

    test = ref.copy()
    cv2.line(test, (52 + 45 * 2, 55), (30 + 45 * 3, 55), 200, 4)   # solder bridge between pads
    cv2.circle(test, (250, 120), 3, 60, -1)                          # nothing
    test[100:106, 35:47] = 60                                        # open trace (missing copper)
    # misplacement: shift and rotation of the board, plus gain change and noise
    tx, ty, ang = 2.6, -1.8, 0.4
    M = cv2.getRotationMatrix2D((W / 2, H / 2), ang, 1.0)
    M[:, 2] += (tx, ty)
    test = cv2.warpAffine(test, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    test = np.clip(1.1 * test.astype(float) + 5 + rng.normal(0, 3, test.shape), 0, 255).astype(np.uint8)

    def diff_mask(a, b):
        # normalize gain and offset before comparing (zero mean, unit variance)
        a = (a - a.mean()) / a.std(); b = (b - b.mean()) / b.std()
        return np.abs(a - b) > 0.8

    d0 = diff_mask(test.astype(float), ref.astype(float))
    warp = np.eye(2, 3, dtype=np.float32)
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    _, warp = cv2.findTransformECC(ref.astype(np.float32), test.astype(np.float32), warp,
                                   cv2.MOTION_EUCLIDEAN, crit, None, 5)
    aligned = cv2.warpAffine(test, warp, (W, H), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_REPLICATE)
    d1 = diff_mask(aligned.astype(float), ref.astype(float))
    d1[:6, :] = d1[-6:, :] = False; d1[:, :6] = d1[:, -6:] = False
    d0[:6, :] = d0[-6:, :] = False; d0[:, :6] = d0[:, -6:] = False
    d1o = cv2.morphologyEx(d1.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)).astype(bool)
    d0o = cv2.morphologyEx(d0.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)).astype(bool)
    true = np.zeros((H, W), bool)
    true[50:61, 50 + 45 * 2:32 + 45 * 3] = True
    true[98:108, 33:49] = True
    true = cv2.warpAffine(true.astype(np.uint8), M, (W, H)) > 0
    true_al = cv2.warpAffine(true.astype(np.uint8), warp, (W, H), flags=cv2.WARP_INVERSE_MAP) > 0
    est_ang = -np.degrees(np.arctan2(warp[1, 0], warp[0, 0]))  # same sign convention as getRotationMatrix2D
    print("\nFigure 21 - ECC alignment")
    print(f"  true: rotation {ang} deg, shift ({tx}, {ty}) px about the image center")
    print(f"  estimated rotation {est_ang:.3f} deg")
    # check residual: map test-image points back and compare with reference points
    pts = np.array([[40, 40], [280, 40], [40, 200], [280, 200]], float)
    fwd = (M[:, :2] @ pts.T).T + M[:, 2]
    back = (warp[:, :2] @ fwd.T).T + warp[:, 2]
    # WARP_INVERSE_MAP: aligned(x) = test(warp x); so warp maps ref coords to test coords
    fwd_est = (warp[:, :2] @ pts.T).T + warp[:, 2]
    err = np.linalg.norm(fwd_est - fwd, axis=1)
    print(f"  max registration error at board corners: {err.max():.3f} px")
    lbl0 = ndimage.label(d0o)[1]; lbl1 = ndimage.label(d1o)[1]
    fp0 = (d0o & ~ndimage.binary_dilation(true, iterations=3)).sum()
    fp1 = (d1o & ~ndimage.binary_dilation(true_al, iterations=3)).sum()
    print(f"  difference blobs: {lbl0} before -> {lbl1} after alignment;"
          f" false difference pixels {fp0} -> {fp1}")

    fig, axs = plt.subplots(1, 4, figsize=(11.5, 2.9))
    show(axs[0], ref, "(a) golden template")
    show(axs[1], test, "(b) test board")
    show(axs[2], d0o.astype(float), f"(c) difference, no alignment\n{lbl0} blobs", 0, 1)
    show(axs[3], d1o.astype(float), f"(d) difference after ECC\n{lbl1} blobs", 0, 1)
    fig.tight_layout()
    fig.savefig(f"{OUT}/preprocessing-alignment.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 22 - point-cloud filtering
# ---------------------------------------------------------------------------
def sor(pts, k=20, std_ratio=2.0):
    tree = cKDTree(pts)
    dist, _ = tree.query(pts, k=k + 1)
    md = dist[:, 1:].mean(1)
    return md < md.mean() + std_ratio * md.std()


def voxel_down(pts, size):
    keys = np.floor((pts - pts.min(0)) / size).astype(np.int64)   # grid anchored at the min bound
    _, inv, cnt = np.unique(keys, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    out = np.zeros((cnt.size, 3))
    np.add.at(out, inv, pts)
    return out / cnt[:, None]


def fig22():
    # laser-scanned flat plate 60 x 40 mm, 0.1 mm point spacing, with a dent 0.10 mm deep
    xs = np.arange(0, 60, 0.1); ys = np.arange(0, 40, 0.1)
    X, Y = np.meshgrid(xs, ys)
    dent = -0.10 * np.exp(-(((X - 40) ** 2 + (Y - 20) ** 2) / (2 * 1.5 ** 2)))
    Z = dent + rng.normal(0, 0.02, X.shape)
    pts = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    n_in = len(pts)
    # outliers: isolated spikes (reflections) and a cluster of mixed points near one edge
    n_sp = 1500
    sp = np.c_[rng.uniform(0, 60, n_sp), rng.uniform(0, 40, n_sp), rng.normal(0, 1.5, n_sp)]
    sp[:, 2] += np.sign(sp[:, 2]) * 0.3
    n_ed = 800
    ed = np.c_[rng.uniform(0, 60, n_ed), rng.uniform(-0.6, 0.0, n_ed), rng.uniform(-2.0, 0.0, n_ed)]
    allp = np.r_[pts, sp, ed]
    is_out = np.r_[np.zeros(n_in, bool), np.ones(n_sp + n_ed, bool)]

    keep = sor(allp, k=20, std_ratio=2.0)
    removed_out = (~keep & is_out).sum() / is_out.sum()
    removed_in = (~keep & ~is_out).sum() / (~is_out).sum()
    clean = allp[keep]
    print("\nFigure 22 - point cloud")
    print(f"  points: {len(allp)} ({is_out.sum()} outliers)")
    print(f"  SOR k=20, 2 std: removed {removed_out:.1%} of outliers and {removed_in:.2%} of surface points")
    remaining_out = (keep & is_out).sum()
    print(f"  outliers remaining: {remaining_out}")
    # pass-through (crop) filter: keep the part's volume of interest only
    box = (clean[:, 1] >= 0) & (clean[:, 1] <= 40) & (np.abs(clean[:, 2]) <= 1.0)
    keep2 = keep.copy(); keep2[np.flatnonzero(keep)[~box]] = False
    print(f"  crop box: removes {(~box).sum()} more points; outliers left {(keep2 & is_out).sum()}, "
          f"surface points lost {(~keep2 & ~is_out).sum()}")
    clean = clean[box]
    # second pass: radius outlier removal after voxel downsampling
    vox = voxel_down(clean, 0.3)
    # surface-aware filter: distance of each point to a plane fitted to its 16 neighbours
    tree = cKDTree(vox)
    _, idx = tree.query(vox, k=17)
    nb = vox[idx[:, 1:]]
    c = nb.mean(1)
    cov = np.einsum("nki,nkj->nij", nb - c[:, None], nb - c[:, None])
    normal = np.linalg.eigh(cov)[1][:, :, 0]
    res = np.abs(np.einsum("ni,ni->n", vox - c, normal))
    lim = 6 * 1.4826 * np.median(res)
    vox2 = vox[res < lim]
    print(f"  voxel 0.3 mm: {len(clean)} -> {len(vox)} points ({len(vox)/len(clean):.1%})")
    print(f"  remaining outliers (|z| > 0.2 mm) before / after plane-residual filter: "
          f"{(np.abs(vox[:, 2]) > 0.2).sum()} / {(np.abs(vox2[:, 2]) > 0.2).sum()}; "
          f"points removed {len(vox) - len(vox2)}; limit {lim*1000:.0f} um")
    flat = np.hypot(vox2[:, 0] - 40, vox2[:, 1] - 20) > 6
    rms_raw = Z[np.hypot(X - 40, Y - 20) > 6].std()
    zf = vox2[flat, 2]
    rms_vox = 1.4826 * np.median(np.abs(zf - np.median(zf)))   # robust (MAD) estimate
    near = np.hypot(vox2[:, 0] - 40, vox2[:, 1] - 20) < 0.3
    depth_vox = vox2[near, 2].mean()
    raw_near = np.hypot(X - 40, Y - 20) < 0.3
    print(f"  surface noise RMS {rms_raw*1000:.1f} um -> {rms_vox*1000:.1f} um after voxel averaging (robust MAD estimate)")
    print(f"  dent depth at center: raw mean {Z[raw_near].mean()*1000:.0f} um, voxel {depth_vox*1000:.0f} um (true 100)")
    # effect of the voxel size on the dent alone (noise-free surface, deepest voxel)
    clean_surf = np.c_[X.ravel(), Y.ravel(), dent.ravel()]
    for size in (0.3, 1.5, 3.0):
        v = voxel_down(clean_surf, size)
        print(f"  noise-free dent depth with {size} mm voxels: {-v[:, 2].min()*1000:.1f} um (true 100)")
    print(f"  surface points removed by SOR: {(~keep & ~is_out).sum()}")

    fig, axs = plt.subplots(1, 4, figsize=(12.5, 3.0), gridspec_kw={"width_ratios": [1.25, 1.25, 1, 1]})
    sel = rng.random(len(allp)) < 0.08
    m = sel & ~is_out
    axs[0].scatter(allp[m, 0], allp[m, 2], s=0.5, c=INK2, lw=0, rasterized=True)
    axs[0].scatter(allp[is_out, 0], allp[is_out, 2], s=3, c=ORANGE, lw=0, rasterized=True)
    axs[0].set_title("(a) raw, side view (outliers in orange)", loc="left")
    axs[0].set_xlabel("x (mm)"); axs[0].set_ylabel("z (mm)"); axs[0].set_ylim(-5, 5)
    sel2 = rng.random(len(clean)) < 0.08
    axs[1].scatter(clean[sel2, 0], clean[sel2, 2], s=0.5, c=INK2, lw=0, rasterized=True)
    ko = keep & is_out
    axs[1].scatter(allp[ko, 0], allp[ko, 2], s=3, c=ORANGE, lw=0, rasterized=True)
    axs[1].set_title("(b) after statistical outlier removal", loc="left")
    axs[1].set_xlabel("x (mm)"); axs[1].set_ylim(-5, 5)
    for ax in axs[:2]:
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
    zoom = (X > 32) & (X < 48) & (Y > 12) & (Y < 28)
    im = axs[2].imshow(Z[120:281, 320:481] * 1000, cmap="RdBu", vmin=-120, vmax=120,
                       extent=[32, 48, 28, 12])
    axs[2].set_title("(c) raw height (µm)", loc="left"); axs[2].set_xticks([]); axs[2].set_yticks([])
    zz = vox2[(vox2[:, 0] > 32) & (vox2[:, 0] < 48) & (vox2[:, 1] > 12) & (vox2[:, 1] < 28)]
    axs[3].scatter(zz[:, 0], zz[:, 1], c=zz[:, 2] * 1000, cmap="RdBu", vmin=-120, vmax=120, s=3.5,
                   marker="s", lw=0)
    axs[3].set_xlim(32, 48); axs[3].set_ylim(28, 12); axs[3].set_aspect("equal")
    axs[3].set_title("(d) after crop, 0.3 mm voxels and\nplane-residual filter (µm)", loc="left")
    axs[3].set_xticks([]); axs[3].set_yticks([])
    fig.subplots_adjust(left=0.05, right=0.92, bottom=0.17, top=0.88, wspace=0.28)
    cax = fig.add_axes([0.935, 0.2, 0.01, 0.65])
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    fig.savefig(f"{OUT}/preprocessing-pointcloud.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig18()
    fig19()
    fig20()
    fig21()
    fig22()
