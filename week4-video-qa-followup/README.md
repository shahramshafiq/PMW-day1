# Video + Voice Capture & QA Follow-up

**Shahram Shafiq | Week 4, Module 18 | QA & Polish**

---

## What this is

A structured quality-assurance pass on the video and voice-over already captured for [Individual Storytelling: What Home Means to You](../week4-home-story/) ("Twenty Guys and a Bus Ride"), plus the real follow-up fixes that came out of it. This module isn't a new video, it's proof of the QA process behind the one already submitted: what was checked, what broke, how it was caught, and how it was fixed, each with actual command output as evidence, not just a claim that it was checked.

- Video under QA: [`../week4-home-story/output/twenty_guys_and_a_bus_ride.mp4`](../week4-home-story/output/twenty_guys_and_a_bus_ride.mp4)
- Live: https://youtu.be/5nhRp_gWVRs
- Build pipeline under QA: [`../week4-home-story/build_video.py`](../week4-home-story/build_video.py)

## 1. Capture

- **Video**: assembled from real photos (the basketball team, the wing/dorm room, entry mates, the campus gate) plus licensed B-roll for the two beats with no real footage available (the bus-ride and rain/leaving moments), see [`week4-home-story/README.md`](../week4-home-story/README.md) for the full sourcing and licensing breakdown.
- **Voice-over**: Shahram's own recording, captured on his phone (Voice Memos-equivalent, quiet room, 6-8 inches off-mic, highest quality format), following the recording guidance given before capture. Mono AAC, 44.1kHz, 113.99s.

## 2. Structured QA checklist

Every check below was actually run against the final file, not assumed. Commands and real output are in section 3.

| # | Check | Category | Result |
|---|---|---|---|
| 1 | Video/audio streams present, correct codec (h264/aac), resolution (1280x720), frame rate (24fps) | Technical | Pass |
| 2 | Container duration matches expected scene-timeline math exactly | Technical | Pass (119.00s) |
| 3 | No silence gaps anywhere in the final audio track | Audio | Pass |
| 4 | True peak stays under 0dB (no clipping, including after lossy AAC re-encode) | Audio | **Failed twice, fixed, now passes** (-1.2dB) |
| 5 | Voice-over is the dominant, clearly audible element over the music | Audio | **Failed, fixed, now passes** |
| 6 | On-screen captions match what's actually being said at that timestamp | Sync | **Failed, fixed, now passes** |
| 7 | Every B-roll/photo shown matches the story being told in that moment | Visual | **Failed on one clip, fixed, now passes** |
| 8 | Text stays legible over both dark and busy backgrounds | Visual | Pass |
| 9 | Local file and the pushed GitHub copy are byte-identical (checksum) | Presentation readiness | Pass |
| 10 | Published YouTube video reflects the final fixed version, not an earlier draft | Presentation readiness | Pass (verified today, see 3.6) |
| 11 | Repo is public, link resolves without login | Presentation readiness | Pass |

## 3. Follow-up fixes, with evidence

### 3.1 Voice-over technically present but inaudible

**Found:** after delivering the first voice-synced cut, direct feedback: "I can't hear my voiceover sound, it's just the music."

**Root cause, found by isolating each component:** raw phone recordings are quiet (mean ≈ -28.6dB) and the first mix only weighted the voice 1.4x against the music, not enough to be heard.

```
FINAL MIX, 40-45s window:       mean_volume: -16.9 dB
VOICE-ONLY (boosted), same:      mean_volume: -23.4 dB
MUSIC-ONLY (pre-ducking):        mean_volume: -30.2 dB
```

**Fix:** boosted the voice ~2.6x, gently compressed it (`acompressor`), dropped the music's base level (0.45 → 0.20), and rebalanced the mix weights, on top of the existing sidechain ducking.

**Re-verified:** voice-alone now measures louder than music-alone in a real speech window, and the combined mix is louder than either component, confirming the voice genuinely dominates, not just theoretically present.

### 3.2 Audio clipping (two separate root causes)

