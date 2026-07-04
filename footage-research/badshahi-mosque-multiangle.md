# Sourced Multi-Angle Footage: Badshahi Mosque, Lahore

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 2, Module 8 (w2d1)**

---

## Why this subject

Badshahi Mosque is already one of the four sites in my Custom Assignment heritage-api dataset (`heritage-api/app.py`), where it is modeled with a 97.2% simulated coverage score and 3D Gaussian Splatting as its reconstruction method. This task is a chance to check that number against real, publicly available imagery instead of a number I made up for the demo.

---

## Sourced footage: 6 angles, curated for reconstruction coverage

All images below are hosted on Wikimedia Commons, contributed by independent photographers, and licensed for reuse. I did not download or re-host the files; each link goes to the original file page where the exact license and photographer credit are shown.

| # | Angle | File | Why it matters for reconstruction |
|---|-------|------|-----------------------------------|
| 1 | Front facade | [Badshahi Mosque front picture.jpg](https://commons.wikimedia.org/wiki/File:Badshahi_Mosque_front_picture.jpg) | Primary reference view, establishes the main facade plane |
| 2 | Aerial / top-down | [Badshahi Mosque - Aerial View.JPG](https://commons.wikimedia.org/wiki/File:Badshahi_Mosque_-_Aerial_View.JPG) (CC BY-SA 3.0) | Gives the roofline and courtyard layout that ground-level shots cannot capture |
| 3 | Main gate / entrance | [Badshahi Masjid Main Gate.JPG](https://commons.wikimedia.org/wiki/File:Badshahi_Masjid_Main_Gate.JPG) | Adds a second structure (the gate) with its own depth relative to the mosque |
| 4 | Minaret, side angle | [Minaret of Badshahi Mosque, Lahore.JPG](https://commons.wikimedia.org/wiki/File:Minaret_of_Badshahi_Mosque,_Lahore.JPG) (CC BY-SA 4.0) | Vertical structure at a steep angle, useful for checking camera pose diversity |
| 5 | Interior, prayer hall | [Interior of Badshahi Mosque.jpg](https://commons.wikimedia.org/wiki/File:Interior_of_Badshahi_Mosque.jpg) | Interior geometry is a separate reconstruction problem from the exterior shell |
| 6 | Full structure, wide daylight | [Badshahi Masjid in the Daylight.JPG](https://commons.wikimedia.org/wiki/File:Badshahi_Masjid_in_the_Daylight.JPG) | Wide establishing shot, useful as a scale reference against the closer shots |

---

## Written piece: what this footage set tells me about reconstruction readiness

Badshahi Mosque was built between 1671 and 1673 under Emperor Aurangzeb, with construction overseen by his foster brother, Fidai Khan Koka [1]. It is built from red sandstone with white marble inlay, a departure from the tile work more common elsewhere in Lahore, and the complex includes an expansive courtyard, a prayer hall with three marble domes, and eight minarets, four major towers standing 60 meters tall and four smaller ones [1]. The courtyard alone covers about 25,600 square meters and the complex can hold 100,000 worshippers, with the prayer hall itself seating 10,000 [1]. The mosque underwent a major restoration between 1939 and 1960, and has been on UNESCO's tentative World Heritage list since 1993 [1].

None of that history is visible in a single photograph. That is the actual argument for multi-angle capture, and it is worth being specific about what six angles buys you versus what a single hero shot does not.

A front facade shot alone gives you one plane of geometry: the main archway, the flanking towers, and whatever depth cues come from shadow. It tells you almost nothing about the courtyard layout, the roofline, or how the four major minarets relate to each other in 3D space. The aerial view fixes that: it is the only shot in this set that shows the courtyard as a shape rather than an implied space behind the front wall. The main gate photo adds a second physical structure with its own depth, which matters because a reconstruction pipeline like COLMAP needs overlapping features across images, not just repeated views of the same wall from slightly different distances. The minaret shot, taken from a steep side angle, is the kind of view that a photographer instinctively avoids capturing when the goal is a nice photo, but photogrammetry needs exactly that kind of oblique, off-axis camera pose to triangulate vertical structures accurately. The interior shot is arguably the most important gap-filler: everything else in this set is exterior, and a 3D model built only from exterior photos would render the mosque as a hollow shell. The wide daylight shot works as a scale anchor, giving a full silhouette to check the other five against.

Even with six well-chosen angles, this set would not be enough to actually run COLMAP or feed a Gaussian Splatting pipeline. Production-grade reconstruction needs 50 to 300+ overlapping photos with sufficient baseline overlap between neighboring shots, not six curated highlights from different photographers using different cameras at different times of day and different focal lengths. What this set is actually useful for is a coverage audit: checking which angles exist, which are missing, and which structural elements (the back facade of the complex, the connection between the courtyard and the outer wall, the underside of the domes) still have zero photographic coverage among freely licensed images. That gap is itself a useful finding for Week 3, when the plan is to reconstruct something from curated footage: a public archive can tell you what a site looks like, but it will rarely tell you what a reconstruction pipeline actually needs.

---

## Sources

[1] [Badshahi Mosque, Wikipedia](https://en.wikipedia.org/wiki/Badshahi_Mosque), accessed 4 Jul 2026, for construction date, architect, dimensions, and preservation history. All six images are individually cited above with direct links to their Wikimedia Commons file pages, where the original photographer credit and license terms are listed per file.
