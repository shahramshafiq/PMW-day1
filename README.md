# PreserveMy.World: AI-Based 3D Scene Reconstruction
### Shahram Shafiq, PreserveMy.World x TechRealm Internship 2026

---

## What this repo is

This is my working repo for the **PreserveMy.World x TechRealm Impact Internship**, team **EchoFrame Labs**, on the AI-Based 3D Reconstruction track. PreserveMy.World turns phone footage into explorable 3D digital records of heritage sites. My job on this track is to understand and build pieces of the AI pipeline that makes that possible: sourcing footage, comparing reconstruction methods, and building tools around the data.

---

## Who I am

**Shahram Shafiq**, CS sophomore at FAST NUCES Islamabad (CGPA 3.66). I currently teach Python to school students aged 8 to 16 at JuniorCoderz. I've built multi-agent AI systems, custom data structures in C++, and a full Hotel Management system in JavaFX. This is my first time working with 3D reconstruction, but it connects directly to what I already know about computer vision and ML.

- GitHub: [github.com/shahramshafiq](https://github.com/shahramshafiq)
- LinkedIn: [linkedin.com/in/shahramshafiq](https://linkedin.com/in/shahramshafiq)
- Email: shahramshafiqgoraya4363@gmail.com
- Portfolio: [shahramshafiq-portfolio.vercel.app](https://shahramshafiq-portfolio.vercel.app)
- Team: EchoFrame Labs, "Rebuilding the Past. Designing the Future."

---

## What's in this repo

```
PMW-day1/
├── README.md                          <- you are here
├── week1-ai-review.md                 <- strict repo audit, merge fix, prompt reflection
├── portfolio/
│   └── index.html                     <- personal HTML portfolio page
├── 3d-learning/
│   ├── point_cloud_basics.py          <- Python script: 3D reconstruction concepts
│   └── experiment_notes.md            <- what I tried, what worked, what didn't
├── blog-post/
│   └── medium_draft.md                <- blog post content (posted on Dev.to)
├── research/
│   ├── 3d_methods_comparison.md       <- COLMAP vs NeRF vs 3DGS vs MiDaS
│   ├── depth_map_demo.py              <- monocular depth simulation script
│   └── depth_output.png               <- generated output
├── footage-research/
│   ├── badshahi-mosque-multiangle.md  <- sourced, cited, multi-angle footage write-up
│   └── images/                        <- 6 verified real photos of Badshahi Mosque
├── heritage-writing/
│   └── mohenjo-daro.md                <- researched, cited heritage write-up
├── ml-viz-ar-capture3d/
│   ├── capture_to_3d_pipeline.py      <- ML features, AR lines, capture-to-3D on a real photo
│   └── output/                        <- 3 generated visualizations
├── week3-3d-reconstruction/
│   ├── sfm_feasibility_test.py        <- real ORB+RANSAC test of multi-view SfM viability
│   ├── build_ply_reconstruction.py    <- exports a real, validated .ply point cloud
│   └── output/                        <- jaulian_monastery_taxila.ply + verification render
├── youthxai_python_colab.ipynb        <- Kaggle Python course applied to 3D reconstruction
├── youthxai_linear_regression.ipynb   <- linear regression + Kaggle Intro to ML
├── youthxai-regression-output/        <- generated plots from the regression notebook
└── heritage-api/
    ├── app.py                         <- Flask REST API (7 endpoints)
    ├── templates/index.html           <- HTML frontend
    ├── react-app/index.html           <- React dashboard
    └── screenshots/                   <- evidence the app runs
```

---

## Portfolio

My portfolio lives at [`portfolio/index.html`](portfolio/index.html). It's a single-file static site built with pure HTML, CSS, and JavaScript (no frameworks, no build step). Features include:

- Animated sparkle particle background on the hero section
- Scroll-reveal animations
- Working contact form via Web3Forms
- Mobile responsive with hamburger navigation
- Live at [shahramshafiq-portfolio.vercel.app](https://shahramshafiq-portfolio.vercel.app)

> Note: `img.png` (my photo) needs to sit in the same folder as `index.html` to render correctly locally. The deployed Vercel version has it included.

---

## 3D Reconstruction: What I Learned

I started from near zero on this. Here's my honest understanding so far:

**The core problem:** You have a flat 2D photo. You want to recover the 3D structure of whatever was photographed. The problem is it's under-constrained: infinitely many 3D scenes could produce the same 2D image.

**How photogrammetry solves it:** Take many photos from different angles. Find matching feature points across images (SIFT, ORB). Triangulate those features to get 3D coordinates. This is called Structure from Motion (SfM). The output is a sparse point cloud.

**Dense reconstruction:** To fill in all the gaps, we run Multi-View Stereo (MVS) after SfM. Now we get millions of points.

**What NeRF does differently:** Instead of matching features, a Neural Radiance Field trains a small neural network to learn what the scene looks like from any angle. The network takes (x, y, z, viewing direction) and outputs (color, density). Rendering means ray marching through the network. Slow to train but photorealistic.

**Gaussian Splatting:** Newer than NeRF. Represents the scene as millions of little 3D Gaussian blobs. Renders in real-time. PreserveMy.World is likely using this or something similar for the explorable worlds part.

**Why this matters for heritage:** A historic site can be reconstructed from drone footage or phone video and stored forever as a 3D model. People can explore it virtually even if the physical site is damaged, demolished, or inaccessible.

**My Python experiment:** [`3d-learning/point_cloud_basics.py`](3d-learning/point_cloud_basics.py) simulates a photogrammetry reconstruction pipeline from scratch using numpy and matplotlib. It demonstrates depth, projection, and point cloud generation for a heritage building corner. I tried Open3D first but hit a GLIBC version issue on my setup, so I documented the fallback in the experiment notes.

---

## Blog Post

Full post: [`blog-post/medium_draft.md`](blog-post/medium_draft.md)

This covers my learning journey about 3D reconstruction and how I plan to use it at PreserveMy.World.

---

## Research: Comparing 3D Reconstruction Methods

Full comparison: [`research/3d_methods_comparison.md`](research/3d_methods_comparison.md)

**Environment used:** Python 3.11 (Anaconda), Git, VS Code, gh CLI. AI coding assistant (Cursor) used for boilerplate and syntax help; all logic read, understood, and verified manually before committing.

I compared four methods: COLMAP, NeRF, 3D Gaussian Splatting (3DGS), and Monocular Depth Estimation (MiDaS). Each entry covers inputs, outputs, hardware needs, difficulty, and where it fits the PMW pipeline.

[`research/depth_map_demo.py`](research/depth_map_demo.py) simulates monocular depth estimation: generates a synthetic depth map of a heritage building (pillars, facade, arched doorway), converts it to a 3D point cloud via back-projection, and saves a 3-panel visualization at [`research/depth_output.png`](research/depth_output.png).

**Key finding:** for PMW's "explorable worlds" feature, the full production pipeline is:
1. Capture footage (phone or drone)
2. Extract frames, run **COLMAP** to get camera poses and a sparse point cloud
3. Feed into **3D Gaussian Splatting** for real-time navigable output
4. Optional: run **NeRF** (Nerfstudio) for high quality archival renders

Monocular depth (MiDaS) is useful when only a single photo of a site exists.

**Tutorials watched:** Computerphile "How does 3D Scanning Work?", Computerphile "Neural Radiance Fields", "Structure from Motion explained", Open3D documentation, Nerfstudio documentation.

---

## Python Fundamentals Applied to 3D Reconstruction

Notebook: [`youthxai_python_colab.ipynb`](youthxai_python_colab.ipynb)

Covers the 7 Kaggle Python course topics (variables, functions, conditionals, lists, loops, strings/dicts, libraries), each applied directly to 3D reconstruction: perspective projection, point cloud generation, and camera view rendering for heritage sites (Lahore Fort, Rohtas Fort, Mohenjo-daro, Badshahi Mosque).

---

## Heritage Reconstruction API

Full app: [`heritage-api/`](heritage-api/)

A full stack Flask + React web app modeling the actual PMW reconstruction pipeline. Flask REST API with 7 endpoints serving data for 4 Pakistani heritage sites, two frontends (a Flask-rendered HTML reference page and a React dashboard with an animated 3D point cloud), and a reconstruction job simulator. Tested via curl, Postman, and a direct LAN IP hit. Full setup and API docs in [`heritage-api/README.md`](heritage-api/README.md).

---

## Repo Audit and Prompt Engineering

Full write-up: [`week1-ai-review.md`](week1-ai-review.md)

Ran a strict AI-assisted audit against my own GitHub work instead of asking for generic feedback. The top finding was real: a PR merging research into `main` had been open for over a week without being merged, meaning that work was invisible to anyone browsing the default branch. Fixed it, rewrote the README to reflect the true scope of the repo, and documented what worked and failed about the prompting process itself.

---

## Multi-Angle Footage: Badshahi Mosque

Full write-up: [`footage-research/badshahi-mosque-multiangle.md`](footage-research/badshahi-mosque-multiangle.md)

Sourced, downloaded, and individually verified 6 real photos of Badshahi Mosque covering distinct angles (front facade, aerial, interior, wide front view with garden, minaret side angle, elevated panorama), then wrote a technical piece auditing what the footage set does and does not cover for an actual 3D reconstruction pipeline. Cross-checked against the simulated coverage number used for the same site in heritage-api.

---

## Heritage Write-up: Mohenjo-daro

Write-up: [`heritage-writing/mohenjo-daro.md`](heritage-writing/mohenjo-daro.md)

A 451-word researched piece on Mohenjo-daro: what it is, why it matters, what a visitor should notice. Every historical fact, construction date, population, UNESCO status, the salinity threat, the 2012 and 2022 conservation warnings, is checked against Wikipedia and cross-verified against a second independent source (Ancient Origins and UNESCO's own World Heritage Centre listing) before being written down.

---

## Linear Regression and Kaggle Intro to ML

Notebook: [`youthxai_linear_regression.ipynb`](youthxai_linear_regression.ipynb)

Linear regression implemented from scratch with gradient descent and checked against scikit-learn (both converge on the same slope and intercept), applied to predicting reconstruction time from photo count. Followed by the core Kaggle Intro to ML lessons (data exploration, first model, validation, underfitting/overfitting, random forests) applied to a simulated 220-job heritage reconstruction dataset. Every cell in this notebook was executed and verified before committing; the generated plots are in [`youthxai-regression-output/`](youthxai-regression-output/).

---

## ML Visualizations, AR Lines and Capture-to-3D

Pipeline and write-up: [`ml-viz-ar-capture3d/`](ml-viz-ar-capture3d/)

One real photo of the Jaulian monastery ruins at Taxila run through three stages: Sobel gradient and Harris corner feature detection, an AR-style line overlay simulating what a heritage app would show live on a phone camera, and a heuristic capture-to-3D colored point cloud. Taxila was picked on purpose to tie into the Team Taxila group sprint running in parallel. Two real bugs were caught by actually looking at the rendered output rather than trusting the code ran without errors: the point cloud stage initially treated the sky as a physical surface and warped the whole projection (fixed by measuring this photo's actual sunset-lit sky/haze brightness and masking it out), and the AR line overlay initially produced 271 noisy lines blanketing the frame (fixed by tightening the edge and line-detection thresholds down to 25 clean, meaningful lines).

---

## Convert Curated Footage to a 3D Reconstruction (.ply)

Write-up: [`week3-3d-reconstruction/`](week3-3d-reconstruction/)

Tested whether real multi-view Structure from Motion (feature matching and triangulation, what COLMAP does) was viable on the 6 already-curated Badshahi Mosque photos before choosing an approach: ORB feature matching and RANSAC geometric verification across 3 photo pairs found only 12 to 17 consistent inliers out of 2000+ keypoints per photo, not enough real overlap for triangulation, since these are photos from different photographers rather than a controlled multi-view capture. Built a monocular reconstruction of the Jaulian monastery ruins instead (extending the approach from `ml-viz-ar-capture3d/`), and exported it as a real `.ply` point cloud file, hand-written against the format spec rather than pulled from a library. Validated three separate ways: manually re-parsed the file to confirm every line is well-formed, reloaded it from disk and re-rendered it to confirm the geometry survives the round trip, and compared it against the earlier module's equivalent visualization.

---

## Mission Connection

PreserveMy.World's core mission is to document and preserve cultural heritage before it disappears. 3D reconstruction is the technical engine that makes this possible, turning footage of a mosque, fort, or old city street into a navigable digital record. As someone on the AI track, my job is to understand and eventually contribute to that pipeline.

Pakistan has hundreds of heritage sites that are underdocumented. Mohenjo-daro, one of the earliest cities of the Indus Valley civilization, faces active deterioration and is a priority target in my heritage-api data model. This isn't just a technical exercise; there's a real gap to fill.

---

*Portfolio, 3D reconstruction research, two applied Python/ML notebooks, a full stack heritage reconstruction API, a real repo audit, and sourced multi-angle footage all live in this repo.*
