# Present the Build & Convert to 3D

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 3, Day 1 (Mon 6 Jul 2026)**

---

## 1. Present your team's progress: Team Taxila

I am team lead for Team Taxila's group preservation sprint (Taxila and the Gandhara learning route, separate group activity, not this individual module). Honest status as of today:

- **Rabeea Iman** built the team's presentation covering Taxila's history, conservation importance, and challenges.
- **Ruwaida Shakeel** built and published the live location page at [ruwaidashakeel05.github.io/Taxila](https://ruwaidashakeel05.github.io/Taxila/), genuinely strong work: it covers the real, current (2026) UNESCO warning over cement restoration at Mohra Moradu and Sirkap, an interactive 3D reconstruction toggle, a Gandhara learning route map, and 8 cited sources. I independently verified the central UNESCO claim against 7+ news outlets before trusting it.
- I missed the team's live session due to a scheduling conflict. As lead, my job now is finishing the portal's required team setup fields (branding, source log, links), still in progress.
- Still open on the team side: branding (name/logo/cover image was never decided), and additional footage/3D reconstruction work, which the team agreed to assign once the other 3 roster members (currently inactive in the group) engage.

## 2. Convert curated footage into a 3D reconstruction

Two files, run in order: [`sfm_feasibility_test.py`](sfm_feasibility_test.py), then [`build_ply_reconstruction.py`](build_ply_reconstruction.py). Output: [`output/jaulian_monastery_taxila.ply`](output/jaulian_monastery_taxila.ply).

### Step 1: tested whether real multi-view SfM was viable first

Before picking an approach, I tested whether genuine Structure from Motion (feature matching + triangulation across multiple photos, what COLMAP actually does) works on the 6 photos already curated in `footage-research/images/` (the Badshahi Mosque set). Ran ORB feature detection and RANSAC-verified fundamental matrix estimation across 3 photo pairs:

| Pair | Keypoints | Candidate matches | RANSAC-verified inliers |
|---|---|---|---|
| front facade vs wide front garden | 2143, 2797 | 60 | 17 |
| front facade vs minaret side angle | 2143, 2842 | 60 | 12 |
| wide front garden vs panoramic elevated | 2797, 2064 | 60 | 14 |

12 to 17 geometrically consistent matches out of 2000+ keypoints per photo, consistently weak across all three pairs. These are 6 real photos from different photographers, cameras, and lighting, not a controlled multi-view capture. That is not enough overlap for real triangulation, this matches what I already wrote honestly in `footage-research/badshahi-mosque-multiangle.md` before writing any code to check it. Forcing a point cloud out of this few, weak matches would produce geometrically meaningless output, so I did not.

### Step 2: built a monocular reconstruction instead, and exported it as a real .ply

Since multi-view SfM was not viable on the available curated photos, I extended the monocular capture-to-3D approach already validated in `ml-viz-ar-capture3d/` (same photo: the Jaulian monastery ruins at Taxila, same sky/haze brightness mask, same row-position-plus-edge depth heuristic), and this time exported it as a real, standard `.ply` point cloud file instead of just a plot image.

The PLY writer was built by hand against the format spec (ASCII header declaring vertex count and per-vertex `x y z red green blue` properties, followed by one line per point), not pulled from a library, so every line of the header is something I can actually explain. 13,375 points, 436 KB.

**Validated three separate ways, not just "it wrote without an error":**
1. Manually re-parsed the file afterward and checked the declared vertex count matches the actual number of data lines exactly, and that every single line has 6 well-formed fields with colors in valid 0-255 range.
2. Loaded the file back from disk (not from the in-memory arrays that generated it) and re-rendered it in matplotlib (`output/ply_reload_verification.png`), confirming it round-trips to the same recognizable ring-of-walls-around-a-courtyard shape.
3. Compared the reloaded shape against the equivalent visualization from the earlier `ml-viz-ar-capture3d` module to confirm consistency.

**Honest limitations, same as documented before:** this is a monocular heuristic depth estimate, not a trained network like MiDaS and not real multi-view triangulation. The bowl-like shape is the geometrically correct outcome for this specific elevated, downward-looking camera angle into a ring of walls, not an artifact.

---

## 3. Export a .ply file

[`output/jaulian_monastery_taxila.ply`](output/jaulian_monastery_taxila.ply), openable in MeshLab, CloudCompare, Blender, or any standard point cloud viewer.
