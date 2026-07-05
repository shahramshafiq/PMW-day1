"""
ML Visualizations, AR Lines & Capture-to-3D
PMW Internship 2026, AI-Based 3D Reconstruction Track, Week 2 Day 4

One real photo goes through three stages: ML feature/edge visualization,
an AR-style line overlay, and a heuristic capture-to-3D point cloud.
Source photo: footage-research/images/01-front-facade.jpg, the Badshahi
Mosque front facade photo already sourced and verified for the
"Source, Curate & Write About Footage" submission.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PHOTO = os.path.join(SCRIPT_DIR, '..', 'footage-research', 'images', '01-front-facade.jpg')
OUT_DIR = os.path.join(SCRIPT_DIR, 'output')

photo_bgr = cv2.imread(SOURCE_PHOTO)
photo_rgb = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2GRAY)
img_h, img_w = gray.shape
print(f"Loaded source photo: {img_w}x{img_h}")

# ---------------------------------------------------------------
# Stage 1: ML visualizations (edge gradients + corner features)
# ---------------------------------------------------------------
print("\n[1] ML visualizations: Sobel gradients + Harris corners")

sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
grad_mag = np.sqrt(sobel_x**2 + sobel_y**2)
grad_mag_norm = (grad_mag / grad_mag.max() * 255).astype(np.uint8)

corner_response = cv2.cornerHarris(gray.astype(np.float32), blockSize=3, ksize=3, k=0.04)
corner_response = cv2.dilate(corner_response, None)
corner_thresh = 0.01 * corner_response.max()
corner_ys, corner_xs = np.where(corner_response > corner_thresh)
print(f"    Gradient magnitude range: {grad_mag.min():.1f} to {grad_mag.max():.1f}")
print(f"    Harris corners detected (above threshold): {len(corner_xs)} pixels")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(photo_rgb)
axes[0].set_title('Original: Badshahi Mosque front facade', fontsize=10, fontweight='bold')
axes[0].axis('off')

axes[1].imshow(grad_mag_norm, cmap='inferno')
axes[1].set_title('Sobel gradient magnitude (ML feature map)', fontsize=10, fontweight='bold')
axes[1].axis('off')

axes[2].imshow(photo_rgb)
axes[2].scatter(corner_xs[::4], corner_ys[::4], s=2, c='cyan', alpha=0.6)
axes[2].set_title(f'Harris corner features ({len(corner_xs)} px, subsampled)', fontsize=10, fontweight='bold')
axes[2].axis('off')

plt.suptitle('Stage 1: ML Visualization, the same feature types SfM/COLMAP match across photos', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, '01_ml_visualization.png'), dpi=130, bbox_inches='tight')
plt.close('all')
print("    Saved: output/01_ml_visualization.png")

# ---------------------------------------------------------------
# Stage 2: AR line overlay
# ---------------------------------------------------------------
print("\n[2] AR line overlay: Hough line detection on top of the real photo")

edges_for_hough = cv2.Canny(gray, 60, 150)
lines = cv2.HoughLinesP(edges_for_hough, rho=1, theta=np.pi / 180, threshold=60,
                         minLineLength=40, maxLineGap=8)
print(f"    Hough line segments detected: {0 if lines is None else len(lines)}")

ar_frame = photo_rgb.copy()
if lines is not None:
    for x1, y1, x2, y2 in lines.reshape(-1, 4):
        cv2.line(ar_frame, (x1, y1), (x2, y2), (57, 255, 20), 2)

symmetry_x = img_w // 2
cv2.line(ar_frame, (symmetry_x, 0), (symmetry_x, img_h), (255, 60, 60), 1, cv2.LINE_AA)

fig, ax = plt.subplots(figsize=(8, 5.3))
ax.imshow(ar_frame)
ax.axis('off')
ax.set_title('Stage 2: AR line overlay (structural edges an AR heritage app\nwould lock onto, plus facade symmetry axis)', fontsize=10, fontweight='bold')

label_boxstyle = dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.65, edgecolor='none')
ax.annotate('Facade symmetry axis', xy=(symmetry_x, 20), xytext=(symmetry_x + 15, 20),
            color='white', fontsize=8, bbox=label_boxstyle)
ax.annotate('Detected structural edges\n(arches, minarets, dome lines)', xy=(20, img_h - 20),
            xytext=(20, img_h - 15), color='white', fontsize=8, bbox=label_boxstyle, va='top')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, '02_ar_line_overlay.png'), dpi=130, bbox_inches='tight')
plt.close('all')
print("    Saved: output/02_ar_line_overlay.png")

# ---------------------------------------------------------------
# Stage 3: Capture-to-3D view
# ---------------------------------------------------------------
print("\n[3] Capture-to-3D: heuristic monocular depth, back-projected to a colored point cloud")

# Honest, simple heuristic (not a trained depth network like MiDaS).
# First problem to solve: the sky has no physical surface, so it must be
# masked out before back-projecting, otherwise it gets treated as a giant
# distant "wall" and warps the whole point cloud into a curtain shape.
# Sky mask: bright, low-saturation pixels (measured on this photo: sky
# averages saturation ~38 and brightness ~210, versus ~113 and ~178 for
# the building), confirmed by sampling the top and bottom strips directly.
hsv = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2HSV)
saturation = hsv[:, :, 1].astype(np.float32)
brightness = hsv[:, :, 2].astype(np.float32)
sky_mask = (saturation < 70) & (brightness > 180)
print(f"    Sky pixels masked out: {sky_mask.sum()} of {img_h * img_w} ({100 * sky_mask.sum() / (img_h * img_w):.1f}%)")

# For the remaining (building/ground) pixels: lower in frame = nearer camera,
# and locally strong edges are pulled slightly forward, giving domes and
# minarets a bit of relief instead of a flat backdrop.
row_norm = np.linspace(0, 1, img_h).reshape(-1, 1)
row_norm = np.repeat(row_norm, img_w, axis=1)
edge_strength = grad_mag / grad_mag.max()
depth_heuristic = 5.0 - 2.0 * row_norm - 0.6 * edge_strength
depth_heuristic = np.clip(depth_heuristic, 2.0, 5.0)
depth_heuristic[sky_mask] = np.nan

step = 3
ys, xs = np.mgrid[0:img_h:step, 0:img_w:step]
depths = depth_heuristic[0:img_h:step, 0:img_w:step]
colors_full = photo_rgb[0:img_h:step, 0:img_w:step].reshape(-1, 3) / 255.0

valid = ~np.isnan(depths.ravel())
ys, xs, depths = ys.ravel()[valid], xs.ravel()[valid], depths.ravel()[valid]
colors = colors_full[valid]

focal = 400.0
cx, cy = img_w / 2.0, img_h / 2.0
x3d = (xs - cx) * depths / focal
y3d = -(ys - cy) * depths / focal
z3d = depths

pts3d = np.column_stack([x3d.ravel(), y3d.ravel(), z3d.ravel()])
print(f"    Point cloud size: {pts3d.shape[0]} points")
print(f"    Depth range: {z3d.min():.2f} to {z3d.max():.2f} (relative units, not metric)")

fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(pts3d[:, 0], pts3d[:, 2], pts3d[:, 1], c=colors, s=3)
ax1.set_title('Front view', fontsize=9, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Z (depth)')
ax1.set_zlabel('Y (height)')
ax1.view_init(elev=10, azim=-90)

ax2 = fig.add_subplot(132, projection='3d')
ax2.scatter(pts3d[:, 0], pts3d[:, 2], pts3d[:, 1], c=colors, s=3)
ax2.set_title('Three-quarter view', fontsize=9, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('Z (depth)')
ax2.set_zlabel('Y (height)')
ax2.view_init(elev=15, azim=-60)

ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(pts3d[:, 0], pts3d[:, 2], pts3d[:, 1], c=colors, s=3)
ax3.set_title('Side view (depth revealed)', fontsize=9, fontweight='bold')
ax3.set_xlabel('X')
ax3.set_ylabel('Z (depth)')
ax3.set_zlabel('Y (height)')
ax3.view_init(elev=5, azim=-5)

plt.suptitle('Stage 3: Capture-to-3D, colored point cloud back-projected from the real photo', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, '03_capture_to_3d.png'), dpi=130, bbox_inches='tight')
plt.close('all')
print("    Saved: output/03_capture_to_3d.png")

print("\nDone. All 3 stages saved to output/:")
print("  01_ml_visualization.png")
print("  02_ar_line_overlay.png")
print("  03_capture_to_3d.png")
