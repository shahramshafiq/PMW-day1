"""
Convert curated footage into a 3D reconstruction (.ply)
PMW Internship 2026, AI-Based 3D Reconstruction Track, Week 3, Day 1

Real multi-view Structure from Motion was tested and ruled out first
(see sfm_feasibility_test.py, only 12-17 RANSAC-verified inliers per
photo pair, not enough for real triangulation). This script instead
builds a monocular heuristic reconstruction, the same approach validated
in ml-viz-ar-capture3d/, extended here to export a real, valid .ply
point cloud file rather than just a matplotlib image.

Source photo: the Jaulian Buddhist monastery ruins at Taxila, already
sourced and verified for the ML/AR/capture-to-3D module.
"""

import numpy as np
import cv2
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PHOTO = os.path.join(SCRIPT_DIR, '..', 'ml-viz-ar-capture3d', 'source', 'jaulian-monastery-taxila.jpg')
OUT_DIR = os.path.join(SCRIPT_DIR, 'output')

photo_bgr = cv2.imread(SOURCE_PHOTO)
photo_rgb = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2GRAY)
img_h, img_w = gray.shape
print(f"Loaded source photo: {img_w}x{img_h}")

sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
grad_mag = np.sqrt(sobel_x**2 + sobel_y**2)

# Same sky/haze mask validated in ml-viz-ar-capture3d: this photo is
# sunset-lit, so brightness (not saturation) is what separates the far
# background (sky + hazy hills) from the shadowed foreground stonework.
hsv = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2HSV)
brightness = hsv[:, :, 2].astype(np.float32)
sky_mask = brightness > 205
print(f"Sky/haze pixels masked out: {sky_mask.sum()} of {img_h * img_w} ({100 * sky_mask.sum() / (img_h * img_w):.1f}%)")

row_norm = np.linspace(0, 1, img_h).reshape(-1, 1)
row_norm = np.repeat(row_norm, img_w, axis=1)
edge_strength = grad_mag / grad_mag.max()
depth_heuristic = 5.0 - 2.0 * row_norm - 0.6 * edge_strength
depth_heuristic = np.clip(depth_heuristic, 2.0, 5.0)
depth_heuristic[sky_mask] = np.nan

step = 2
ys, xs = np.mgrid[0:img_h:step, 0:img_w:step]
depths = depth_heuristic[0:img_h:step, 0:img_w:step]
colors_full = photo_rgb[0:img_h:step, 0:img_w:step].reshape(-1, 3)

valid = ~np.isnan(depths.ravel())
ys, xs, depths = ys.ravel()[valid], xs.ravel()[valid], depths.ravel()[valid]
colors = colors_full[valid]

focal = 400.0
cx, cy = img_w / 2.0, img_h / 2.0
x3d = (xs - cx) * depths / focal
y3d = -(ys - cy) * depths / focal
z3d = depths

num_points = len(x3d)
print(f"Point cloud size: {num_points} points")
print(f"Depth range: {z3d.min():.2f} to {z3d.max():.2f} (relative units, not metric)")


def write_ply(path, x, y, z, rgb, comment_lines):
    """Write a standard ASCII PLY point cloud, built by hand against the
    format spec rather than pulled from a library, so every field in the
    header is something I can actually explain."""
    n = len(x)
    with open(path, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        for line in comment_lines:
            f.write(f"comment {line}\n")
        f.write(f"element vertex {n}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for i in range(n):
            r, g, b = rgb[i]
            f.write(f"{x[i]:.4f} {y[i]:.4f} {z[i]:.4f} {int(r)} {int(g)} {int(b)}\n")


ply_path = os.path.join(OUT_DIR, 'jaulian_monastery_taxila.ply')
write_ply(
    ply_path, x3d, y3d, z3d, colors,
    comment_lines=[
        "Jaulian Buddhist monastery ruins, Taxila",
        "PMW Internship 2026, AI-Based 3D Reconstruction Track",
        "Monocular heuristic reconstruction (not multi-view SfM), see README for method and limitations",
    ]
)
print(f"Saved: {os.path.relpath(ply_path, SCRIPT_DIR)}")

file_size_kb = os.path.getsize(ply_path) / 1024
print(f"File size: {file_size_kb:.1f} KB")
