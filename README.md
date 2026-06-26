# PMW Day 1: GitHub Portfolio Setup
### Shahram Shafiq, AI Track, PreserveMy.World x TechRealm Internship 2026

---

## What this repo is

This is my Day 1 submission for the **PreserveMy.World x TechRealm Impact Internship** (22 Jun to 19 Jul 2026). I'm on the AI-Based 3D Reconstruction track. The goal of Day 1 was to:

- Set up GitHub properly
- Build a personal portfolio page
- Start learning 3D reconstruction and document what I understood
- Write a public blog post about it

PreserveMy.World turns phone footage into explorable 3D digital records of heritage sites. My track is about building the AI pipeline that makes that possible.

---

## Who I am

**Shahram Shafiq**, CS sophomore at FAST NUCES Islamabad (CGPA 3.66). I currently teach Python to school students aged 8 to 16 at JuniorCoderz. I've built multi-agent AI systems, custom data structures in C++, and a full Hotel Management system in JavaFX. This is my first time working with 3D reconstruction, but it connects directly to what I already know about computer vision and ML.

- GitHub: [github.com/shahramshafiq](https://github.com/shahramshafiq)
- LinkedIn: [linkedin.com/in/shahramshafiq](https://linkedin.com/in/shahramshafiq)
- Email: shahramshafiqgoraya4363@gmail.com
- Portfolio: [shahramshafiq-portfolio.vercel.app](https://shahramshafiq-portfolio.vercel.app)

---

## What's in this repo

```
PMW-day1/
├── README.md               <- you are here
├── portfolio/
│   └── index.html          <- personal HTML portfolio page
├── 3d-learning/
│   ├── point_cloud_basics.py   <- Python script: 3D reconstruction concepts
│   └── experiment_notes.md     <- what I tried, what worked, what didn't
└── blog-post/
    └── medium_draft.md         <- blog post content (posted on Medium/DEV)
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

I started from near zero on this. Here's my honest understanding after Day 1:

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

This covers my complete Day 1 learning journey about 3D reconstruction and how I plan to use it at PreserveMy.World.

---

## Mission Connection

PreserveMy.World's core mission is to document and preserve cultural heritage before it disappears. 3D reconstruction is the technical engine that makes this possible, turning footage of a mosque, fort, or old city street into a navigable digital record. As someone on the AI track, my job is to understand and eventually contribute to that pipeline. Day 1 was about building the foundations.

Pakistan has hundreds of heritage sites that are underdocumented. This isn't just a technical exercise; there's a real gap to fill.

---

*Day 1 complete. Day 2 is Python Setup and Git/First PR.*
