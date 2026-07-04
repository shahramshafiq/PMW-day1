# PMW Week 1: GitHub Portfolio, Research & Custom Build
### Shahram Shafiq, AI-Based 3D Scene Reconstruction Track, PreserveMy.World x TechRealm Internship 2026

---

## What this repo is

This is my Week 1 submission repo for the **PreserveMy.World x TechRealm Impact Internship** (22 Jun to 19 Jul 2026), team **EchoFrame Labs**. I'm on the AI-Based 3D Reconstruction track. Week 1 covered:

- Setting up GitHub properly and building a personal portfolio page
- Learning 3D reconstruction fundamentals and documenting the process
- Writing a public blog post
- Researching and comparing 3D reconstruction methods (COLMAP, NeRF, 3DGS, MiDaS)
- Completing the youthxAI Python + Colab exercises
- Building a full stack Flask + React app for the Custom Assignment

PreserveMy.World turns phone footage into explorable 3D digital records of heritage sites. My track is about building the AI pipeline that makes that possible.

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
├── youthxai_python_colab.ipynb        <- Kaggle Python course applied to 3D reconstruction
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

I started from near zero on this. Here's my honest understanding after Week 1:

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

## youthxAI: Python + Colab

Notebook: [`youthxai_python_colab.ipynb`](youthxai_python_colab.ipynb)

Covers the 7 Kaggle Python course topics (variables, functions, conditionals, lists, loops, strings/dicts, libraries), each applied directly to 3D reconstruction: perspective projection, point cloud generation, and camera view rendering for heritage sites (Lahore Fort, Rohtas Fort, Mohenjo-daro, Badshahi Mosque).

---

## Custom Assignment: Heritage Reconstruction API

Full app: [`heritage-api/`](heritage-api/)

A full stack Flask + React web app modeling the actual PMW reconstruction pipeline. Flask REST API with 7 endpoints serving data for 4 Pakistani heritage sites, two frontends (a Flask-rendered HTML reference page and a React dashboard with an animated 3D point cloud), and a reconstruction job simulator. Tested via curl, Postman, and a direct LAN IP hit. Full setup and API docs in [`heritage-api/README.md`](heritage-api/README.md).

---

## Mission Connection

PreserveMy.World's core mission is to document and preserve cultural heritage before it disappears. 3D reconstruction is the technical engine that makes this possible, turning footage of a mosque, fort, or old city street into a navigable digital record. As someone on the AI track, my job is to understand and eventually contribute to that pipeline.

Pakistan has hundreds of heritage sites that are underdocumented. Mohenjo-daro, one of the earliest cities of the Indus Valley civilization, faces active deterioration and is a priority target in my heritage-api data model. This isn't just a technical exercise; there's a real gap to fill.

---

*Week 1 complete: portfolio, 3D learning, research comparison, youthxAI Colab notebook, and the heritage reconstruction API all live in this repo.*
