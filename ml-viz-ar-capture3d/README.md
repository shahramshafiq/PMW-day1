# ML Visualizations, AR Lines & Capture-to-3D

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 2, Day 4**

---

## What this is

One real photo run through three connected stages: an ML feature/edge visualization, an AR-style line overlay, and a heuristic capture-to-3D point cloud. Script: [`capture_to_3d_pipeline.py`](capture_to_3d_pipeline.py). Source photo: [`source/jaulian-monastery-taxila.jpg`](source/jaulian-monastery-taxila.jpg). Outputs: [`output/`](output/).

**Why Taxila:** an elevated view of the Jaulian Buddhist monastery ruins, sourced from Wikimedia Commons via the Taxila Wikipedia article and verified before use. Chosen on purpose over reusing a site already covered elsewhere in this repo, it ties directly to the Team Taxila group sprint running in parallel, and the ring of ruined monk cells gives noticeably richer, more repeated structure to detect than a single flat facade would.

---

## Stage 1: ML visualization

[`output/01_ml_visualization.png`](output/01_ml_visualization.png)

Two classic feature-detection outputs, computed with OpenCV:

- **Sobel gradient magnitude**: the edge/intensity-change map. On this photo it cleanly traces the repeated monk cell walls, the courtyard boundary, and the hillside horizon.
- **Harris corner detection**: 24,091 corner-response pixels, concentrated densely across the stonework, exactly the kind of feature points Structure from Motion would try to match across multiple photos of the same ruins to triangulate their 3D shape.

---

## Stage 2: AR line overlay

[`output/02_ar_line_overlay.png`](output/02_ar_line_overlay.png)

Canny edge detection followed by a probabilistic Hough transform (`cv2.HoughLinesP`), drawn directly on top of the original photo in bright green, plus a red courtyard symmetry axis. This simulates what an AR heritage app would show a visitor holding their phone up at the site: live structural line tracking locking onto the same cell walls and courtyard edges a reconstruction pipeline would also key off of.

**This stage needed a real fix.** The first pass reused the same Canny/Hough thresholds that worked on a different, flatter photo used earlier in this pipeline's development, and it produced 271 line segments that blanketed almost the entire frame in noisy horizontal streaks, picking up mortar lines and stone texture instead of actual structural boundaries. Caught by looking at the rendered image, not by trusting that 271 lines meant it worked. Tightening the Canny thresholds (60/150 to 100/200) and the Hough parameters (threshold 60 to 80, minimum line length 40 to 60, max gap 8 to 5) brought it down to 25 clean, meaningful lines that actually trace the cell walls, courtyard edge, and horizon.

---

## Stage 3: Capture-to-3D

[`output/03_capture_to_3d.png`](output/03_capture_to_3d.png)

This is a heuristic single-image depth estimate, not a trained monocular depth network like MiDaS. Being upfront about exactly what it does and does not do:

1. **Sky and haze masking first.** Neither has a reconstructible surface, so both had to be excluded before back-projecting, otherwise they get treated as physical "walls" and warp the whole point cloud. This photo is lit at sunset, which flips the usual assumption: the sky here is actually *more* saturated than the hazy distant hills below it, measured directly on this image (sky: saturation ~74, brightness ~238; hazy hills: saturation ~47, brightness ~238; foreground ruins: saturation ~149, brightness ~167). Saturation alone does not separate sky from haze here, but brightness does, since both the sky and the haze are far brighter than the shadowed stonework. That is the mask actually used (`brightness > 205`), re-measured on this specific photo rather than reusing the previous photo's saturation-based threshold, which does not transfer given the different lighting.
2. **Depth heuristic for what's left:** lower in the frame means nearer the camera, and locally strong edges are pulled slightly forward for a bit of relief. Because this photo is an elevated, downward-looking shot into a ring of walls around a courtyard, the resulting point cloud is a bowl-like shape, which is the geometrically correct outcome for this camera angle, not a bug like the curtain-shaped distortion an earlier version of this pipeline produced on a different photo.
3. **Back-projection:** each surviving pixel converts from 2D image coordinates plus estimated depth into an (x, y, z) point using a standard pinhole camera model, colored with that pixel's real RGB value. 5,958 points make it through the mask.

A single photo cannot recover real depth the way multiple overlapping photos (COLMAP) or a trained depth network (MiDaS) can. What this does show honestly is the ring of walls and courtyard floor reading as a recognizable 3D shape from three different angles, the right amount of signal to expect from one image and no more.

---

## Why this matters for PMW

Same three-stage shape as the actual production pipeline, compressed to run on one photo instead of hundreds. Feature detection (Stage 1) is what COLMAP does across many images to find matches. AR line tracking (Stage 2) is the kind of live overlay a capture app would show a field volunteer to confirm coverage while filming a site. Capture-to-3D (Stage 3) is the eventual output, just with a real monocular depth network and many more photos standing in for the heuristic used here.
