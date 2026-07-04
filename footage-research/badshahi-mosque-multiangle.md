# Sourced Multi-Angle Footage: Badshahi Mosque, Lahore

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 2, Module 8 (w2d1)**

---

## Why this subject

Badshahi Mosque is already one of the four sites in my Custom Assignment heritage-api dataset (`heritage-api/app.py`), where it is modeled with a 97.2% simulated coverage score and 3D Gaussian Splatting as its reconstruction method. This task is a chance to check that number against real, publicly available imagery instead of a number I made up for the demo.

**A correction before this write-up starts:** an earlier version of this document linked out to `commons.wikimedia.org` file pages without actually opening them first. Several of those links were pulled from a search summary, not a verified fetch, and some pointed at file page URLs I had never confirmed existed. That was a mistake. The six images below were re-sourced, individually downloaded, and visually checked by me against their captions before being committed to this repo. They now live in [`images/`](images/) so the deliverable does not depend on any external link staying alive.

---

## Sourced footage: 6 verified angles

Each image was fetched directly from Wikimedia's media host (`upload.wikimedia.org`), downloaded, and opened to confirm it actually shows what the caption claims, before being added to this repo.

| # | File | Angle | What it actually shows | Why it matters for reconstruction |
|---|------|-------|-------------------------|-----------------------------------|
| 1 | [images/01-front-facade.jpg](images/01-front-facade.jpg) | Front facade, ground level | Full front elevation: main archway, flanking minarets, three domes, clear sky | Primary reference view, establishes the main facade plane |
| 2 | [images/02-aerial-rooftop.jpg](images/02-aerial-rooftop.jpg) | Aerial, from an adjacent minaret | Marble domes seen from above, with Lahore's skyline and a red sandstone minaret in the background | Gives the roofline and dome geometry that ground-level shots cannot capture |
| 3 | [images/03-interior-hall.jpg](images/03-interior-hall.jpg) | Interior, prayer hall corridor | Ornately decorated hallway, painted ceiling, chandeliers, receding archways | Interior geometry is a separate reconstruction problem from the exterior shell |
| 4 | [images/04-wide-front-garden.jpg](images/04-wide-front-garden.jpg) | Wide front view with foreground garden | Full facade from a distance, including the Hazuri Bagh garden and fountain in front of it | Adds real-world scale and a second depth layer (the garden) in front of the structure |
| 5 | [images/05-minaret-side-angle.jpg](images/05-minaret-side-angle.jpg) | Minaret, steep side angle | A single red sandstone minaret in sharp foreground, with the white marble domes of the adjacent Ranjit Singh Samadhi (a Sikh-era mausoleum) visible behind it | Oblique, off-axis camera pose, exactly the kind of view photogrammetry needs to triangulate a vertical structure accurately |
| 6 | [images/06-panoramic-elevated.jpg](images/06-panoramic-elevated.jpg) | Panoramic, elevated wide shot | The full courtyard and complex seen from a raised vantage point, with a minaret in the foreground anchoring the scale | Wide establishing shot, useful as a scale and layout reference against the closer shots |

**Original sources (Wikimedia Commons, via Wikipedia's Badshahi Mosque article):** all six files are hosted at `upload.wikimedia.org` and were originally uploaded to Wikimedia Commons under Creative Commons licenses. Full attribution and exact license terms for each file are listed on its Wikimedia Commons file page, linked from the [Badshahi Mosque Wikipedia article](https://en.wikipedia.org/wiki/Badshahi_Mosque) under the image credits. I am hosting local copies in this repo for reliability, not claiming original authorship.

---

## Written piece: what this footage set tells me about reconstruction readiness

Badshahi Mosque was built between 1671 and 1673 under Emperor Aurangzeb, with construction overseen by his foster brother, Fidai Khan Koka [1]. It is built from red sandstone with white marble inlay, a departure from the tile work more common elsewhere in Lahore, and the complex includes an expansive courtyard, a prayer hall with three marble domes, and eight minarets, four major towers standing 60 meters tall and four smaller ones [1]. The courtyard alone covers about 25,600 square meters and the complex can hold 100,000 worshippers, with the prayer hall itself seating 10,000 [1]. The mosque underwent a major restoration between 1939 and 1960, and has been on UNESCO's tentative World Heritage list since 1993 [1].

None of that history is visible in a single photograph. That is the actual argument for multi-angle capture, and it is worth being specific about what six angles buys you versus what a single hero shot does not.

A front facade shot alone (image 1) gives you one plane of geometry: the main archway, the flanking towers, and whatever depth cues come from shadow. It tells you almost nothing about the roofline or how the domes relate to each other in 3D space. The aerial shot (image 2) fixes part of that: taken from an adjacent minaret rather than a drone, it still gives real elevation and shows the domes as three-dimensional forms with the city behind them for scale. The wide front shot with the garden (image 4) adds a second depth layer entirely absent from image 1: a fountain and garden bed sitting between the camera and the building, which is exactly the kind of foreground-midground-background separation that helps a structure-from-motion pipeline triangulate depth. The minaret shot (image 5), taken from a steep side angle that a typical tourist photo would avoid, is the kind of oblique, off-axis camera pose that photogrammetry actually needs to reconstruct a tall vertical structure correctly, most casual photography avoids this angle because it looks less flattering, but it is structurally the most useful. The interior shot (image 3) is the most important gap-filler: images 1, 2, 4, 5, and 6 are all exterior, and a 3D model built only from exterior photos would render the mosque as a hollow shell with nothing behind the front wall. The panoramic elevated shot (image 6) works as a full-context anchor, tying the courtyard layout to the individual close-up angles.

Even with six well-chosen, verified angles, this set would not be enough to actually run COLMAP or feed a Gaussian Splatting pipeline. Production-grade reconstruction needs 50 to 300+ overlapping photos with sufficient baseline overlap between neighboring shots, not six curated highlights taken by different photographers, at different times of day, with different cameras and focal lengths. What this set is actually useful for is a coverage audit: checking which angles exist publicly, which are missing (there is no back facade shot in this set, and no direct top-down drone view, only an oblique aerial from a minaret), and which structural elements still have no freely available photographic coverage. That gap is itself a useful finding heading into Week 3, when the plan is to reconstruct something from curated footage: a public archive can tell you what a site looks like, but it will rarely tell you, on its own, whether the coverage is dense enough for an actual reconstruction pipeline to succeed.

---

## Sources

[1] [Badshahi Mosque, Wikipedia](https://en.wikipedia.org/wiki/Badshahi_Mosque), accessed 4 Jul 2026, for construction date, architect, dimensions, and preservation history.

Images: originally sourced via Wikimedia Commons (linked from the Badshahi Mosque Wikipedia article's image credits), downloaded and verified individually before being added to this repository at [`footage-research/images/`](images/).
