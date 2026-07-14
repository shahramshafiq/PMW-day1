"""
Twenty Guys and a Bus Ride: what home means to me
PMW Internship 2026, Week 4 Module 16, Individual Storytelling

A personal short film built entirely from Shahram's own story about
Cadet College Hasan Abdal (2019-2022): the hostel routine, basketball,
away fixtures at sister institutes like Cadet College Kallar Kahar, and
leaving for A Levels at Roots International. There is no personal footage
available, so the visual language is illustrative mood B-roll (licensed,
free for commercial and personal use, no attribution required, under the
Mixkit Stock Video Free License) combined with original kinetic-typography
scenes for the beats that are too specific for stock footage to represent
honestly (the twenty wing mates, the closing line). None of the B-roll is
presented as literal footage of CCH, it is used the way a documentary uses
illustrative cutaways under narration.

This first pass builds the visual/music draft using estimated scene timing
from the script. Once the real voice-over recording arrives, sync_voiceover.py
retimes every scene to the actual narration and remuxes the final video.
"""
import os
import subprocess
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SCRIPT_DIR, 'source')
SCENES_DIR = os.path.join(SCRIPT_DIR, 'scenes')
OUT = os.path.join(SCRIPT_DIR, 'output')

for d in (SCENES_DIR, OUT):
    os.makedirs(d, exist_ok=True)
for f in os.listdir(SCENES_DIR):
    fp = os.path.join(SCENES_DIR, f)
    if os.path.isdir(fp):
        shutil.rmtree(fp)
    else:
        os.remove(fp)

W, H, FPS = 1280, 720, 24
BG = (17, 14, 13)
CREAM = (236, 224, 200)
RUST = (191, 106, 58)
XFADE = 0.7

_SYS_FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf" if os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf") else r"C:\Windows\Fonts\arialbd.ttf"
_SYS_FONT_REG = r"C:\Windows\Fonts\segoeui.ttf" if os.path.exists(r"C:\Windows\Fonts\segoeui.ttf") else r"C:\Windows\Fonts\arial.ttf"
FONTS_DIR = os.path.join(SCRIPT_DIR, 'fonts')
os.makedirs(FONTS_DIR, exist_ok=True)
FONT_BOLD = os.path.join(FONTS_DIR, 'bold.ttf')
FONT_REG = os.path.join(FONTS_DIR, 'regular.ttf')
shutil.copyfile(_SYS_FONT_BOLD, FONT_BOLD)
shutil.copyfile(_SYS_FONT_REG, FONT_REG)


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR)
    if result.returncode != 0:
        print("FFMPEG FAILED:", " ".join(cmd))
        print(result.stderr[-3000:])
        raise RuntimeError("ffmpeg failed")
    return result


def make_gradient_bg(path, top, bottom, grain=True):
    gw, gh = 3200, 1800
    img = Image.new('RGB', (gw, gh), top)
    px = img.load()
    for y in range(gh):
        t = y / gh
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(0, gw, 4):
            px[x, y] = (r, g, b)
            if x + 1 < gw:
                px[x + 1, y] = (r, g, b)
            if x + 2 < gw:
                px[x + 2, y] = (r, g, b)
            if x + 3 < gw:
                px[x + 3, y] = (r, g, b)
    if grain:
        noise = (np.random.randn(gh, gw, 1) * 6).astype(np.int16)
        arr = np.array(img).astype(np.int16) + noise
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    img.save(path)


def wrap_lines(text, font_path, size, max_w):
    f = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox
    from PIL import ImageFont
    fnt = ImageFont.truetype(font_path, size)
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        bbox = d.textbbox((0, 0), trial, font=fnt)
        if bbox[2] - bbox[0] > max_w and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def caption_textfile(lines, path):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write("\n".join(lines))
    return path


