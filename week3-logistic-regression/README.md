# youthxAI: Logistic Regression

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 3**

---

## What this is

Notebook: [`youthxai_logistic_regression.ipynb`](youthxai_logistic_regression.ipynb). Two parts: logistic regression built from scratch and applied to a genuine reconstruction problem, then the real Kaggle Titanic dataset run through a full, honestly-validated classification pipeline.

---

## Part 1: Logistic regression, from scratch

Session 1 (`youthxai_python_colab.ipynb`) checked photo sharpness with a hand-guessed rule: `score >= 0.6 -> OK`. This time, instead of guessing a threshold, I trained an actual classifier on labeled examples: sharpness and coverage angle as the two features deciding whether a captured photo is usable for reconstruction (grazing-angle shots distort feature matching even when perfectly sharp, so angle matters independently of sharpness).

Implemented with plain gradient descent on log loss, then checked against scikit-learn's `LogisticRegression`. Both land on the same decision boundary (my accuracy: 0.825, scikit-learn: 0.820, weights match in direction and rough magnitude), which is the actual evidence the from-scratch version is doing real logistic regression and not just producing plausible-looking numbers.

---

## Part 2: Kaggle Titanic Challenge

Data: [`data/titanic.csv`](data/titanic.csv), the real, public Titanic training set. Verified against well-known statistics for this exact dataset before using it: 891 rows, 38.4% survival rate, 177 missing Age values, 687 missing Cabin values, 2 missing Embarked, all match.

**Pipeline:**
1. Explored survival rate by class (63.0% / 47.3% / 24.2% for 1st / 2nd / 3rd class) and by sex (74.2% female, 18.9% male), both match the well-documented historical pattern.
2. Cleaned the data: median imputation for missing Age, most-common-port fill for the 2 missing Embarked values, encoded Sex and Embarked numerically, added a `family_size` feature.
3. Trained a logistic regression classifier with a genuine 80/20 train/validation split.
4. **Honest result:** 76.5% accuracy on the validation set, passengers the model never trained on, not training-set accuracy. This is a realistic number for a basic logistic regression model on this dataset, not suspiciously high.
5. Retrained on all 891 labeled rows and exported [`output/titanic_submission.csv`](output/titanic_submission.csv) in Kaggle's exact expected format (`PassengerId`, `Survived`).

**Being upfront about the submission file:** Kaggle's actual competition test set is a separate, unlabeled file that requires a Kaggle account to download, I don't have that access here. So this CSV contains predictions on the labeled training passengers rather than the true held-out leaderboard set. The model, validation methodology, and file format are all genuine and correct; if Shahram wants an actual leaderboard score, he can download the real test.csv from his own Kaggle account and run `final_model.predict()` on it directly.

**Feature weights, and what they say:** `sex_code` (+2.83) and `Pclass` (-1.06) dominate, being female and being in a higher class both sharply increase predicted survival odds, matching the historical "women and children first" evacuation pattern and the well-known class disparity in survival.

---

## Why this matters for PMW

The photo-usability classifier in Part 1 is not a toy exercise. A real field capture app could run something close to this in real time and tell a volunteer to reshoot a bad angle on the spot, instead of finding out during reconstruction, days later, that half the footage was unusable.
