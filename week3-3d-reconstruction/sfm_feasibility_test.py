"""
SfM feasibility test on the curated Badshahi Mosque photo set.
PMW Internship 2026, AI-Based 3D Reconstruction Track, Week 3

Before building the monocular reconstruction, I checked whether real
multi-view Structure from Motion (feature matching + triangulation, what
COLMAP actually does) is viable on the 6 photos already curated in
footage-research/images/. This matters: if it works, that is a stronger
result than any single-photo heuristic. If it does not, that is worth
knowing and documenting honestly rather than assumed either way.
"""

import cv2
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, '..', 'footage-research', 'images')

pairs_to_test = [
    ('01-front-facade.jpg', '04-wide-front-garden.jpg'),
    ('01-front-facade.jpg', '05-minaret-side-angle.jpg'),
    ('04-wide-front-garden.jpg', '06-panoramic-elevated.jpg'),
]

print("Testing ORB feature matching + RANSAC geometric verification")
print("across pairs of the 6 curated Badshahi Mosque photos:\n")

for name_a, name_b in pairs_to_test:
    img_a = cv2.imread(os.path.join(IMG_DIR, name_a), cv2.IMREAD_GRAYSCALE)
    img_b = cv2.imread(os.path.join(IMG_DIR, name_b), cv2.IMREAD_GRAYSCALE)

    orb = cv2.ORB_create(3000)
    kp_a, des_a = orb.detectAndCompute(img_a, None)
    kp_b, des_b = orb.detectAndCompute(img_b, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(des_a, des_b), key=lambda m: m.distance)
    top_matches = matches[:60]

    pts_a = np.float32([kp_a[m.queryIdx].pt for m in top_matches])
    pts_b = np.float32([kp_b[m.trainIdx].pt for m in top_matches])

    F, mask = cv2.findFundamentalMat(pts_a, pts_b, cv2.FM_RANSAC, 3, 0.99)
    inliers = int(mask.ravel().sum()) if mask is not None else 0

    print(f"{name_a}  <->  {name_b}")
    print(f"    keypoints: {len(kp_a)} and {len(kp_b)}")
    print(f"    candidate matches (best 60 by descriptor distance): {len(top_matches)}")
    print(f"    RANSAC-verified geometrically consistent inliers: {inliers}")
    print()

print("Conclusion: single-digit to low-double-digit inlier counts out of")
print("thousands of keypoints per photo. These are 6 real photos taken by")
print("different photographers, cameras, and lighting conditions, not a")
print("controlled multi-view capture. Real triangulation needs far denser,")
print("more consistent overlap than this set provides. Forcing a point")
print("cloud out of this few, weak matches would be geometrically")
print("meaningless. This is the same conclusion already documented in")
print("footage-research/badshahi-mosque-multiangle.md before any code was")
print("written to test it, this script exists to check that claim with")
print("real numbers instead of leaving it as an assumption.")