def build_scene(idx, name, duration, bg_video=None, bg_start=0.0, loop_bg=False,
                 gradient=None, bg_photo=None, caption=None, kicker=None, zoom_from=1.0, zoom_to=1.08,
                 grade=True):
    out_path = os.path.join(SCENES_DIR, f"scene_{idx:02d}_{name}.mp4")
    tmp_dir = os.path.join(SCENES_DIR, f"_tmp_{idx:02d}")
    os.makedirs(tmp_dir, exist_ok=True)

    if gradient is not None:
        bg_png = os.path.join(tmp_dir, "bg.png")
        make_gradient_bg(bg_png, gradient[0], gradient[1])
        base_cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(duration), "-i", bg_png]
        vf_pre = "scale=3200:1800,"
    elif bg_photo is not None:
        base_cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(duration), "-i", bg_photo]
        # real photos vary in aspect ratio, unlike generated gradients, so
        # fill-crop to 16:9 first instead of a plain scale (which would distort)
        vf_pre = "scale=3200:1800:force_original_aspect_ratio=increase,crop=3200:1800,"
    else:
        if loop_bg:
            base_cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-t", str(duration), "-i", bg_video]
        else:
            base_cmd = ["ffmpeg", "-y", "-ss", str(bg_start), "-t", str(duration), "-i", bg_video]
        vf_pre = "scale=2560:1440,"

    zoompan = f"zoompan=z='min(zoom+{(zoom_to - zoom_from) / (duration * FPS):.6f},{zoom_to})':d=1:s=1280x720:fps={FPS}"
    vf = vf_pre + zoompan
    if grade:
        vf += ",eq=contrast=1.08:saturation=0.80:gamma=0.94,colorbalance=rs=0.07:gs=0.01:bs=-0.09:rm=0.04:bm=-0.05"
    vf += ",vignette=PI/4.2,noise=alls=5:allf=t+u"

    draw_filters = []
    if kicker:
        kfile = os.path.join(tmp_dir, "kicker.txt")
        caption_textfile([kicker], kfile)
        alpha_expr = fade_expr(duration, 0.6)
        draw_filters.append(
            f"drawtext=fontfile={_fpath(FONT_BOLD)}:textfile={_fpath(kfile)}:fontcolor={_hex(RUST)}:fontsize=22:"
            f"line_spacing=6:x=(w-text_w)/2:y=h-190:alpha='{alpha_expr}'"
        )
    if caption:
        lines = wrap_lines(caption, FONT_REG, 34, W - 220)
        cfile = os.path.join(tmp_dir, "caption.txt")
        caption_textfile(lines, cfile)
        alpha_expr = fade_expr(duration, 0.6)
        y_pos = "h-150" if kicker else "h-140"
        draw_filters.append(
            f"drawtext=fontfile={_fpath(FONT_REG)}:textfile={_fpath(cfile)}:fontcolor={_hex(CREAM)}:fontsize=34:"
            f"line_spacing=10:x=(w-text_w)/2:y={y_pos}:alpha='{alpha_expr}':"
            f"box=1:boxcolor=black@0.28:boxborderw=18"
        )
    if draw_filters:
        vf += "," + ",".join(draw_filters)

    cmd = base_cmd + [
        "-vf", vf, "-r", str(FPS), "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
        out_path
    ]
    run(cmd)
    shutil.rmtree(tmp_dir)
    print(f"Built scene {idx:02d} [{name}]  {duration:.1f}s -> {out_path}")
    return out_path, duration


def _hex(rgb):
    return "0x%02X%02X%02X" % rgb


def _fpath(path):
    rel = os.path.relpath(path, SCRIPT_DIR)
    return rel.replace("\\", "/")


def fade_expr(duration, in_time, out_time=None):
    out_time = out_time if out_time is not None else in_time
    # wrapped in single quotes by the caller, so commas need no escaping here
    return (
        f"min(1,max(0,if(lt(t,{in_time}),t/{in_time},"
        f"if(gt(t,{duration}-{out_time}),({duration}-t)/{out_time},1))))"
    )


