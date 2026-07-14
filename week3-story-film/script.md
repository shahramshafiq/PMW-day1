# Taxila, Preserved in 3D
### Short story video script | Team Taxila | Shahram Shafiq

**Runtime target:** ~70 seconds
**Format:** on-screen text and real project visuals, no live-action footage (this is a technical/AI track project, the "camera" here is the reconstruction pipeline itself, not a physical film camera)

---

| # | Duration | Visual | On-screen text / narration |
|---|----------|--------|------------------------------|
| 1 | 4s | Title card, dark navy background, gold text | **TAXILA, PRESERVED IN 3D**<br>Team Taxila &middot; PreserveMy.World x TechRealm 2026 |
| 2 | 5s | Real photo: Jaulian monastery ruins | 2,600 years ago, this was a center of learning. Older than Oxford. Older than Nalanda. |
| 3 | 5s | Same photo, text overlay | Today, it's a UNESCO World Heritage Site under active threat. |
| 4 | 5s | Text card | In 2026, UNESCO warned Pakistan that cement "restoration" at two Taxila sites risked the whole listing. |
| 5 | 4s | Text card | So we asked: can we preserve it a different way? |
| 6 | 6s | ML feature detection render | Step one: teach a computer to see structure. 24,091 feature points, detected automatically. |
| 7 | 6s | AR line overlay render | Step two: trace what an AR app would show a visitor live, on their phone. |
| 8 | 5s | Text card | We tested real multi-view reconstruction first. It failed honestly: only 12-17 matching points per photo pair. Not enough. |
| 9 | 6s | Capture-to-3D static render | So we built the honest alternative: a single-photo depth reconstruction. |
| 10 | 12s | Rotating point cloud sequence (real render, not a mockup) | 13,375 real 3D points. One photo. Rotating right now. |
| 11 | 5s | Text card | Not perfect. Not multi-view SfM. But real, verified, and yours to explore. |
| 12 | 5s | Text card, team credits | Built by Team Taxila: Rabeea Iman, Ruwaida Shakeel, Shahram Shafiq (lead) |
| 13 | 4s | End card | **PreserveMy.World x TechRealm 2026**<br>Full interactive version: shahramshafiq.github.io/PMW-heritage-showcase |

---

## Why this structure

A real short film needs a hook, a problem, a journey, and a resolution, this follows that shape, just built from real project artifacts instead of live-action footage:

- **Hook (1-3):** the site is old and famous, then immediately at risk, real news from this year.
- **Problem (4-5):** names the actual threat honestly, then poses the project's actual question.
- **Journey (6-9):** the real technical pipeline, including the part that failed honestly (multi-view SfM) before the part that worked.
- **Climax (10):** the one truly "live" moment, the actual rotating reconstruction, not a screenshot.
- **Resolution (11-13):** honest about limitations, credits the real team, points to where to explore it further.

## Sources for facts used in this script

Same sources already verified for the Taxila location page: the 2026 UNESCO cement-restoration warning (verified against 7+ news outlets before use), the "older than Oxford/Nalanda" framing and 12-17 SfM inlier count (both from this repo's own tested, documented work in `ml-viz-ar-capture3d/` and `week3-3d-reconstruction/`).
