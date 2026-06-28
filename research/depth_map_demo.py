# depth_map_demo.py
# PMW Internship 2026 - Day 2 - AI Track
# Shahram Shafiq (i242541, FAST NUCES Islamabad)
#
# What this demonstrates:
#   Monocular depth estimation: the idea that a single RGB image can be used
#   to predict the depth of every pixel. Tools like MiDaS and Depth Anything
#   do this with deep learning. Here I simulate the output to show:
#     1. What a depth map looks like
#     2. How to unproject it into a 3D point cloud
#     3. How this compares to what COLMAP produces
#
# This is the FOURTH 3D reconstruction method I researched (after SfM, NeRF, 3DGS).
# Key difference: works from a SINGLE image, no multiple views needed.
# Limitation: depths are relative, not metric (no real scale).
#
# Libraries: numpy, matplotlib (standard)
# Run: python depth_map_demo.py
# Output: depth_output.png

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ─────────────────────────────────────────────────────────────────────────────
# Simulate a depth map of a heritage building scene
# This is what MiDaS would produce from a real photo
# Scene layout:
#   - Sky / far background at depth = 10
#   - Main building wall at depth = 5
#   - Left and right stone pillars at depth = 3 (closer, in front)
#   - Arched doorway opening revealing depth = 8 behind it
# ─────────────────────────────────────────────────────────────────────────────

def make_depth_map(H=120, W=160):
    depth = np.ones((H, W)) * 10.0  # background

    # main building facade
    depth[25:100, 15:145] = 5.0

    # left pillar (stone column, closer to camera)
    depth[25:100, 15:42] = 3.0

    # right pillar
    depth[25:100, 118:145] = 3.0

    # arched doorway opening (semicircular, reveals deeper wall behind)
    arch_cx, arch_cy = W // 2, 80
    arch_rx, arch_ry = 22, 28
    for row in range(H):
        for col in range(W):
            if (col - arch_cx) ** 2 / arch_rx ** 2 + (row - arch_cy) ** 2 / arch_ry ** 2 < 1.0:
                if row >= arch_cy - arch_ry // 2:
                    depth[row, col] = 8.0

    # add small Gaussian noise to simulate real prediction imprecision
    depth += np.random.normal(0, 0.08, depth.shape)
    depth = np.clip(depth, 1.0, 12.0)

    return depth


# ─────────────────────────────────────────────────────────────────────────────
# Unproject depth map to 3D point cloud
# This is the standard "back-projection" step used in all depth-based methods.
# Formula: X = (u - cx) * Z / f,  Y = (v - cy) * Z / f,  Z = depth[v, u]
# ─────────────────────────────────────────────────────────────────────────────

def depth_to_pointcloud(depth_map, focal=80.0, stride=2):
    H, W = depth_map.shape
    cx, cy = W / 2.0, H / 2.0

    rows, cols = np.mgrid[0:H:stride, 0:W:stride]
    z = depth_map[::stride, ::stride].flatten()
    x = (cols.flatten() - cx) * z / focal
    y = (rows.flatten() - cy) * z / focal

    points = np.stack([x, y, z], axis=1)
    return points


# ─────────────────────────────────────────────────────────────────────────────
# Visualize: depth map + histogram + 3D point cloud
# ─────────────────────────────────────────────────────────────────────────────

def visualize(depth, points, out_path='depth_output.png'):
    fig = plt.figure(figsize=(16, 5))

    # Panel 1: depth map as image
    ax1 = fig.add_subplot(131)
    img = ax1.imshow(depth, cmap='plasma', interpolation='nearest')
    ax1.set_title('Simulated Depth Map\n(what MiDaS predicts from 1 photo)', fontsize=9, fontweight='bold')
    ax1.set_xlabel('pixel x')
    ax1.set_ylabel('pixel y')
    plt.colorbar(img, ax=ax1, label='depth (m)')

    # Panel 2: depth histogram shows scene layers clearly
    ax2 = fig.add_subplot(132)
    ax2.hist(depth.flatten(), bins=60, color='steelblue', alpha=0.75, edgecolor='none')
    ax2.set_title('Depth Histogram\n(peaks = distinct scene layers)', fontsize=9, fontweight='bold')
    ax2.set_xlabel('depth value')
    ax2.set_ylabel('pixel count')
    for d, label, color in [(3.0, 'pillars', 'orange'), (5.0, 'facade', 'red'),
                             (8.0, 'arch behind', 'green'), (10.0, 'sky/bg', 'purple')]:
        ax2.axvline(x=d, color=color, linestyle='--', linewidth=1.2, label=f'{label} ({d}m)')
    ax2.legend(fontsize=7)

    # Panel 3: 3D point cloud from back-projection
    ax3 = fig.add_subplot(133, projection='3d')
    sc = ax3.scatter(points[:, 0], points[:, 2], -points[:, 1],
                     c=points[:, 2], cmap='plasma', s=1.5, alpha=0.5)
    ax3.set_title('3D Point Cloud\n(unprojected from depth map)', fontsize=9, fontweight='bold')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z (depth)')
    ax3.set_zlabel('Y')
    plt.colorbar(sc, ax=ax3, label='depth')

    plt.suptitle(
        'Monocular Depth to 3D: Heritage Building Scene\nPMW Day 2 | Shahram Shafiq | AI Track',
        fontsize=11
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close('all')
    print(f"Saved: {out_path}")


def print_stats(depth, points):
    print(f"\n  Depth map size  : {depth.shape[0]} x {depth.shape[1]} pixels")
    print(f"  Depth range     : {depth.min():.2f}m  to  {depth.max():.2f}m")
    print(f"  Total 3D points : {len(points)}")
    print(f"  X range         : {points[:,0].min():.2f}  to  {points[:,0].max():.2f}")
    print(f"  Z (depth) range : {points[:,2].min():.2f}  to  {points[:,2].max():.2f}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(7)

    print("=" * 55)
    print("  Monocular Depth Demo: PMW Day 2")
    print("  Shahram Shafiq | FAST NUCES | AI Track")
    print("=" * 55)

    print("\n[1] Generating synthetic depth map (heritage building)...")
    depth = make_depth_map(120, 160)

    print("\n[2] Unprojecting depth map to 3D point cloud...")
    points = depth_to_pointcloud(depth, focal=80, stride=2)
    print_stats(depth, points)

    print("\n[3] Saving visualization...")
    visualize(depth, points)

    print("\nDone. Output: depth_output.png")
    print("\nReal-world equivalent:")
    print("  pip install transformers torch")
    print("  from transformers import pipeline")
    print("  depth_pipe = pipeline('depth-estimation', model='depth-anything/Depth-Anything-V2-Small-hf')")
    print("  result = depth_pipe('your_heritage_photo.jpg')")
    print("  depth_array = result['depth']  # same format as what this script simulates")