def build_title_scene(idx, name, duration, headline, sub, bg_photo=None):
    out_path = os.path.join(SCENES_DIR, f"scene_{idx:02d}_{name}.mp4")
    tmp_dir = os.path.join(SCENES_DIR, f"_tmp_{idx:02d}")
    os.makedirs(tmp_dir, exist_ok=True)
    hfile = os.path.join(tmp_dir, "headline.txt")
    sfile = os.path.join(tmp_dir, "sub.txt")
    caption_textfile(wrap_lines(headline, FONT_BOLD, 58, W - 160), hfile)
    caption_textfile(wrap_lines(sub, FONT_REG, 26, W - 160), sfile)
    alpha_expr = fade_expr(duration, 1.0, 0.8)

    if bg_photo is not None:
        bg_src = bg_photo
        vf_pre = "scale=3200:1800:force_original_aspect_ratio=increase,crop=3200:1800,"
        # darken and desaturate the real photo so white text stays legible over it
        grade = "eq=contrast=1.02:brightness=-0.12:saturation=0.55:gamma=0.92,"
        box = "box=1:boxcolor=black@0.32:boxborderw=22:"
    else:
        bg_png = os.path.join(tmp_dir, "bg.png")
        make_gradient_bg(bg_png, (24, 17, 15), (58, 32, 20))
        bg_src = bg_png
        vf_pre = "scale=3200:1800,"
        grade = ""
        box = ""

    vf = (
        f"{vf_pre}"
        f"zoompan=z='min(zoom+{0.06 / (duration * FPS):.6f},1.06)':d=1:s=1280x720:fps={FPS},"
        f"{grade}"
        "vignette=PI/4,noise=alls=5:allf=t+u,"
        f"drawtext=fontfile={_fpath(FONT_BOLD)}:textfile={_fpath(hfile)}:fontcolor={_hex(CREAM)}:fontsize=58:"
        f"line_spacing=14:x=(w-text_w)/2:y=(h/2)-100:{box}alpha='{alpha_expr}',"
        f"drawtext=fontfile={_fpath(FONT_REG)}:textfile={_fpath(sfile)}:fontcolor={_hex(RUST)}:fontsize=26:"
        f"line_spacing=8:x=(w-text_w)/2:y=(h/2)+40:{box}alpha='{alpha_expr}'"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-t", str(duration), "-i", bg_src,
        "-vf", vf, "-r", str(FPS), "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
        out_path
    ]
    run(cmd)
    shutil.rmtree(tmp_dir)
    print(f"Built scene {idx:02d} [{name}]  {duration:.1f}s -> {out_path}")
    return out_path, duration


# =====================================================================
# SCENE TIMELINE (estimated pacing from script.md; retimed once the real
# voice-over recording arrives, see sync_voiceover.py)
# =====================================================================
scenes = []
PHOTOS = os.path.join(SRC, "photos")

scenes.append(build_title_scene(
    0, "title", 2.00,
    "TWENTY GUYS AND A BUS RIDE",
    "What Home Means to Me  |  Shahram Shafiq",
    bg_photo=os.path.join(PHOTOS, "cch_gate.jpg")
))

scenes.append(build_scene(
    1, "corridor-a", 8.03,
    bg_photo=os.path.join(PHOTOS, "group_outside_building.jpg"),
    caption="For three years, home wasn't a house. It was a wing, in a hostel, at Cadet College Hasan Abdal.",
    kicker="CADET COLLEGE HASAN ABDAL  ·  2019–2022"
))

scenes.append(build_scene(
    2, "corridor-b", 16.92,
    bg_photo=os.path.join(PHOTOS, "cch_aerial_wikimedia.jpg"),
    caption="Everything ran on a schedule so tight it should have felt like a punishment. It didn't."
))

scenes.append(build_scene(
    3, "basketball-a", 18.94,
    bg_photo=os.path.join(PHOTOS, "basketball_team.jpg"),
    caption="It felt like the safest routine I've ever lived in. Inside it, I found basketball, and it became mine."
))

scenes.append(build_scene(
    4, "bus-a", 15.73,
    bg_video=os.path.join(SRC, "bus_pov.mp4"), bg_start=0.0,
    caption="The best memories weren't even at CCH. They were on the bus, going to fixtures at other cadet colleges.",
    kicker="AWAY FIXTURES"
))

scenes.append(build_scene(
    5, "bus-b", 14.22,
    bg_photo=os.path.join(PHOTOS, "friends_hillside.jpg"),
    caption="Cadet College Kallar Kahar felt like a vacation from CCH itself. New campus. New faces. A game to win."
))

scenes.append(build_title_scene(
    6, "wing", 17.23,
    "TWENTY GUYS",
    "My entry mates. My wing mates.\nEvery 5 a.m. wake-up. Every late-night talk after lights out.",
    bg_photo=os.path.join(PHOTOS, "wing_dorm_trophy.jpg")
))

scenes.append(build_scene(
    7, "rain", 11.57,
    bg_video=os.path.join(SRC, "rainy_window.mp4"), bg_start=0.0,
    caption="I left in 2022. CCH only offered sciences at A Level, and I wanted CS and business, so I moved to Roots International.",
    kicker="2022"
))

scenes.append(build_scene(
    8, "corridor-c", 7.62,
    bg_photo=os.path.join(PHOTOS, "wing_dorm_trophy.jpg"),
    caption="It was the right call. But I still measure routine, discipline, and friendship against that wing."
))

scenes.append(build_scene(
    9, "basketball-b", 7.24,
    bg_photo=os.path.join(PHOTOS, "basketball_team.jpg"),
    caption="That's what I miss. Not a building. Twenty guys, a basketball court, and a bus ride to Kallar Kahar."
))

