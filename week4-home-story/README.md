# Individual Storytelling: What Home Means to You

**Shahram Shafiq | Week 4, Module 16 | Individual (not team) submission**

---

## What this is

A personal short film about what home means to me: three years at Cadet College Hasan Abdal (2019-2022), the routine, basketball, away fixtures with sister institutes, and the twenty guys I shared a wing with before leaving for A Levels. My own voice-over narration, synced to real footage and a licensed score.

- Script: [`script.md`](script.md)
- Build pipeline: [`build_video.py`](build_video.py)
- Final video: [`output/twenty_guys_and_a_bus_ride.mp4`](output/twenty_guys_and_a_bus_ride.mp4), 119s, 1280x720, h264 + aac

## On the footage

I don't have personal photos or video from CCH to build this from. Rather than fake that, the visual language here is honest about what it is: licensed, royalty-free B-roll used as illustrative mood footage under the narration (an empty institutional corridor, a solo basketball player, a road trip point-of-view shot, rain on a window), the way a documentary uses cutaways, not a claim that any specific frame is literally CCH. All footage is from Mixkit under the Mixkit Stock Video Free License (free for commercial and personal use, no attribution required):

- `corridor_hallway.mp4` — "Walking down a library corridor with tables and bookcases"
- `basketball_solo.mp4` — "Skilled basketball player shooting baskets, training alone"
- `bus_pov.mp4` — "Point of view from a bus passenger seat roading in a highway"
- `rainy_window.mp4` — "Window on a rainy day"

An earlier cut used a different bus clip that, on review, turned out to show people in party/nightclub styling under neon lighting, completely wrong for a story about cadets on a school fixture trip. Caught by actually watching spot-check frames rather than trusting that "a bus interior" was close enough. Replaced with a neutral road point-of-view shot before this went anywhere near a submission.

The three text-only scenes (title, "Twenty Guys," end card) are original: a warm hand-generated gradient background with film grain, not footage.

## On the score

A licensed royalty-free piano track ("Piano Reflections" by Ahjay Stelino, Mixkit Stock Music Free License, same terms as above), not procedurally synthesized. Pure numpy audio synthesis hit a real quality ceiling on an earlier project in this internship even after a full DSP rework, so this time a properly licensed real recording was used instead.

## On the voice-over and sync

The narration is Shahram's own recording (`source/voiceover_raw.mp4`, mono AAC, 113.99s), read slowly with a pause between sentences as instructed. Every scene's on-screen duration was retimed to the real recording, not the original estimate:

1. Ran `ffmpeg silencedetect` on the raw recording to find every pause, then cross-checked the biggest pauses against a word-count-weighted estimate of where each script paragraph should end. Both methods agreed to within a second, giving high confidence in four paragraph boundaries: ~9.33s, ~43.79s, ~88.87s, ~106.66s.
2. Split each paragraph's duration across its constituent scenes in proportion to their original (pre-recording) estimated share.
3. **Corrected for a real bug caught during verification**: the crossfade-concatenation shifts every scene's actual on-screen appearance earlier than the naive sum of durations (each of the 10 transitions eats 0.7s). A first pass ignored this and scenes drifted up to ~5-6 seconds out of sync with the narration by the back half of the video, caught by spot-checking frames at the target timestamps and seeing the wrong caption on screen. Fixed by solving for each scene's `duration` parameter as `(next_target_time - this_target_time) + crossfade_duration`, which correctly compensates for the compounding overlap.
4. The licensed piano score is ducked under the voice with `sidechaincompress` (keyed off the voice track, so the music dips while Shahram is talking and swells back up in the pauses and the outro) rather than just laid flat underneath it.
5. **Corrected a real audibility bug reported after the first cut**: the voice was technically present in the mix but too quiet to hear over the music, because the raw phone recording is naturally quiet (mean ~-28.6dB) and the first mix only weighted it 1.4x with no boost of its own. Fixed by boosting and gently compressing the voice track before mixing (`volume=2.6` + `acompressor`), dropping the music's base level further (0.45 to 0.20), and mixing with a much heavier voice weight. Verified objectively, not just re-tuned and assumed fixed: rendered the boosted voice and the pre-ducking music in isolation and compared mean volume in a known-speech window (40-45s) against the combined mix. Voice-alone measured louder (-23.4dB) than music-alone (-30.2dB) in that window, and the combined mix (-16.9dB) is louder than either component alone, confirming the voice is now the dominant, clearly audible element rather than just theoretically mixed in.

## Verification

Checked directly, not assumed from a clean exit code:
- `ffprobe`: confirms both video (h264, 1280x720, 24fps) and audio (aac) streams present, 119.0s container, matches on both streams.
- Frame count matches the container duration exactly.
- `ffmpeg silencedetect`: zero silence gaps anywhere in the final audio.
- `ffmpeg volumedetect` / `astats`: mean ~-11.6dB, true peak -0.5dB, no clipping.
- **Caught and fixed a real clipping bug during verification**: the first ducking/mix pass showed a 0.0dB (and after a naive fix, +0.5dB) peak. Traced it to ffmpeg's `alimiter` filter defaulting `level=true` (auto makeup-gain compensation), which was silently undoing the limiter ceiling regardless of what `limit` value was set. Fixed by explicitly setting `level=disabled`; also removed a redundant double AAC re-encode (mixed audio was being lossy-encoded twice) that was adding to the overshoot.
- **Caught and fixed a real sync bug during verification**: see "On the voice-over and sync" above, the crossfade-compounding issue.
- Spot-checked frames at multiple timestamps against the derived paragraph boundaries by actually viewing them, confirming the correct caption is on screen at each target time, not just trusting the arithmetic.

## Note on `scenes/`, `fonts/`, and `source/`

`scenes/` and `fonts/` are build artifacts regenerated by `build_video.py` (individually rendered scene clips before crossfade-concatenation, and copies of system fonts needed to avoid a Windows drive-letter escaping issue in ffmpeg's filtergraph parser) and are gitignored.

`source/` (the four downloaded B-roll clips, the piano track, and the raw voice-over) is also gitignored, the B-roll/score are downloaded stock assets, not original work product, and the repo doesn't need ~220MB of it. They're fully reproducible from the licensed direct-download URLs below (Mixkit Stock Video / Stock Music Free License, confirmed on each item's page before download); the raw voice-over is a personal recording, not reproducible from a URL, so it stays local:

- `basketball_solo.mp4`: https://assets.mixkit.co/videos/44448/44448-1080.mp4
- `corridor_hallway.mp4`: https://assets.mixkit.co/videos/21589/21589-1080.mp4
- `bus_pov.mp4`: https://assets.mixkit.co/videos/4394/4394-1080.mp4
- `rainy_window.mp4`: https://assets.mixkit.co/videos/2846/2846-1080.mp4
- `piano_reflections.mp3`: https://assets.mixkit.co/music/22/22.mp3

The real, original inputs are `script.md` and `build_video.py`. The real output is `output/twenty_guys_and_a_bus_ride.mp4`.
