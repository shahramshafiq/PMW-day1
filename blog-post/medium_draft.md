# I Spent a Day Learning 3D Reconstruction — Here's What Actually Stuck

*Posted as part of my Day 1 work for the PreserveMy.World x TechRealm Internship 2026*

---

I'm a CS student at FAST NUCES Islamabad. I build AI agents, write C++ without STL, and once wrote a Mario clone in 7,700 lines of x86 Assembly. But I had never seriously touched 3D reconstruction before this week.

I joined the PreserveMy.World x TechRealm Internship on the AI-Based 3D Reconstruction track. The mission of PreserveMy.World is to document and preserve cultural heritage — mosques, forts, old city streets — by turning phone footage into explorable 3D digital memories. My job, eventually, is to contribute to the AI pipeline that makes that work.

Day 1 task: learn what 3D reconstruction actually is, write some code, and explain it.

---

## The core problem

A camera takes a 2D photo. You want to know the 3D structure of what was photographed. The problem is that this is fundamentally under-constrained — a flat wall and a curved wall can produce exactly the same photo if you position the camera just right.

The solution is more cameras. Specifically, taking photos of the same object from different angles and combining the information.

This is called **Structure from Motion (SfM)**, and it's the backbone of most photogrammetry pipelines.

---

## How photogrammetry actually works (simplified)

Here's the pipeline from photos to 3D:

**Step 1 — Feature extraction**
Run a feature detector (SIFT, ORB) on every image. These find distinctive points — corners, edges, texture patterns — that are likely to appear in other photos of the same scene.

**Step 2 — Feature matching**
Find which feature points in Image A correspond to the same physical point in Image B. This is the hardest part in practice — false matches ruin everything downstream.

**Step 3 — Camera pose estimation**
From matched features, compute where each camera was when it took the photo. This uses the Essential Matrix (for calibrated cameras) or Fundamental Matrix (uncalibrated).

**Step 4 — Triangulation**
With known camera positions, a matched point in two images defines two rays in 3D space. Where those rays intersect (or come closest) is the 3D location of that point. Do this for thousands of matched points and you get a **sparse point cloud**.

**Step 5 — Dense reconstruction (MVS)**
The sparse point cloud has gaps. Multi-View Stereo fills them in by computing depth for every pixel, not just feature points. Now you have millions of 3D points.

**Step 6 — Mesh / surface reconstruction**
Connect the points into a continuous surface (Poisson surface reconstruction, Delaunay, etc.). Now you have an actual 3D model you can view in any 3D viewer.

The standard open-source tool for steps 1-5 is **COLMAP**.

---

## What I coded

I couldn't get Open3D working on my machine (GLIBC version mismatch — a known issue on some Anaconda setups). So I implemented the core concepts from scratch with numpy and matplotlib.

My script (`point_cloud_basics.py`) does this:

1. Generates a synthetic 3D scene — a heritage building corner with a front wall, side wall, and roofline
2. Projects it to 2D from 4 different "camera" positions (perspective projection)
3. Simulates reconstruction by adding noise (representing real-world imprecision in feature matching)
4. Visualizes both the ground truth and the reconstructed point cloud side by side

Here's the projection function:

```python
def project_to_image(pts_3d, cam_pos, focal=2.0):
    shifted = pts_3d - cam_pos
    depth = shifted[:, 2]
    visible = depth > 0.1

    u = focal * shifted[visible, 0] / (depth[visible] + 1e-9)
    v = focal * shifted[visible, 1] / (depth[visible] + 1e-9)
    return u, v, depth[visible], visible
```

This is basic perspective projection — divide x and y by depth, scale by focal length. Real cameras are more complicated (lens distortion, sensor size, principal point) but the geometry is the same.

Running it gives two PNGs: the 4 camera views and the 3D reconstruction comparison.

Is it real SfM? No. The "reconstruction" is simulated. But the math — projection, depth, point clouds — is real, and I understand it now in a way I didn't this morning.

---

## NeRF and Gaussian Splatting — what's the difference?

Photogrammetry gives you an explicit 3D model (point cloud, mesh). NeRF and Gaussian Splatting are different approaches that have become more popular recently.

**NeRF (Neural Radiance Field):** Train a small neural network to represent the scene. You give it (x, y, z, viewing direction) and it outputs (color, density). To render a new view, you shoot rays through the scene and query the network for each point along the ray. It's slow to train (hours) and slow to render without tricks, but the quality is incredible.

**3D Gaussian Splatting:** Represent the scene as millions of tiny 3D Gaussian blobs, each with its own color, opacity, and orientation. During training (which is faster than NeRF), you optimize the positions and properties of these Gaussians to match the input photos. Rendering is very fast — real-time on a decent GPU. This is likely closer to what PreserveMy.World is targeting for the "explorable worlds" side of the product.

---

## Why this matters for heritage

Pakistan has hundreds of heritage sites that are either underdocumented, physically deteriorating, or difficult to access. Lahore Fort, Mohenjo-daro, the old city lanes of Walled Lahore. A 3D reconstruction built from a few hours of phone video could preserve a site forever as a navigable digital memory.

That's PreserveMy.World's mission. And it's genuinely interesting to work on.

My contribution right now is learning the pipeline well enough to be useful during Week 3, when our team will actually capture footage and run it through reconstruction tools. I don't want to be the person who just hands off footage without understanding what happens to it.

---

## Honest reflection

Day 1 was heavier on reading than on building. I hit library install issues, had to pivot my code plan, and my "reconstruction" is still a simulation rather than a real SfM output.

But I now have a working mental model: cameras project 3D to 2D, matching features across views lets you triangulate back, NeRF learns it implicitly, Gaussian Splatting approximates it with blobs. Next step is running COLMAP on actual photos and seeing the real pipeline in action.

---

*Shahram Shafiq — FAST NUCES Islamabad — PreserveMy.World x TechRealm Internship, AI Track*
*GitHub: [github.com/shahramshafiq](https://github.com/shahramshafiq)*
