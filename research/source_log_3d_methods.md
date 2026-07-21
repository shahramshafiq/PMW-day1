# Source Log: 3D Reconstruction Methods for PreserveMy.World

**Shahram Shafiq | Extension Sprint 2, Research and Source Log | AI-Based 3D Scene Reconstruction Track**

---

## Research question

The Day 2 comparison of COLMAP, NeRF, 3D Gaussian Splatting, and monocular depth (`research/3d_methods_comparison.md`) was written from general knowledge, with no cited sources. This log fixes that gap and answers a narrower, more useful question: what do the actual papers and documentation say about each method's real requirements, and does that explain what actually happened when I tested real multi-view reconstruction in Week 3 (`week3-3d-reconstruction/`), where I got only 12 to 17 geometrically verified matches per photo pair out of 2,000+ keypoints, not enough to triangulate, and had to pivot to a monocular depth heuristic instead?

Every source below was fetched and checked live before being cited, not assumed from memory.

---

## Sources

### 1. Structure-from-Motion Revisited (the COLMAP paper)
**Link:** https://openaccess.thecvf.com/content_cvpr_2016/html/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.html
**Authors / venue:** Johannes L. Schönberger and Jan-Michael Frahm, CVPR 2016 (CVF Open Access, freely readable, no login)
**Credibility:** This is the actual academic paper COLMAP was built from, hosted on the Computer Vision Foundation's own open-access archive, not a summary or a blog post.
**In my own words:** This paper is the foundation for basically all classic multi-view 3D reconstruction, including the SfM feasibility test I ran in Week 3. It describes incremental Structure-from-Motion: find matching feature points across many photos of the same scene, triangulate their 3D positions, and work out where each camera was standing. The key thing for my project is that this whole approach depends entirely on having enough correctly-matched points between photo pairs, which is exactly the step that failed when I tested it.

### 2. NeRF, Representing Scenes as Neural Radiance Fields for View Synthesis
**Link:** https://arxiv.org/abs/2003.08934
**Authors / venue:** Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, Ren Ng, ECCV 2020 (arXiv preprint, freely readable)
**Credibility:** Original arXiv paper from the authors, the standard way to cite this work.
**In my own words:** NeRF trains a small neural network to answer "what color and density is at this exact 3D point, seen from this exact angle," then renders new views by sampling along camera rays. The part that matters for PMW: NeRF needs 20 to 200 images with known camera positions, and those camera positions are normally obtained by running COLMAP first. So NeRF doesn't replace the multi-view matching problem I hit, it depends on it succeeding first.

### 3. 3D Gaussian Splatting for Real-Time Radiance Field Rendering
**Link:** https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
**Authors / venue:** Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis, ACM Transactions on Graphics, July 2023 (official project page hosted by the research lab, Inria)
**Credibility:** Official project page from the paper's own institution, includes the paper, code, and results directly from the authors.
**In my own words:** 3DGS represents a scene as a cloud of soft, colored 3D blobs (Gaussians) instead of a neural network, which is why it renders in real time instead of taking 30 seconds per frame like NeRF. For PMW's "explorable worlds" goal this is the most realistic real-time option, but it has the exact same input requirement as NeRF: calibrated multi-view images with known camera poses. Same dependency, same failure point for my dataset.

### 4. Towards Robust Monocular Depth Estimation, Mixing Datasets for Zero-Shot Cross-Dataset Transfer (MiDaS)
**Link:** https://github.com/isl-org/MiDaS
**Authors / venue:** René Ranftl, Katrin Lasinger, David Hafner, Konrad Schindler, Vladlen Koltun, originally arXiv:1907.01341, later IEEE TPAMI 2022 (official repository, Intel ISL)
**Credibility:** Official maintained repository from the paper's original authors' lab, not a fork or mirror.
**In my own words:** MiDaS is trained on 12 different datasets at once so it can guess a reasonable depth map from a single photo it has never seen anything like before, without needing multiple viewpoints at all. This is the actual category of method behind the monocular depth heuristic I used in Week 3 after multi-view SfM failed, real MiDaS is a trained neural network doing this properly, mine is a simpler hand-written heuristic (brightness-based sky masking plus a row-position depth cue), which is exactly the honest limitation I already wrote up in `week3-3d-reconstruction/README.md`.

### 5. Cultural Heritage Imaging: Photogrammetry
**Link:** https://culturalheritageimaging.org/Technologies/Photogrammetry/
**Authors / venue:** Cultural Heritage Imaging, a nonprofit specifically focused on 3D documentation of heritage sites
**Credibility:** A heritage-sector-specific technical guide, not a general CV tutorial, directly relevant to PMW's actual mission, not just the algorithm.
**In my own words:** This is the source that actually explains *why* my SfM test failed. It states that reliable photogrammetry needs a consistent 66% overlap between consecutive photos, and that round subjects need photos taken every 10 to 15 degrees, with every part of the subject covered by at least three overlapping frames. My 6 test photos were taken by different photographers at different times with no overlap plan at all, so getting only 12 to 17 verified matches per pair isn't a bug in my code, it's the expected outcome of feeding an SfM pipeline photos that never met the coverage requirement it needs to work.

---

## Connecting the research to a PMW deliverable

This directly explains and strengthens the honest failure analysis already written in `week3-3d-reconstruction/README.md`: the SfM test didn't fail because of a coding mistake, it failed because the 6 available photos never met the ~66% overlap, 10 to 15 degree spacing standard that source 5 documents as the actual requirement for this class of method (sources 1 to 3). Given that, pivoting to a monocular depth heuristic (source 4's category of method) was the technically correct call for this specific dataset, not a fallback taken because multi-view was too hard.

**Practical takeaway for future PMW capture sessions:** if the team wants real multi-view SfM or NeRF/3DGS output instead of a monocular heuristic, footage needs to be captured by one person, in one session, following the 66% overlap and 10 to 15 degree spacing guidance from source 5, not sourced after the fact from photos taken by different people at different times.