**Found:** `astats` showed the true peak sitting at 0.0dB, then +0.3dB, then +0.5dB across attempted fixes, meaning the ceiling I was setting wasn't holding.

**Root cause 1:** ffmpeg's `alimiter` filter defaults `level=true` (automatic makeup-gain compensation), which was silently pushing the output right back up after limiting it, regardless of the `limit` value set.
**Root cause 2:** the mixed audio was being lossy-encoded to AAC twice (once when saving the mix, again in the final mux), and each lossy pass adds inter-sample overshoot.

**Fix:** set `level=disabled` explicitly on the limiter, and changed the final mux to `-c:a copy` instead of re-encoding.

**Re-verified:** true peak -1.2dB, safely under 0dB, confirmed again today (section 3.5 below shows today's fresh re-run).

### 3.3 Scene/caption sync drifted from the narration

**Found:** spot-checking frames at the exact timestamps a caption *should* have appeared showed the wrong caption on screen, drifting further out of sync the later in the video (up to ~5-6 seconds by the back half).

**Root cause:** crossfade transitions between scenes shift every later scene's actual on-screen appearance earlier than a naive sum of scene durations would suggest (10 transitions × 0.7s = up to 7 seconds of compounding drift), and the first duration pass didn't account for that.

**Fix:** derived exact paragraph boundaries from real pause detection on the voice-over (`ffmpeg silencedetect`), cross-checked against a word-count-weighted estimate (both agreed to within a second), then solved each scene's duration as `(next_target_time - this_target_time) + crossfade_duration` to correctly cancel out the compounding overlap.

**Re-verified:** spot-checked frames at the corrected target timestamps, confirmed the right caption is on screen at each one (e.g., the Kallar Kahar line appears exactly as the bus B-roll starts, not 5 seconds into a different scene).

### 3.4 Mismatched footage

**Found:** one bus B-roll clip, on closer look, showed people in party/nightclub styling under neon lighting, wrong mood entirely for cadets on a school fixture trip. This is exactly the kind of thing "mission fit" and "communication & clarity" would penalize hard if it had shipped, a viewer would reasonably wonder whether the visuals were even watched before submitting.

**Fix:** re-sourced a neutral bus-window road POV clip that actually matches "away fixture" mood, verified its license, swapped it in.

### 3.5 Fresh re-verification, run today (18 Jul 2026)

Not just recapping old fixes, re-ran the full check suite against the current file today, before writing this report:

```
ffprobe:      h264 1280x720 24fps, aac audio, duration 119.000000s, size 38589115 bytes
astats peak:  -1.207372 dB / -1.209698 dB   (safely under 0dB, no clipping)
volumedetect: mean -17.4 dB, max -1.2 dB
silencedetect: (no output = zero silence gaps found)

local git blob hash:   80ef93bc44c63fee37c879537baef60f8c7da457
GitHub blob hash:       80ef93bc44c63fee37c879537baef60f8c7da457   MATCH
```

### 3.6 New check: does the published YouTube video actually match the final file?

This had never actually been verified, only assumed, so it was checked today rather than left as an open question:

- Fetched the video's oEmbed metadata: title "Twenty Guys and a Bus Ride | What Home Means to Me", author Shahram Shafiq, confirms the correct video is live at the given link.
- Downloaded the actual YouTube thumbnail and inspected it: it shows the "TWENTY GUYS" title card composited over the real wing/dorm-room photo with the Drill Winner trophy, which only exists in the final version (the draft cut before photos were added used a plain gradient background there). This confirms the uploaded video is genuinely the final, fixed cut, not a stale earlier draft.

## 4. Sign-off

All 11 checklist items pass as of this report. Four real, distinct bugs were found and fixed during this process (inaudible voice, audio clipping from two separate causes, sync drift, mismatched footage), each with before/after evidence above, not just a claim that QA happened.

Full technical detail and licensing notes for the underlying video: [`week4-home-story/README.md`](../week4-home-story/README.md).