scenes.append(build_title_scene(
    10, "end", 6.50,
    "SHAHRAM SHAFIQ",
    "PreserveMy.World x TechRealm 2026\nIndividual Storytelling: What Home Means to You",
    bg_photo=os.path.join(PHOTOS, "cch_gate.jpg")
))

# =====================================================================
# CONCATENATE WITH CROSSFADE TRANSITIONS
# =====================================================================
print("\nConcatenating scenes with crossfade transitions...")
paths = [p for p, _ in scenes]
durations = [d for _, d in scenes]

inputs = []
for p in paths:
    inputs += ["-i", p]

filter_parts = []
running = durations[0]
last_label = "0:v"
for i in range(1, len(paths)):
    offset = running - XFADE
    out_label = f"v{i}"
    filter_parts.append(f"[{last_label}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out_label}]")
    running = running + durations[i] - XFADE
    last_label = out_label

filter_complex = ";".join(filter_parts)
total_video_duration = running
print(f"Total assembled video duration: {total_video_duration:.2f}s")

concat_out = os.path.join(SCENES_DIR, "concatenated_silent.mp4")
cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", filter_complex,
    "-map", f"[{last_label}]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
    concat_out
]
run(cmd)
print(f"Saved silent concatenated cut: {concat_out}")

# =====================================================================
# AUDIO: real voice-over, with the licensed piano score ducked underneath
# it (sidechain compression, music dips while Shahram is talking, swells
# back up in the pauses) rather than just laid flat under the voice.
# =====================================================================
print("\nMixing voice-over with ducked piano score...")
voice_src = os.path.join(SRC, "voiceover_raw.mp4")
piano_src = os.path.join(SRC, "piano_reflections.mp3")
mixed_audio = os.path.join(SCENES_DIR, "audio_mixed.m4a")

probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice_src],
    capture_output=True, text=True
)
voice_duration = float(probe.stdout.strip())
print(f"Voice-over duration: {voice_duration:.2f}s | video duration: {total_video_duration:.2f}s")

if voice_duration > total_video_duration + 0.5:
    print(f"WARNING: voice-over ({voice_duration:.2f}s) is more than 0.5s longer than the "
          f"assembled video ({total_video_duration:.2f}s). Extending the end card would be needed; "
          f"stopping so scene timings can be re-checked instead of silently truncating the voice.")
    raise SystemExit(1)
target_dur = total_video_duration
fade_out_start = max(0, target_dur - 2.5)
# Voice is a quiet phone recording (mean ~-28.6dB), so it's boosted and
# gently compressed BEFORE mixing, the music bed is dropped to a low base
# level, and sidechain ducking on top of that pushes it down further while
# Shahram is talking. Explicit asplit avoids any ambiguity about reusing
# the voice stream as both the sidechain key and the thing being mixed in.
filter_complex_audio = (
    f"[0:a]atrim=0:{target_dur},afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.2f}:d=2.5,volume=0.20[music];"
    f"[1:a]atrim=0:{target_dur},apad=whole_dur={target_dur},"
    f"volume=2.6,acompressor=threshold=0.12:ratio=3:attack=10:release=200:makeup=1.15[voiceboost];"
    f"[voiceboost]asplit=2[voice_key][voice_mix];"
    f"[music][voice_key]sidechaincompress=threshold=0.015:ratio=15:attack=20:release=600:makeup=1[ducked];"
    f"[ducked][voice_mix]amix=inputs=2:duration=first:weights='0.6 3.0':normalize=0[premix];"
    f"[premix]alimiter=limit=0.85:attack=5:release=50:level=disabled[mixed]"
)
cmd = [
    "ffmpeg", "-y", "-i", piano_src, "-i", voice_src,
    "-filter_complex", filter_complex_audio,
    "-map", "[mixed]", "-t", str(target_dur),
    "-c:a", "aac", "-b:a", "192k",
    mixed_audio
]
run(cmd)
print(f"Saved mixed audio (voice-forward mix, ducked score): {mixed_audio}")

# =====================================================================
# FINAL MUX
# =====================================================================
final_out = os.path.join(OUT, "twenty_guys_and_a_bus_ride.mp4")
cmd = [
    "ffmpeg", "-y", "-i", concat_out, "-i", mixed_audio,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-c:a", "copy", "-shortest",
    final_out
]
run(cmd)
print(f"\nSaved final video: {final_out}")
print(f"File size: {os.path.getsize(final_out) / 1024:.1f} KB")
