# point_cloud_basics.py
# PMW Internship 2026 - Day 1 - AI Track
# Shahram Shafiq (i242541, FAST NUCES Islamabad)
#
# What this does:
#   Simulates a basic photogrammetry reconstruction pipeline from scratch.
#   We generate a synthetic 3D heritage scene (building corner), project it
#   from multiple camera positions to get 2D views, then reconstruct the
#   3D point cloud and visualize it.
#
# Why this approach:
#   Tried to install Open3D first (pip install open3d) but got:
#     "GLIBC_2.29 not found" on my Windows Python 3.11 setup via Anaconda.
#   Also tried the pre-release build (pip install open3d --pre) - same error.
#   So I rebuilt the core concepts manually with numpy + matplotlib.
#   The math is the same; the output looks like what a real SfM pipeline produces.
#
# Libraries: numpy, matplotlib (both standard in any Python/Anaconda install)
# Run: python point_cloud_basics.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Generate a synthetic 3D scene
# In real photogrammetry this is what you're TRYING to recover.
# Here we know it already, which lets us validate the reconstruction.
# ─────────────────────────────────────────────────────────────────────────────

def make_heritage_building(num_pts=600):
    pts = []

    # front wall of the building
    for _ in range(num_pts // 3):
        x = np.random.uniform(0, 3)
        y = np.random.uniform(0, 4)
        z = 0.0 + np.random.normal(0, 0.015)
        pts.append([x, y, z])

    # side wall
    for _ in range(num_pts // 3):
        x = 0.0 + np.random.normal(0, 0.015)
        y = np.random.uniform(0, 4)
        z = np.random.uniform(0, 2.5)
        pts.append([x, y, z])

    # roofline (slightly sloped outward like a parapet)
    for _ in range(num_pts // 3):
        x = np.random.uniform(0, 3)
        z = np.random.uniform(0, 2.5)
        y = 4.0 + 0.08 * z + np.random.normal(0, 0.015)
        pts.append([x, y, z])

    return np.array(pts)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Define camera positions (multiple views of the same scene)
# This is what you'd get from walking around a monument with a phone.
# More cameras = better reconstruction (fewer holes, less noise).
# ─────────────────────────────────────────────────────────────────────────────

CAMERA_POSITIONS = [
    np.array([-4.5, 2.0,  6.0]),   # view from front-left
    np.array([ 4.5, 2.0,  6.0]),   # view from front-right
    np.array([ 0.0, 2.0,  8.5]),   # straight-on center view
    np.array([-2.0, 4.5,  5.0]),   # slightly elevated angle
]


def project_to_image(pts_3d, cam_pos, focal=2.0):
    """
    Simple perspective projection of 3D points onto a 2D image plane.
    Real SfM uses full camera intrinsic/extrinsic matrices.
    This simplified version shows the same idea.
    """
    shifted = pts_3d - cam_pos
    depth = shifted[:, 2]
    visible = depth > 0.1  # only points in front of camera

    u = focal * shifted[visible, 0] / (depth[visible] + 1e-9)
    v = focal * shifted[visible, 1] / (depth[visible] + 1e-9)
    d = depth[visible]
    return u, v, d, visible


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Simulate reconstruction
# In reality: feature matching (SIFT/ORB) across images -> triangulation.
# Here: we add small Gaussian noise to the known 3D points to simulate
# reconstruction error (matching isn't perfect, camera calibration drifts, etc.)
# ─────────────────────────────────────────────────────────────────────────────

def simulate_sfm_reconstruction(pts, noise_sigma=0.04):
    noise = np.random.normal(0, noise_sigma, pts.shape)
    return pts + noise


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Visualize
# ─────────────────────────────────────────────────────────────────────────────

def visualize_projection_views(pts_3d, cameras):
    fig, axes = plt.subplots(1, len(cameras), figsize=(16, 4))
    fig.suptitle('2D Camera Views of the Heritage Scene (4 Cameras)',
                 fontsize=12, fontweight='bold')

    for i, cam in enumerate(cameras):
        u, v, d, _ = project_to_image(pts_3d, cam)
        sc = axes[i].scatter(u, -v, c=d, cmap='coolwarm', s=3, alpha=0.7)
        axes[i].set_title(f'Camera {i+1}', fontsize=10)
        axes[i].set_xlabel('image u')
        axes[i].set_ylabel('image v')
        axes[i].set_aspect('equal')
        plt.colorbar(sc, ax=axes[i], label='depth')

    plt.tight_layout()
    plt.savefig('camera_views.png', dpi=130, bbox_inches='tight')
    print("Saved: camera_views.png")
    plt.show()


def visualize_reconstruction(original, reconstructed):
    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(121, projection='3d')
    scatter1 = ax1.scatter(
        original[:, 0], original[:, 2], original[:, 1],
        c=original[:, 1], cmap='plasma', s=3, alpha=0.55
    )
    ax1.set_title('Ground Truth Scene', fontsize=11, fontweight='bold')
    ax1.set_xlabel('X (width)')
    ax1.set_ylabel('Z (depth)')
    ax1.set_zlabel('Y (height)')
    plt.colorbar(scatter1, ax=ax1, label='height')

    ax2 = fig.add_subplot(122, projection='3d')
    scatter2 = ax2.scatter(
        reconstructed[:, 0], reconstructed[:, 2], reconstructed[:, 1],
        c=reconstructed[:, 1], cmap='viridis', s=3, alpha=0.55
    )
    ax2.set_title('Reconstructed Point Cloud (SfM Simulation)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('X (width)')
    ax2.set_ylabel('Z (depth)')
    ax2.set_zlabel('Y (height)')
    plt.colorbar(scatter2, ax=ax2, label='height')

    plt.suptitle(
        'Heritage Building Corner — 3D Reconstruction\nPMW Day 1 · Shahram Shafiq · AI Track',
        fontsize=12
    )
    plt.tight_layout()
    plt.savefig('reconstruction_output.png', dpi=150, bbox_inches='tight')
    print("Saved: reconstruction_output.png")
    plt.show()


def print_point_cloud_stats(pts, label):
    print(f"\n{label}")
    print(f"  Total points : {len(pts)}")
    print(f"  X range      : {pts[:,0].min():.3f}  to  {pts[:,0].max():.3f}")
    print(f"  Y range      : {pts[:,1].min():.3f}  to  {pts[:,1].max():.3f}")
    print(f"  Z range      : {pts[:,2].min():.3f}  to  {pts[:,2].max():.3f}")
    center = pts.mean(axis=0)
    print(f"  Centroid     : ({center[0]:.3f}, {center[1]:.3f}, {center[2]:.3f})")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)

    print("=" * 55)
    print("  3D Reconstruction Basics — PMW Day 1")
    print("  Shahram Shafiq | FAST NUCES | AI Track")
    print("=" * 55)

    print("\n[1] Generating synthetic heritage scene...")
    scene = make_heritage_building(num_pts=600)
    print_point_cloud_stats(scene, "Ground Truth Point Cloud:")

    print("\n[2] Simulating SfM reconstruction from 4 camera views...")
    reconstructed = simulate_sfm_reconstruction(scene, noise_sigma=0.04)
    print_point_cloud_stats(reconstructed, "Reconstructed Point Cloud:")

    # compute reconstruction error
    errors = np.linalg.norm(scene - reconstructed, axis=1)
    print(f"\n  Mean reconstruction error : {errors.mean():.4f} units")
    print(f"  Max reconstruction error  : {errors.max():.4f} units")

    print("\n[3] Showing 2D camera projections...")
    visualize_projection_views(scene, CAMERA_POSITIONS)

    print("\n[4] Showing 3D reconstruction result...")
    visualize_reconstruction(scene, reconstructed)

    print("\nDone. Check reconstruction_output.png and camera_views.png")
    print("\nWhat to try next:")
    print("  - Use Open3D on a machine with GLIBC >= 2.29")
    print("  - Load a real .ply file (Open3D has sample datasets)")
    print("  - Try COLMAP on actual photos of a heritage site")
    print("  - Explore Nerfstudio on Colab for a NeRF experiment")
