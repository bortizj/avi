"""Figure 25 of 05_object_detection.md (roi-learned-segmentation.png).

Otsu threshold versus a learned pixel classifier (random forest on a filter bank) for parts on a
woven conveyor belt, including the drop in performance on a belt that was not in the training data.

Run:  python fig25_roi_learned_segmentation.py
Output: roi-learned-segmentation.png in the current folder; the numbers quoted in the text are printed to the console.
"""
import numpy as np, cv2, time
from scipy import ndimage as ndi
from sklearn.ensemble import RandomForestClassifier
from style import *
H, W = 240, 360
yy, xx = np.mgrid[0:H, 0:W]

def belt(rng, kind):
    if kind == "A":   # woven belt, medium gray
        per, mean, amp = rng.uniform(7, 9), 115, 28
    else:             # new belt: finer weave, darker
        per, mean, amp = rng.uniform(4, 5), 85, 22
    th = rng.uniform(-0.2, 0.2)
    u = xx * np.cos(th) + yy * np.sin(th); v = -xx * np.sin(th) + yy * np.cos(th)
    t = mean + amp * np.sign(np.sin(2 * np.pi * u / per)) * np.sin(2 * np.pi * v / (2 * per)) ** 2
    return t + rng.normal(0, 6, (H, W))

def scene(rng, kind="A"):
    img = belt(rng, kind); gt = np.zeros((H, W), np.uint8)
    for _ in range(rng.integers(3, 6)):
        m = np.zeros((H, W), np.uint8)
        cx, cy = rng.integers(40, W - 40), rng.integers(40, H - 40)
        if rng.random() < 0.5:
            cv2.ellipse(m, (int(cx), int(cy)), (int(rng.integers(18, 40)), int(rng.integers(14, 32))), float(rng.uniform(0, 180)), 0, 360, 1, -1)
        else:
            cv2.fillPoly(m, [cv2.boxPoints(((float(cx), float(cy)), (float(rng.integers(30, 80)), float(rng.integers(20, 50))), float(rng.uniform(0, 180)))).astype(np.int32)], 1)
        tone = rng.choice([rng.uniform(35, 65), rng.uniform(105, 125), rng.uniform(175, 215)])
        part = tone + rng.normal(0, 4, (H, W))
        img = np.where(m > 0, part, img); gt |= m
    # illumination gradient and a soft highlight
    g = 0.75 + 0.45 * (xx / W) * rng.uniform(0.6, 1.0) + 0.1 * (yy / H)
    hl = 50 * np.exp(-(((xx - rng.uniform(0, W)) ** 2 + (yy - rng.uniform(0, H)) ** 2) / (2 * 35 ** 2)))
    img = img * g + hl
    img = cv2.GaussianBlur(img, (0, 0), 0.7)
    return np.clip(img, 0, 255).astype(np.uint8), gt

def features(img):
    f = img.astype(np.float32); out = [f]
    for s in (1, 2, 4, 8):
        gs = ndi.gaussian_filter(f, s)
        out += [gs, ndi.gaussian_gradient_magnitude(f, s), ndi.gaussian_laplace(f, s)]
        mu = ndi.uniform_filter(f, 2 * s + 1); mu2 = ndi.uniform_filter(f * f, 2 * s + 1)
        out.append(np.sqrt(np.maximum(mu2 - mu * mu, 0)))
    return np.stack(out, -1)

def iou(a, b): return (a & b).sum() / max((a | b).sum(), 1)
def objects(pred, gt, min_area=150):
    nl, lab = cv2.connectedComponents(pred.astype(np.uint8))
    ng, gl = cv2.connectedComponents(gt.astype(np.uint8))
    preds = [lab == i for i in range(1, nl) if (lab == i).sum() >= min_area]
    gts = [gl == i for i in range(1, ng)]
    found = sum(any(iou(p, g) > 0.5 for p in preds) for g in gts)
    false = sum(not any(iou(p, g) > 0.5 for g in gts) for p in preds)
    return found, len(gts), false

rng = np.random.default_rng(11)
train = [scene(rng, "A") for _ in range(25)]
testA = [scene(rng, "A") for _ in range(40)]
testB = [scene(rng, "B") for _ in range(40)]
trainB = [scene(rng, "B") for _ in range(5)]

def fit(data, n_per=6000):
    X, y = [], []
    for im, gt in data:
        F = features(im).reshape(-1, 17); g = gt.ravel()
        idx = rng.choice(len(g), n_per, replace=False)
        X.append(F[idx]); y.append(g[idx])
    clf = RandomForestClassifier(n_estimators=60, max_depth=18, n_jobs=-1, random_state=0)
    clf.fit(np.concatenate(X), np.concatenate(y)); return clf

def predict(clf, im):
    p = clf.predict_proba(features(im).reshape(-1, 17))[:, 1].reshape(H, W)
    p = cv2.morphologyEx((p > 0.5).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return p > 0

def otsu(im):
    t, bw = cv2.threshold(cv2.GaussianBlur(im, (0, 0), 2), 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    a = bw > 0
    return a if a.mean() < 0.5 else ~a
def evaluate(fn, data):
    ious = []; f = n = fp = 0
    for im, gt in data:
        p = fn(im); ious.append(iou(p, gt > 0)); a, b, c = objects(p, gt > 0); f += a; n += b; fp += c
    return np.mean(ious), f, n, fp

t0 = time.time(); clf = fit(train); print("train s", time.time() - t0)
rA = evaluate(otsu, testA); print("otsu A", rA)
rB0 = evaluate(otsu, testB); print("otsu B", rB0)
lA = evaluate(lambda im: predict(clf, im), testA); print("rf A", lA)
lB = evaluate(lambda im: predict(clf, im), testB); print("rf B", lB)
clf2 = fit(train + trainB)
lB2 = evaluate(lambda im: predict(clf2, im), testB); print("rf+5 B", lB2)
lA2 = evaluate(lambda im: predict(clf2, im), testA); print("rf+5 A", lA2)

imA, gA = testA[0]; imB, gB = testB[0]
def show(ax, im, pred, gt, title):
    img_ax(ax); ax.imshow(im, cmap="gray", vmin=0, vmax=255)
    ov = np.zeros((H, W, 4))
    ov[pred & gt] = matplotlib.colors.to_rgba(GREEN, 0.5)
    ov[pred & ~gt] = matplotlib.colors.to_rgba(ORANGE, 0.7)
    ov[~pred & gt] = matplotlib.colors.to_rgba(BLUE, 0.6)
    ax.imshow(ov); ax.set_title(title)
fig, axs = plt.subplots(1, 4, figsize=(16, 3.4))
img_ax(axs[0]); axs[0].imshow(imA, cmap="gray", vmin=0, vmax=255); axs[0].set_title("(a) parts on a woven belt")
show(axs[1], imA, otsu(imA), gA > 0, "(b) Otsu threshold\nIoU %.2f on 40 test images" % rA[0])
show(axs[2], imA, predict(clf, imA), gA > 0, "(c) learned pixel classifier\nIoU %.2f on 40 test images" % lA[0])
show(axs[3], imB, predict(clf, imB), gB > 0, "(d) same classifier, new belt\nIoU %.2f on 40 test images" % lB[0])
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=GREEN, alpha=0.6, label="correct part pixels"), Patch(color=ORANGE, alpha=0.8, label="false part pixels"), Patch(color=BLUE, alpha=0.7, label="missed part pixels")],
           loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.06))
plt.tight_layout()
plt.savefig("roi-learned-segmentation.png", bbox_inches="tight", facecolor="white")
