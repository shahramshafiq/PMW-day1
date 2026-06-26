# 3D Reconstruction: Day 1 Experiment Notes

**Shahram Shafiq, AI Track, PMW Internship 2026**

---

## What I was trying to do

Start understanding how photogrammetry and 3D reconstruction actually work, not just the theory, but enough to write real code and make something visible.

---

## Tutorials I went through

1. **Computerphile: "How does 3D Scanning Work?"** - good starting point, explains depth sensors vs photogrammetry, 10 min video. Key takeaway: cameras don't see depth, reconstruction is inferring it from geometry.

2. **Kaggle Learn: Python course** - already completed, but relevant since the reconstruction pipeline I wrote relies on numpy array operations.

3. **Open3D documentation** (open3d.org/docs/release) - read through the point cloud and geometry sections. They have a great tutorial on ICP (Iterative Closest Point) for aligning two point clouds.

4. **YouTube: "Structure from Motion explained"** - anonymous channel but clear explanation. Covers feature extraction, matching, fundamental matrix, triangulation. This explained *why* you need multiple views and what "sparse reconstruction" means.

5. **NeRF paper abstract** (Mildenhall et al., 2020) - read just the abstract and intro. The key idea: a neural network learns the volumetric scene representation implicitly. You don't get a mesh or point cloud, you get a network you can query for any viewpoint.

---

## What I tried (technically)

### Attempt 1: Install Open3D

```bash
pip install open3d
```

**Result:** ImportError on import.

```
ImportError: /lib/x86_64-linux-gnu/libm.so.6: version 'GLIBC_2.29' not found
```

Tried the pre-release build:

```bash
pip install open3d --pre
```

Same error. My Windows Anaconda environment has Python 3.11 but the underlying GLIBC is too old (2.28 vs required 2.29). This is a known issue on some setups.

**Workaround tried:** Found a stackoverflow post suggesting to use the CPU-only build:

```bash
pip install open3d-python
```

That package is discontinued. No luck.

**Honest conclusion:** Open3D didn't work on my setup without upgrading the system libraries, which I didn't want to do mid-internship. I'll try it on Google Colab later where the environment is controlled.

---

### Attempt 2: Use matplotlib for 3D visualization

This worked completely. `matplotlib` + `mpl_toolkits.mplot3d` can render 3D scatter plots fine. The limitation is you can't do real-time rotation or very large point clouds, but for understanding and demonstrating the concepts it's solid.

Wrote `point_cloud_basics.py` which:
- Generates a synthetic building corner as 3D points
- Projects it from 4 camera positions (perspective projection)
- Simulates SfM reconstruction with noise
- Visualizes both the original and reconstructed point cloud
- Outputs PNGs without needing any GUI interaction

**What worked:** Everything ran cleanly. The 2D projections look exactly like what you'd see from camera views. The 3D plots clearly show the difference between the ground truth and the noisy reconstruction.

**What I'd do differently:** The "reconstruction" in my script is just adding noise to known points, it's a simulation, not real SfM. A real pipeline would:
1. Extract SIFT features from actual images
2. Match features across image pairs
3. Compute Essential Matrix and recover pose
4. Triangulate matched keypoints
5. Run bundle adjustment to minimize reprojection error

I understand these steps conceptually but implementing them from scratch is beyond Day 1.

---

### Attempt 3: COLMAP (quick look)

COLMAP is the go-to open-source SfM tool. I downloaded it but didn't have photos to feed it yet. Plan is to use it on Week 3 when we actually capture footage.

---

## What I understand now vs yesterday

**Before:** I knew photogrammetry = making 3D from photos, roughly. Knew NeRF was a neural thing. Gaussian splatting was just a name.

**After:**
- **Photogrammetry:** feature matching + triangulation + bundle adjustment. COLMAP does this.
- **Point cloud:** the output of SfM: a set of (x, y, z) points in 3D space. Sparse at first, dense after MVS.
- **NeRF:** trains a neural network on the images to learn implicit scene representation. Slow train, photorealistic render. Not real-time.
- **3D Gaussian Splatting:** represents scene as 3D Gaussians. Much faster than NeRF. Real-time rendering. Likely what PreserveMy.World is targeting for the "explorable worlds" part.
- **GLIBC compatibility issues are real.** Even simple library installs can fail depending on system config. Colab is more reliable for this kind of thing.

---

## What's next

- Run my script on Colab to confirm it works in a fresh environment
- Get actual photos of something (my room, a building nearby) and run through COLMAP
- Watch the Nerfstudio tutorial on Colab
- Week 3: use our team's actual heritage footage to do a real reconstruction

---

*Day 1 was more setup and reading than building. That's fine. I now have a mental model that will make Week 3's reconstruction work make sense.*
