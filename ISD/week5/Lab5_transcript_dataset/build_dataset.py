#!/usr/bin/env python3
"""
Lab5 - Transcript Dataset builder
=================================
Render transcript PDFs -> PNG, generate augmented variants that simulate
real-world scan/photo conditions, and emit a manifest linking every image
to its student_id and ground-truth JSON (labeling).

Sources (read-only):
  week3/.../data/input/input      + ground_truth      (group "th")
  week3/.../data/input/input_G    + ground_truth_G    (group "G")

Output: week5/Lab5_transcript_dataset/
  images/original/<group>/<id>.png
  images/augmented/<group>/<id>_aug{1..N}.png
  ground_truth/<group>/Json_<id>_*.json   (copied)
  labels/manifest.csv
"""
import csv
import glob
import os
import re
import shutil

import cv2
import numpy as np
from pdf2image import convert_from_path

# ----------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
WEEK3 = os.path.abspath(os.path.join(HERE, "..", "..", "week3"))
INPUT_ROOT = os.path.join(
    WEEK3, "Lab3_ocr_system", "Lab3_ocr_system", "ocr_system", "data", "input"
)
GT_ROOT = os.path.join(WEEK3, "ground_truth_transcript 2")

GROUPS = {
    "th": (os.path.join(INPUT_ROOT, "input"), os.path.join(GT_ROOT, "ground_truth")),
    "G": (os.path.join(INPUT_ROOT, "input_G"), os.path.join(GT_ROOT, "ground_truth_G")),
}

DPI = 150
VARIANTS = 5  # augmented variants per transcript

OUT = HERE
IMG_ORIG = os.path.join(OUT, "images", "original")
IMG_AUG = os.path.join(OUT, "images", "augmented")
GT_OUT = os.path.join(OUT, "ground_truth")
LABELS = os.path.join(OUT, "labels")


# --- augmentation primitives ------------------------------------------------
def _white_border():
    return (255, 255, 255)


def aug_rotate_bright(img, rng):
    """slight rotation + brightness shift (tilted, brighter scan)"""
    h, w = img.shape[:2]
    angle = rng.uniform(-3, 3)
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), borderValue=_white_border())
    beta = rng.uniform(15, 40)
    return cv2.convertScaleAbs(img, alpha=1.0, beta=beta)


def aug_noise(img, rng):
    """sensor / photocopier grain"""
    noise = rng.normal(0, rng.uniform(8, 18), img.shape).astype(np.float32)
    return np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def aug_blur_contrast(img, rng):
    """out-of-focus + higher contrast"""
    k = rng.choice([3, 5])
    img = cv2.GaussianBlur(img, (k, k), 0)
    alpha = rng.uniform(1.1, 1.4)
    return cv2.convertScaleAbs(img, alpha=alpha, beta=-10)


def aug_perspective(img, rng):
    """camera-angle keystone warp"""
    h, w = img.shape[:2]
    m = 0.04
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    jit = lambda: rng.uniform(-m, m)
    dst = np.float32([
        [w * jit(), h * jit()],
        [w * (1 + jit()), h * jit()],
        [w * (1 + jit()), h * (1 + jit())],
        [w * jit(), h * (1 + jit())],
    ])
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, M, (w, h), borderValue=_white_border())


def aug_jpeg_dark(img, rng):
    """low-quality JPEG re-compression + darker (bad phone photo)"""
    img = cv2.convertScaleAbs(img, alpha=1.0, beta=rng.uniform(-40, -20))
    q = int(rng.uniform(25, 45))
    ok, enc = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, q])
    return cv2.imdecode(enc, cv2.IMREAD_COLOR)


AUGS = [
    ("rotate_bright", aug_rotate_bright),
    ("noise", aug_noise),
    ("blur_contrast", aug_blur_contrast),
    ("perspective", aug_perspective),
    ("jpeg_dark", aug_jpeg_dark),
]


# --- helpers ----------------------------------------------------------------
def index_ground_truth(gt_dir):
    idx = {}
    for f in glob.glob(os.path.join(gt_dir, "Json_*.json")):
        m = re.search(r"Json_(\d+)_", os.path.basename(f))
        if m:
            idx[m.group(1)] = f
    return idx


def render_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=DPI)
    pil = pages[0].convert("RGB")
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def rel(path):
    return os.path.relpath(path, OUT)


# --- main -------------------------------------------------------------------
def main():
    for d in (IMG_ORIG, IMG_AUG, GT_OUT, LABELS):
        os.makedirs(d, exist_ok=True)

    rows = []
    n_orig = n_aug = 0
    for group, (idir, gdir) in GROUPS.items():
        for sub in (IMG_ORIG, IMG_AUG, GT_OUT):
            os.makedirs(os.path.join(sub, group), exist_ok=True)
        gt_idx = index_ground_truth(gdir)

        pdfs = sorted(glob.glob(os.path.join(idir, "*.pdf")))
        for pdf in pdfs:
            sid = os.path.splitext(os.path.basename(pdf))[0]
            gt_src = gt_idx.get(sid)
            gt_rel = ""
            if gt_src:
                gt_dst = os.path.join(GT_OUT, group, os.path.basename(gt_src))
                shutil.copy2(gt_src, gt_dst)
                gt_rel = rel(gt_dst)

            img = render_pdf(pdf)

            # original
            op = os.path.join(IMG_ORIG, group, f"{sid}.png")
            cv2.imwrite(op, img)
            n_orig += 1
            rows.append([rel(op), "original", group, sid, "none",
                         gt_rel, bool(gt_src)])

            # augmented variants (reproducible per image)
            for i in range(VARIANTS):
                name, fn = AUGS[i % len(AUGS)]
                rng = np.random.default_rng(abs(hash((sid, i))) % (2**32))
                out = fn(img.copy(), rng)
                ap = os.path.join(IMG_AUG, group, f"{sid}_aug{i+1}_{name}.png")
                cv2.imwrite(ap, out)
                n_aug += 1
                rows.append([rel(ap), "augmented", group, sid, name,
                             gt_rel, bool(gt_src)])
            print(f"[{group}] {sid}: original + {VARIANTS} variants"
                  f"{'' if gt_src else '  (NO GT)'}")

    manifest = os.path.join(LABELS, "manifest.csv")
    with open(manifest, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["image_path", "split", "group", "student_id",
                    "aug_type", "gt_path", "gt_exists"])
        w.writerows(rows)

    print("\n=== SUMMARY ===")
    print(f"originals : {n_orig}")
    print(f"augmented : {n_aug}")
    print(f"total imgs: {n_orig + n_aug}")
    print(f"manifest  : {rel(manifest)} ({len(rows)} rows)")
    missing = sum(1 for r in rows if not r[6])
    if missing:
        print(f"NOTE: {missing} rows have no ground truth (gt_exists=False)")


if __name__ == "__main__":
    main()
