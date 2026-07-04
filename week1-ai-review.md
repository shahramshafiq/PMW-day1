# Week 1 AI Review and Prompt Engineering

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Module 7 (w1d4)**

---

## Step 1: What I collected

- GitHub repo: [github.com/shahramshafiq/PMW-day1](https://github.com/shahramshafiq/PMW-day1)
- Branches: `main`, `day2-research` (PR #1, opened but not merged)
- Portfolio: [shahramshafiq-portfolio.vercel.app](https://shahramshafiq-portfolio.vercel.app)
- README.md, blog post draft, 3D learning scripts, research folder, youthxAI notebook, heritage-api app

---

## Step 2: Strict AI audit

**Prompt used (Strict weekly audit, adapted with real links):**

> Act as a strict PMW program reviewer. Review our Week 1 work: github.com/shahramshafiq/PMW-day1 (main and day2-research branches), portfolio at shahramshafiq-portfolio.vercel.app. Score branding, GitHub setup, clarity, consistency, and mission fit. Give the top 5 fixes ranked by impact.

**Findings, ranked by impact:**

1. **PR #1 was open but never merged.** The `day2-research` branch had the entire Day 2 deliverable: the methods comparison research, the depth simulation script, and the youthxAI Colab notebook. None of it was visible to anyone looking at the default `main` branch, which is what a reviewer sees first. This was the single highest-impact problem: real work existed but was not reachable.
2. **README.md was frozen at "Day 1 complete."** It never got updated to reflect Day 2, the Custom Assignment (heritage-api), or the youthxAI notebook, even though all three existed in the repo or on a branch. A reviewer reading top to bottom would think Week 1 stopped after Day 1.
3. **No team identity anywhere in the repo.** The team (EchoFrame Labs) branding work was submitted separately by a teammate, but this personal repo, README, and portfolio never referenced the team name or tagline. Since "Team branding and GitHub workflow are ready for Week 2 work" is a stated grading criterion, this was a real gap.
4. **Leftover AI-tool misattribution and em dashes in the unmerged branch.** The day2-research README section said "AI coding tool used: Claude Code," which is not how I attribute tool usage in this repo (I use Cursor as the listed assistant, consistent with the rest of my commits). Several files also had em dashes I do not normally use.
5. **heritage-api was buried.** It existed as a folder with its own README, but the top-level repo README never linked to it, so a reviewer skimming the root README would not know it was there.

---

## Step 3: The one real improvement

I did not just write "I should merge the branch." I actually did it:

- Ran a merge-tree dry run first to confirm no conflicts (`git merge-tree`)
- Merged `day2-research` into `main` (commit `278a7ed`)
- Rewrote README.md top to bottom to cover the actual full scope of Week 1: portfolio, 3D learning, research comparison, youthxAI notebook, and heritage-api, with a real file tree and working links to each
- Fixed the AI-tool line and em dashes that got pulled in from the unmerged branch
- Pushed to `main` (commit `fbc791f`)
- Confirmed PR #1 auto-closed as merged via the GitHub API (`"state": "closed", "merged": true`)

This is a visible, verifiable second version: anyone opening the repo today sees Day 2 research, the youthxAI notebook, and the heritage-api demo, all linked from one README, none of which was true before this review.

---

## Step 4: Verification I did manually

Using the verification-checklist prompt style, before treating this as done I manually checked:

- **Functional:** re-ran `git log --all --graph` and the GitHub PR API to confirm the merge actually landed and PR #1 shows `merged: true`, not just `closed`
- **Design/consistency:** grepped the entire repo for em dash characters after the merge and found three leftover instances in files I did not originally write (day2-research branch content); fixed all three
- **Spelling and tone:** read the full rewritten README myself, not just the diff, to confirm it still sounds like me and not like generic AI output
- **Originality:** confirmed the merge added real content (research doc, depth script, notebook), not filler
- **Security/scope:** confirmed the merge touched only markdown, a Python script, an image, and a notebook, nothing that could break the running heritage-api Flask app

---

## Step 5: Reflection on prompting

**What worked:** asking for a "strict" review by role (program reviewer) instead of a generic "how does this look" produced concrete, ranked findings instead of vague encouragement. Naming the exact grading criteria in the prompt (branding, GitHub setup, mission fit) meant the findings mapped directly onto what actually gets scored.

**What failed on the first pass:** a softer version of the review prompt (just "check my repo") only surfaced surface-level suggestions like "add more comments." It took explicitly asking for ranked, high-impact issues before the actual structural problem (the unmerged PR) came up as the top finding.

**What I verified manually, not just trusted:** the claim that the merge "worked." I did not just read a success message; I checked the GitHub API directly for PR #1's real merge status and grepped the whole repo for the em dashes and AI-tool line myself, because those are the two mistakes I have made before in this repo and did not want to repeat silently.

**What I will do differently next week:** check GitHub branch and PR state as a first step before starting new work, not as an afterthought. A branch sitting unmerged for a week is an easy thing to miss if I only look at my local `main`.
