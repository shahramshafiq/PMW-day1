# Special: Story, Script, Film & Edit

**Shahram Shafiq | AI-Based 3D Reconstruction Track | Week 3 Special Session**

---

## What this is

This is an AI-based 3D reconstruction project, there is no camera and no live-action filming here. Rather than fake that, this builds the honest equivalent: a real, playable video file assembled entirely from genuine project artifacts, a real photo, real generated visualizations, and a real rotating render of the actual `.ply` point cloud, following a proper written script, with real synthesized audio design and motion, not a plain silent slideshow.

- Script: [`script.md`](script.md)
- Build script: [`build_video.py`](build_video.py)
- Final video: [`output/taxila_preserved_in_3d.mp4`](output/taxila_preserved_in_3d.mp4) (75 seconds, 1280x720, h264 video + aac audio)

---

## On the voiceover

The team discussed this directly: having only one of three teammates record a voiceover would look uneven when the others didn't, so the team decision was no voiceover, but the video should not be plain or silent either. What's here instead is real production value built without one:

- **A synthesized ambient pad** running under the whole video (procedurally generated with numpy, a slow three-note minor-key drone, each note chorus-detuned across two voices plus a soft octave overtone, filtered through a Butterworth lowpass for warmth, a touch of algorithmic reverb, and gentle tremolo, not licensed music, not claimed to be)
- **Whoosh transitions** at every scene change
- **A reveal chime** at the exact moment the live 3D point cloud first appears, the emotional climax of the video (near-harmonic bell partials with independent decay rates, lowpass filtered and reverbed for a soft tone instead of a harsh buzz)
- **A low tension rumble** under the UNESCO warning scene
- **A descending "failure" stinger** at the beat where the video admits multi-view reconstruction didn't work
- **Ken Burns slow zoom** on every photo and render card instead of a frozen still
- **Crossfade dissolves** between every scene instead of hard cuts
- **Fade in/out text** instead of text just appearing and disappearing

All of it verified after building, not just assumed to have worked, see below.

---

## Bugs caught by actually checking, not by trusting a clean exit code

**v1, bug 1:** an extra 12 frames from a `repeat_frame()` helper that copied a source card into the sequence but never deleted the original, adding 0.5s of drift. Fixed by deleting the source after use and adding an assertion that checks the actual frame count on disk against the expected total.

**v1, bug 2, the serious one:** the entire video played back scrambled, completely out of scene order. Cause: frame filenames zero-padded to 3 digits, but the sequence needed 1704 frames, past 999. Python's format spec doesn't truncate for larger numbers, so frame 1080 became `"1080_..."` rather than `"080_..."`, and once filename lengths differ, alphabetical sort stops matching numeric order. Fixed by padding to 5 digits everywhere. Verified by extracting 9 frames across the timeline and confirming each matched its intended scene, including two different timestamps inside the rotation to confirm real rotation.

**v2, re-verified from scratch since the frame-building logic changed substantially:**
- Extracted 9 frames at the recalculated scene timestamps (crossfades shift every scene's start time) and confirmed every one is in the correct order again.
- Confirmed the rotation is still genuinely animating (two different timestamps show different angles).
- Ran `ffprobe` to confirm both a video stream (h264) and an audio stream (aac, 44.1kHz) are actually present and the container plays as a real 75.0-second file.
- Ran `ffmpeg silencedetect` on the audio: zero silent gaps found, the ambient bed is genuinely continuous.
- Ran `ffmpeg volumedetect` on the audio: max level -10 dB (headroom, no clipping), and confirmed real dynamic variation by comparing the reveal-chime moment (mean -24.3 dB) against a quiet text-only scene (mean -28.7 dB), so the audio design is actually doing something, not a flat unchanging tone.

**v3 (this version): reworked the ambient pad and chime, both sounded thin and harsh in v2.** Rebuilt both with chorus-detuned voices, a soft octave overtone, a Butterworth lowpass filter to cut harsh high content, a small algorithmic reverb tail (a few decaying delayed copies summed back in), and gentle tremolo on the pad. Frame generation and scene timing are untouched (still exactly 1800 frames, 75.00s), so only the audio needed re-checking:
- `ffprobe` confirms both streams intact, 75.0s container.
- `ffmpeg silencedetect` found zero silent gaps.
- `ffmpeg volumedetect` on the full track: mean -30.7 dB, max -12.1 dB, no clipping.
- Plotted a full 1-second-window RMS loudness profile across all 75 seconds (not just two spot checks) using numpy directly on the raw samples: loudness genuinely swings between roughly -22 dB (chime and transition moments) and -40 dB (quiet stretches) throughout the track, confirmed against the actual sample data, not assumed from the code.

---

## Facts used in the script

- Taxila (Takshashila) dates to roughly 600 BCE, predating Oxford (1096 CE) by about 1,700 years and predating Nalanda, independently verified before writing the script.
- The 2026 UNESCO cement-restoration warning and the 12-17 SfM inlier count are both already verified and documented elsewhere in this repo (`ml-viz-ar-capture3d/`, `week3-3d-reconstruction/`).

---

## Note on `frames/`

The `frames/` folder is regenerated by `build_video.py` (1800 PNG frames, roughly 350 MB) and is gitignored, it is a build artifact, not part of the deliverable. Run the script to regenerate it if needed; the final video in `output/` is the actual submission.
