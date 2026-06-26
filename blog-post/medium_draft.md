# what i learned on day 1 of a 3D reconstruction internship

*Day 1 post, PreserveMy.World x TechRealm Internship 2026*

---

I'm a CS student at FAST NUCES Islamabad. I've built multi-agent AI pipelines, written C++ without touching STL once, and spent a full semester writing a Mario clone in x86 Assembly (7,700 lines, no regrets). But 3D reconstruction? Never touched it before this week.

I joined PreserveMy.World x TechRealm on the AI-Based 3D Reconstruction track. PMW builds navigable 3D digital records of heritage sites from phone footage. My track is the AI pipeline that turns raw video into something you can actually walk through on a screen.

Day 1: figure out what photogrammetry actually is, write real code, don't just paraphrase a Wikipedia article.

---

## the core problem

A camera gives you a flat 2D image. You want the 3D shape of whatever's in it. The problem is there's no unique answer to that question. A flat wall and a slightly curved wall can look identical in a photo if the angle is right.

The fix is more photos from different positions. Enough views of the same scene and the geometry across them pins down where things actually are in 3D. This is Structure from Motion (SfM). It's what most photogrammetry pipelines are built on.

---

## the pipeline

Most tools (COLMAP is the standard open-source one) follow roughly this:

1. Run a feature detector (SIFT, ORB) on every image to find keypoints: corners, edges, distinctive patches.
2. Match those keypoints across image pairs. Figure out which point in image A is the same physical point as something in image B. This is where the whole thing breaks if it's going to break.
3. From matched keypoints, estimate where each camera was positioned. This uses the Essential Matrix for calibrated cameras.
4. Two matched points in two images define two rays in 3D space. Where they intersect is the real-world location of that point. Do this for thousands of pairs and you get a sparse point cloud.
5. Multi-View Stereo fills in the gaps. Instead of just feature points, it computes depth for every pixel. Now you have millions of points.
6. Poisson surface reconstruction (or similar) connects the dots into an actual mesh.

---

## what I built

Open3D didn't install cleanly on my machine. GLIBC version mismatch, which is apparently a known issue on certain Anaconda setups on Windows. Tried the pre-release build. Same error. Spent maybe 40 minutes on this before switching to just implementing the core ideas with numpy and matplotlib.

My script generates a synthetic building corner (front wall, side wall, roofline), projects it from 4 camera positions using perspective projection, adds Gaussian noise to simulate the imprecision you'd get from real feature matching, and plots original vs reconstructed point cloud side by side.

The projection step:

```python
def project_to_image(pts_3d, cam_pos, focal=2.0):
    shifted = pts_3d - cam_pos
    depth = shifted[:, 2]
    visible = depth > 0.1
    u = focal * shifted[visible, 0] / (depth[visible] + 1e-9)
    v = focal * shifted[visible, 1] / (depth[visible] + 1e-9)
    return u, v, depth[visible], visible
```

Basic perspective projection: divide x and y by depth, scale by focal length. Real cameras have lens distortion and principal point offsets on top of this, but the core geometry is the same.

Is it real SfM? No. The "reconstruction" is just noisy copies of points I already knew. But the projection math is real, the depth reasoning is real, and I get what a point cloud actually represents now in a way I didn't this morning.

---

## NeRF and 3D Gaussian Splatting

Photogrammetry gives you an explicit model: a point cloud or a mesh. NeRF and 3DGS take a completely different angle.

NeRF trains a small neural network on your images. Input is a 3D position plus a viewing direction. Output is color and density at that point. Rendering a new viewpoint means shooting rays through the scene and querying the network along each ray. The results are photorealistic but training takes hours and rendering is slow unless you add a lot of tricks.

3D Gaussian Splatting represents the scene as a huge number of 3D Gaussian blobs, each with its own color, opacity, and shape. You optimize these blobs against your input images. Training is faster than NeRF and rendering is real-time on a decent GPU. This is probably what PMW uses for the "explorable worlds" part, since people actually need to walk through these reconstructions in real time.

---

## why i'm doing this

Pakistan has a lot of heritage sites that most people will never visit, some that are actively falling apart, and a few that barely anyone has documented properly. Lahore Fort is famous. The old city lanes of Walled Lahore are not. Mohenjo-daro has been eroding for decades.

PMW's approach is: capture footage with a phone, run it through a reconstruction pipeline, get something navigable and permanent. I want to understand the full pipeline I'm contributing to, not just collect footage and hand it off.

---

## where I'm at after day 1

More reading than building. Hit an install wall, pivoted to manual implementation, got visible output out of Python.

What I have now: a working mental model of SfM, a clear picture of where NeRF and 3DGS fit in, and actual runnable code. What I don't have yet: a real reconstruction from real images.

Next up is COLMAP on actual photos. Week 3 is when our team captures real footage of a heritage site and runs it through the pipeline for real.

---

*Shahram Shafiq, FAST NUCES Islamabad*
*GitHub: [github.com/shahramshafiq](https://github.com/shahramshafiq)*
