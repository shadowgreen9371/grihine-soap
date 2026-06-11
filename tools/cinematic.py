#!/usr/bin/env python3
"""
Grihine Soap — cinematic photo processor.

Gives any new product photo the same dark, color-graded, vignetted look as
the rest of the site so the catalogue always reads as one cohesive set.

Usage:
    python3 tools/cinematic.py SRC.jpg images/output-name.jpg --mode studio
    python3 tools/cinematic.py SRC.jpg images/output-name.jpg --mode env

Modes:
    studio  — subject sits on a saturated, solid-colour backdrop (velvet,
              coloured cloth). The backdrop is matted out and replaced with a
              warm near-black studio gradient. Best for "soap + box on cloth".
    grape   — special matte for the grape-cluster-on-rope shot (keeps the jute
              rope + dark berries, drops everything else to black).
    env     — real-world background kept but darkened at the edges with a
              strong vignette + luminance pull. Best for batch trays, gift
              boxes on wood, workshop shots.

Needs: pip install pillow numpy   (already used elsewhere in this project)

After running, update the <img width/height> attributes if the aspect
changed, then `git add images/ && git commit && git push` to deploy.
"""
import argparse
import colorsys

import numpy as np
from PIL import Image, ImageFilter


def velvet_matte(arr):
    h, w, _ = arr.shape
    c = 44
    p = np.concatenate([arr[:c, :c].reshape(-1, 3), arr[:c, -c:].reshape(-1, 3),
                        arr[-c:, :c].reshape(-1, 3), arr[-c:, -c:].reshape(-1, 3)])
    bg = np.median(p, 0)
    bh, _, _ = colorsys.rgb_to_hsv(*(bg / 255))
    r, g, b = arr[..., 0] / 255, arr[..., 1] / 255, arr[..., 2] / 255
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    df = np.maximum(mx - mn, 1e-6)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    hue = np.zeros_like(mx)
    i = (mx == r); hue[i] = ((g[i] - b[i]) / df[i]) % 6
    i = (mx == g); hue[i] = ((b[i] - r[i]) / df[i]) + 2
    i = (mx == b); hue[i] = ((r[i] - g[i]) / df[i]) + 4
    hue /= 6.0
    hd = np.minimum(np.abs(hue - bh), 1 - np.abs(hue - bh))
    fg = np.clip(np.maximum(1 - np.clip((s - 0.30) / 0.22, 0, 1),
                            np.clip((hd - 0.11) / 0.07, 0, 1)), 0, 1)
    fg = fg * fg * (3 - 2 * fg)
    return np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32) / 255


def grape_matte(arr):
    x = arr / 255.0
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    L = 0.299 * r + 0.587 * g + 0.114 * b
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    s = (mx - mn) / np.maximum(mx, 1e-6)
    berry = np.clip((0.50 - L) / 0.34, 0, 1) * np.clip(((b - r) + 0.10) / 0.16, 0, 1)
    rope = np.clip(((r - b) - 0.06) / 0.12, 0, 1) * np.clip((s - 0.22) / 0.16, 0, 1)
    subj = np.clip(np.maximum(berry, rope), 0, 1)
    si = Image.fromarray((subj * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))
    subj = np.asarray(si).astype(np.float32) / 255
    subj = np.clip((subj - 0.25) / 0.4, 0, 1)
    subj = subj * subj * (3 - 2 * subj)
    return np.asarray(Image.fromarray((subj * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255


def backdrop(h, w, ctr=(46, 42, 35), edge=(13, 12, 10), cy=0.48):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rad = np.clip(np.sqrt(((xx - w / 2) / (w * 0.62)) ** 2 + ((yy - h * cy) / (h * 0.62)) ** 2), 0, 1)
    return (np.array(ctr)[None, None] * (1 - rad[..., None]) + np.array(edge)[None, None] * rad[..., None])


def lum_darken(arr, amt=0.5, knee=0.5):
    x = arr / 255.0
    L = 0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2]
    bgp = np.clip((L - knee) / 0.28, 0, 1)
    bgp = np.asarray(Image.fromarray((bgp * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    dark = x * 0.22
    return (x * (1 - bgp[..., None] * amt) + dark * (bgp[..., None] * amt)) * 255


def cinematic(arr, vig=0.30, cap=1900):
    x = arr / 255.0
    x = np.clip((x - 0.5) * 1.10 + 0.5, 0, 1)
    lum = (0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2])[..., None]
    sh, hi = (1 - lum), lum
    x[..., 0] += (-0.015 * sh + 0.032 * hi)[..., 0]
    x[..., 1] += (0.012 * sh + 0.012 * hi)[..., 0]
    x[..., 2] += (0.024 * sh - 0.032 * hi)[..., 0]
    x = np.clip(x, 0, 1)
    g = (0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2])[..., None]
    x = np.clip(g + (x - g) * 1.12, 0, 1)
    h, w, _ = x.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rad = np.sqrt(((xx - w / 2) / (w * 0.72)) ** 2 + ((yy - h * 0.5) / (h * 0.72)) ** 2)
    x *= (1 - np.clip(rad, 0, 1) ** 2.1 * vig)[..., None]
    im = Image.fromarray((x * 255).clip(0, 255).astype(np.uint8))
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(8))).astype(np.float32) / 255
    x = 1 - (1 - x) * (1 - blur * 0.15)
    x = np.clip(x + np.random.normal(0, 0.011, x.shape), 0, 1)
    out = Image.fromarray((x * 255).clip(0, 255).astype(np.uint8))
    out = out.resize((w * 2, h * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 70, 2))
    if max(out.size) > cap:
        sc = cap / max(out.size)
        out = out.resize((int(out.width * sc), int(out.height * sc)), Image.LANCZOS)
    return out


def main():
    ap = argparse.ArgumentParser(description="Apply Grihine dark-cinematic look to a photo.")
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--mode", choices=["studio", "grape", "env"], default="studio")
    ap.add_argument("--vig", type=float, default=None, help="vignette strength override (0-0.5)")
    ap.add_argument("--quality", type=int, default=84)
    args = ap.parse_args()

    arr = np.asarray(Image.open(args.src).convert("RGB")).astype(np.float32)
    h, w, _ = arr.shape
    if args.mode == "studio":
        m = velvet_matte(arr)[..., None]
        arr = arr * m + backdrop(h, w) * (1 - m)
        vig = args.vig if args.vig is not None else 0.24
    elif args.mode == "grape":
        m = grape_matte(arr)[..., None]
        arr = arr * m + backdrop(h, w, cy=0.52) * (1 - m)
        vig = args.vig if args.vig is not None else 0.24
    else:  # env
        arr = lum_darken(arr, amt=0.45, knee=0.5)
        vig = args.vig if args.vig is not None else 0.42

    out = cinematic(arr, vig=vig)
    out.save(args.dst, "JPEG", quality=args.quality, optimize=True)
    print(f"wrote {args.dst}  {out.size}  ({len(open(args.dst, 'rb').read()) // 1024} KB)")


if __name__ == "__main__":
    main()
