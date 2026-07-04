# 3D Reconstruction Methods: Research for PreserveMy.World

**Shahram Shafiq, AI Track, PMW Internship 2026 (Day 2)**

---

## Why this comparison matters

PreserveMy.World needs to turn raw phone footage of heritage sites into navigable 3D digital records. There are multiple ways to do this technically. Before Week 3 when we actually reconstruct something, I need to know which method does what, what it costs, and which one fits the PMW workflow.

---

## Methods Covered

1. COLMAP (Structure from Motion + Multi-View Stereo)
2. NeRF (Neural Radiance Fields)
3. 3D Gaussian Splatting (3DGS)
4. Monocular Depth Estimation (MiDaS / Depth Anything)

---

## Comparison Table

| Method | Inputs needed | Output | Min hardware | Training time | Render speed | PMW fit |
|---|---|---|---|---|---|---|
| COLMAP | 50+ overlapping photos or video frames | Sparse point cloud, then dense mesh | CPU (slow) or GPU | Hours | N/A (offline) | Main pipeline for raw reconstruction |
| NeRF | 20-200 calibrated images with camera poses | Photorealistic novel view images, implicit model | GPU (RTX 2080+) | 4-12 hours | 30s per frame | High-quality archival renders, not real-time |
| 3D Gaussian Splatting | Same as NeRF (calibrated images + poses) | Explicit Gaussian blob scene, real-time renderer | GPU (RTX 3060+) | 20-45 min | Real-time (100+ FPS) | Best for the explorable worlds feature |
| Monocular Depth (MiDaS) | Single RGB image or video | Per-frame depth map, relative depths | CPU or GPU | None (inference only) | Real-time | Preprocessing step, fast rough scan |

---

## Detailed Notes

### 1. COLMAP

**What it does:** Classic photogrammetry pipeline. Step 1 (SfM): extracts feature points from all images, matches them across pairs, triangulates 3D positions of matched points, estimates where every camera was. Outputs a sparse point cloud. Step 2 (MVS): for every pixel in every image, compute depth by comparing patches across neighboring images. Outputs a dense point cloud with millions of points.

**Inputs:** A folder of overlapping images (or video frames extracted at ~1fps). Images need to overlap by at least 60%. The more angles the better.

**Outputs:**
- `sparse/` folder: camera positions + sparse point cloud (.ply)
- `dense/` folder: fused dense point cloud (.ply)
- Can be converted to mesh using Meshlab or Open3D

**Hardware:** Runs on CPU (slow, hours for a big scene) or NVIDIA GPU (faster). No special GPU required.

**Difficulty:** Medium. Installing COLMAP is straightforward. Running it requires understanding the pipeline steps but the GUI helps a lot.

**Where it fits PMW:** This is step 1 of almost every serious reconstruction pipeline. NeRF and 3DGS both often use COLMAP outputs (camera poses) as input. PMW likely runs COLMAP on the captured footage as the foundation.

**My attempt:** Downloaded COLMAP but haven't run it on real footage yet. Plan for Week 3.

---

### 2. NeRF (Neural Radiance Field)

**What it does:** Trains a small MLP (Multi-Layer Perceptron) to learn the scene as a continuous volumetric function. You give it a 3D position (x, y, z) and a viewing direction, and it predicts the color and density at that point. To render a new view, you shoot a ray from the virtual camera through the scene, sample points along the ray, query the network, and composite the result.

**Inputs:** 20 to 200 calibrated images (meaning: you know the camera intrinsics and the exact position/orientation of each camera). Camera poses are usually estimated by running COLMAP first.

**Outputs:** A trained network that can render the scene from any viewpoint. Not a mesh or point cloud. Cannot be easily exported to standard 3D formats.

