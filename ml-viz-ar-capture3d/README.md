# ML Visualizations, AR Lines & Capture-to-3D

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 2, Day 4**

---

## What this is

One real, already-verified photo (the Badshahi Mosque front facade from [`footage-research/images/01-front-facade.jpg`](../footage-research/images/01-front-facade.jpg)) run through three connected stages: an ML feature/edge visualization, an AR-style line overlay, and a heuristic capture-to-3D point cloud. Script: [`capture_to_3d_pipeline.py`](capture_to_3d_pipeline.py). Outputs: [`output/`](output/).

---

## Stage 1: ML visualization

[`output/01_ml_visualization.png`](output/01_ml_visualization.png)

Two classic feature-detection outputs, computed with OpenCV:

- **Sobel gradient magnitude**: the edge/intensity-change map. This is the same kind of gradient information a feature detector (SIFT, ORB, the kind COLMAP uses) starts from before it picks out distinctive keypoints.
- **Harris corner detection**: 9,397 corner-response pixels found, concentrated exactly where a human would expect: arch edges, dome outlines, minaret silhouettes. These are the literal feature points that Structure from Motion would try to match across multiple photos of the same building to triangulate its 3D shape.

---

## Stage 2: AR line overlay

[`output/02_ar_line_overlay.png`](output/02_ar_line_overlay.png)

Ran Canny edge detection followed by a probabilistic Hough transform (`cv2.HoughLinesP`) to pull out 145 straight line segments, then drew them directly on top of the original photo in bright green, plus a red facade symmetry axis down the middle. This simulates what an AR heritage app would show a visitor holding their phone up to the building: live structural line tracking overlaid on the camera feed, locking onto the same arches, dome edges, and minaret verticals that a reconstruction pipeline would also key off of.

---

## Stage 3: Capture-to-3D

[`output/03_capture_to_3d.png`](output/03_capture_to_3d.png)

This is a heuristic single-image depth estimate, not a trained monocular depth network like MiDaS. Being upfront about exactly what it does and does not do:

1. **Sky masking first.** The sky has no physical surface, so treating it as part of the depth field breaks everything. Measured directly on this photo: sky pixels average saturation ~38 and brightness ~210, versus ~113 and ~178 for the building. Thresholding on that (low saturation, high brightness) masked out 59.7% of the image as sky before any depth or projection math ran. My first pass at this script skipped that step and the sky got projected as a giant warped backdrop, a genuine bug I caught and fixed by actually looking at the output before writing this up, not by assuming it worked.
2. **Depth heuristic for what's left:** lower in the frame means nearer the camera (a reasonable assumption for a photo taken at ground level with a visible base), and locally strong edges get pulled slightly forward, so domes and minarets pop out a little from the flatter wall behind them instead of everything sitting on one flat plane.
3. **Back-projection:** each surviving pixel is converted from 2D image coordinates plus estimated depth into an (x, y, z) point using a standard pinhole camera model, then colored with that exact pixel's real RGB value from the photo. 7,398 points make it through the sky mask.

The result is a shallow relief, not a full volumetric reconstruction, and it should not be mistaken for one. A single photo cannot recover real depth the way multiple overlapping photos (COLMAP) or a trained depth network (MiDaS) can. What it does show, honestly, is the recognizable silhouette of the mosque with real domes and minarets reading as distinct 3D forms when viewed from the front, three-quarter, and side angles, which is the right amount of signal to expect from one image and no more.

---

## Why this matters for PMW

This is the same three-stage shape as the actual production reconstruction pipeline, just compressed to run on one photo instead of hundreds: detect features (Stage 1) is what COLMAP does across many images to find matches, AR line tracking (Stage 2) is the kind of live overlay a capture app would show a field volunteer to confirm coverage while filming a site, and capture-to-3D (Stage 3) is the eventual output, just with a real monocular depth network and many more photos standing in for the heuristic used here.