**Hardware:** Needs a decent GPU. Original NeRF takes 1-2 days to train. Instant-NGP (NVIDIA's fast version) reduces this to minutes.

**Difficulty:** Hard for a beginner. Setting up the environment, getting correct camera poses, understanding the rendering pipeline takes time.

**Where it fits PMW:** Good for creating high-quality photorealistic archival images of a heritage site. Not suitable for real-time walkthroughs because rendering is slow per-frame.

**Tools to try:** Nerfstudio (has a Colab notebook, beginner friendly), Instant-NGP (fast but needs CUDA setup).

---

### 3. 3D Gaussian Splatting (3DGS)

**What it does:** Represents the entire scene as millions of tiny 3D Gaussian blobs (called "splats"). Each splat has a position, size, orientation, color, and opacity. During training (which starts from COLMAP's sparse point cloud), the optimizer adjusts these splats to match the input images. Rendering works by projecting the Gaussians onto the image plane and blending them by depth, which is extremely fast on a GPU.

**Inputs:** Same as NeRF: calibrated images + camera poses (from COLMAP). Also uses COLMAP's sparse point cloud as initialization.

**Outputs:** A `.ply` file with millions of Gaussians. Can be rendered in real-time using the official viewer or web-based viewers (three.js-based).

**Hardware:** GPU required. RTX 3060 or better recommended. Training takes 20-45 minutes typically.

**Difficulty:** Medium. The official codebase is well-maintained. Colab versions exist. The trickiest part is getting good COLMAP poses.

**Where it fits PMW:** This is the most direct fit for the "explorable worlds" product. Real-time rendering means users can actually navigate the reconstructed heritage site in a browser or app. PMW's platform likely uses 3DGS or a derivative of it for the final walkable output.

**Tools to try:** Official gaussian-splatting repo (github.com/graphdeco-inria/gaussian-splatting), Luma AI (cloud-based, no setup needed), Polycam (mobile app that does 3DGS on-device).

---

### 4. Monocular Depth Estimation (MiDaS / Depth Anything)

**What it does:** Uses a deep learning model trained on millions of images to predict the relative depth of every pixel in a single image. No multiple views required. The output is a depth map: a grayscale image where brighter = closer to camera.

**Inputs:** A single RGB image or a video (processed frame by frame).

**Outputs:** A depth map (same resolution as input). Can be "unprojected" to a point cloud using the camera's focal length.

**Limitations:** Depths are relative, not absolute. Scale is unknown without calibration. Good for understanding scene structure, not for precise measurements.

**Hardware:** Runs on CPU (slow but works) or GPU (real-time on decent GPU).

**Difficulty:** Easy. `pip install transformers` and run 5 lines of Python.

**Where it fits PMW:** Useful for quick scans where you only have a single photo of a site. Also useful as a preprocessing step to estimate camera motion. Cannot replace COLMAP or 3DGS for full reconstruction but fills the gap when multi-view data is unavailable.

**My code:** See `depth_map_demo.py` in this folder. I simulated what MiDaS outputs and showed how to convert it to a 3D point cloud.

---

## Summary: Which method for which situation at PMW?

| Situation | Best method |
|---|---|
| Have 50+ overlapping photos, want a mesh | COLMAP |
| Want a photorealistic archival render from novel views | NeRF (Nerfstudio) |
| Want a real-time walkable 3D scene for the website | 3D Gaussian Splatting |
| Only have one photo, want a rough depth sense | Monocular depth (MiDaS) |
| Full production pipeline | COLMAP first, then 3DGS on top |

---

## Sources and resources

- COLMAP documentation: colmap.github.io
- NeRF original paper: arxiv.org/abs/2003.08934
- 3DGS paper: arxiv.org/abs/2308.04079
- Nerfstudio (beginner NeRF tool): docs.nerf.studio
- MiDaS GitHub: github.com/isl-org/MiDaS
- Depth Anything v2: github.com/DepthAnything/Depth-Anything-V2
- Computerphile "How does 3D Scanning Work?" (YouTube)
- Computerphile "Neural Radiance Fields" (YouTube)
