"""
Taxila, Preserved in 3D: short story video (v2, with real audio and motion)
PMW Internship 2026, Special: Story, Script, Film & Edit

No camera, no live-action footage, this is an AI-based 3D reconstruction
project. This script builds an actual playable MP4 from genuine project
artifacts: a real photo, real generated visualizations, and a real
rotating render of the actual .ply point cloud, following script.md.

v2 adds real production value on top of the v1 static-card version:
- Ken Burns slow zoom on every photo/render card instead of a frozen still
- Crossfade dissolves between every scene instead of hard cuts
- Fade in/out text instead of text just appearing
- A real synthesized audio track (ambient pad, whoosh transitions, a
  reveal chime at the 3D climax, a low tension tone, a descending
  "failure" stinger), all procedurally generated with numpy, not
  licensed music, no voiceover per team decision (would look uneven if
  only one of three teammates narrated).
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import subprocess
import wave

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(SCRIPT_DIR, 'frames')
OUT_DIR = os.path.join(SCRIPT_DIR, 'output')
FPS = 24
SR = 44100
W, H = 1280, 720

BG = (6, 11, 20)
GOLD = (212, 168, 67)
SAND = (245, 236, 215)

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
for f in os.listdir(FRAMES_DIR):
    os.remove(os.path.join(FRAMES_DIR, f))

# =================================================================
# TEXT / FONT HELPERS
# =================================================================

def get_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def fade_alpha_curve(num_frames, fade_frames):
    """1.0 in the middle, ramping 0->1 at the start and 1->0 at the end."""
    fade_frames = min(fade_frames, num_frames // 2)
    curve = np.ones(num_frames)
    if fade_frames > 0:
        ramp = np.linspace(0, 1, fade_frames)
        curve[:fade_frames] = ramp
        curve[-fade_frames:] = ramp[::-1]
    return curve


# =================================================================
# SCENE BUILDERS: each returns a LIST of PIL frames
# =================================================================

def build_title_frames(num_frames):
    base = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(base)
    title_font = get_font(64, bold=True)
    sub_font = get_font(26)

    title = "TAXILA, PRESERVED IN 3D"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tx = (W - (bbox[2] - bbox[0])) // 2
    sub = "Team Taxila | PreserveMy.World x TechRealm 2026"
    bbox2 = draw.textbbox((0, 0), sub, font=sub_font)
    sx = (W - (bbox2[2] - bbox2[0])) // 2

    curve = fade_alpha_curve(num_frames, fade_frames=18)
    frames = []
    for i in range(num_frames):
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        # slight scale-in on the title for the first ~20 frames
        scale = min(1.0, 0.94 + 0.06 * (i / 18)) if i < 18 else 1.0
        alpha = curve[i]
        gold_a = tuple(int(BG[c] + (GOLD[c] - BG[c]) * alpha) for c in range(3))
        sand_a = tuple(int(BG[c] + (SAND[c] - BG[c]) * alpha) for c in range(3))
        d.text((tx, H // 2 - 60 + int((1 - scale) * 20)), title, font=title_font, fill=gold_a)
        d.text((sx, H // 2 + 30), sub, font=sub_font, fill=sand_a)
        border_a = tuple(int(v * 0.3 * alpha) for v in GOLD)
        d.rectangle([(0, 0), (W - 1, H - 1)], outline=border_a, width=2)
        frames.append(img)
    return frames


def build_text_frames(lines, num_frames, sub_lines=None):
    body_font = get_font(34)
    sub_font = get_font(24)

    wrapped = []
    tmp = Image.new('RGB', (1, 1))
    d0 = ImageDraw.Draw(tmp)
    for line in lines:
        wrapped.extend(wrap_text(d0, line, body_font, W - 240))

    total_h = len(wrapped) * 52 + (len(sub_lines) * 34 + 20 if sub_lines else 0)
    start_y = (H - total_h) // 2

    curve = fade_alpha_curve(num_frames, fade_frames=15)
    frames = []
    for i in range(num_frames):
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        alpha = curve[i]
        sand_a = tuple(int(BG[c] + (SAND[c] - BG[c]) * alpha) for c in range(3))
        gold_a = tuple(int(BG[c] + (GOLD[c] - BG[c]) * alpha) for c in range(3))
        y = start_y
        for line in wrapped:
            bbox = d.textbbox((0, 0), line, font=body_font)
            x = (W - (bbox[2] - bbox[0])) // 2
            d.text((x, y), line, font=body_font, fill=sand_a)
            y += 52
        if sub_lines:
            y += 20
            for line in sub_lines:
                bbox = d.textbbox((0, 0), line, font=sub_font)
                x = (W - (bbox[2] - bbox[0])) // 2
                d.text((x, y), line, font=sub_font, fill=gold_a)
                y += 34
        frames.append(img)
    return frames


def build_kenburns_photo_frames(photo_path, caption_lines, num_frames, zoom_end=1.14):
    photo = Image.open(photo_path).convert('RGB')
    photo_ratio = photo.width / photo.height
    target_h = int(H * 0.62)
    target_w = int(target_h * photo_ratio)
    if target_w > W - 100:
        target_w = W - 100
        target_h = int(target_w / photo_ratio)
    base_photo = photo.resize((target_w, target_h), Image.LANCZOS)

    body_font = get_font(30)
    tmp = Image.new('RGB', (1, 1))
    d0 = ImageDraw.Draw(tmp)
    wrapped = []
    for line in caption_lines:
        wrapped.extend(wrap_text(d0, line, body_font, W - 200))

    fade = fade_alpha_curve(num_frames, fade_frames=12)
    frames = []
    for i in range(num_frames):
        t = i / max(1, num_frames - 1)
        zoom = 1.0 + (zoom_end - 1.0) * t
        crop_w = int(target_w / zoom)
        crop_h = int(target_h / zoom)
        cx, cy = target_w // 2, target_h // 2
        box = (cx - crop_w // 2, cy - crop_h // 2, cx + crop_w // 2, cy + crop_h // 2)
        cropped = base_photo.crop(box).resize((target_w, target_h), Image.LANCZOS)

        img = Image.new('RGB', (W, H), BG)
        img.paste(cropped, ((W - target_w) // 2, 50))
        d = ImageDraw.Draw(img)
        alpha = fade[i]
        sand_a = tuple(int(BG[c] + (SAND[c] - BG[c]) * alpha) for c in range(3))
        y = 50 + target_h + 30
        for line in wrapped:
            bbox = d.textbbox((0, 0), line, font=body_font)
            x = (W - (bbox[2] - bbox[0])) // 2
            d.text((x, y), line, font=body_font, fill=sand_a)
            y += 42
        frames.append(img)
    return frames


def build_kenburns_render_frames(render_path, caption_lines, num_frames, zoom_end=1.10):
    render = Image.open(render_path).convert('RGB')
    render_ratio = render.width / render.height
    target_w = W - 120
    target_h = int(target_w / render_ratio)
    if target_h > H - 180:
        target_h = H - 180
        target_w = int(target_h * render_ratio)
    base_render = render.resize((target_w, target_h), Image.LANCZOS)

    body_font = get_font(28)
    tmp = Image.new('RGB', (1, 1))
    d0 = ImageDraw.Draw(tmp)
    wrapped = []
    for line in caption_lines:
        wrapped.extend(wrap_text(d0, line, body_font, W - 200))

    fade = fade_alpha_curve(num_frames, fade_frames=12)
    frames = []
    for i in range(num_frames):
        t = i / max(1, num_frames - 1)
        zoom = 1.0 + (zoom_end - 1.0) * t
        crop_w = int(target_w / zoom)
        crop_h = int(target_h / zoom)
        cx, cy = target_w // 2, target_h // 2
        box = (cx - crop_w // 2, cy - crop_h // 2, cx + crop_w // 2, cy + crop_h // 2)
        cropped = base_render.crop(box).resize((target_w, target_h), Image.LANCZOS)

        img = Image.new('RGB', (W, H), BG)
        img.paste(cropped, ((W - target_w) // 2, 30))
        d = ImageDraw.Draw(img)
        alpha = fade[i]
        sand_a = tuple(int(BG[c] + (SAND[c] - BG[c]) * alpha) for c in range(3))
        y = 30 + target_h + 25
        for line in wrapped:
            bbox = d.textbbox((0, 0), line, font=body_font)
            x = (W - (bbox[2] - bbox[0])) // 2
            d.text((x, y), line, font=body_font, fill=sand_a)
            y += 38
        frames.append(img)
    return frames


def load_ply(path):
    with open(path) as f:
        lines = f.readlines()
    header_end = next(i for i, l in enumerate(lines) if l.strip() == 'end_header')
    data = np.array([list(map(float, l.split())) for l in lines[header_end + 1:]])
    return data[:, :3], data[:, 3:6] / 255.0


def build_rotation_frames(ply_path, num_frames):
    xyz, rgb = load_ply(ply_path)
    print(f"Loaded point cloud for rotation: {len(xyz)} points")
    frames = []
    fade = fade_alpha_curve(num_frames, fade_frames=10)
    for i in range(num_frames):
        azim = -90 + (360.0 * i / num_frames)
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        fig.patch.set_facecolor(np.array(BG) / 255)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(np.array(BG) / 255)
        ax.scatter(xyz[:, 0], xyz[:, 2], xyz[:, 1], c=rgb, s=4)
        ax.view_init(elev=12, azim=azim)
        ax.set_axis_off()
        ax.set_box_aspect([1, 1, 0.6])
        text_alpha = fade[i]
        sand_a = tuple((BG[c] + (SAND[c] - BG[c]) * text_alpha) / 255 for c in range(3))
        fig.text(0.5, 0.06, "13,375 real 3D points, rotating live", ha='center', color=sand_a, fontsize=13)

        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        img = Image.fromarray(buf).convert('RGB').resize((W, H))
        plt.close('all')
        frames.append(img)
    print(f"Rendered {num_frames} rotation frames")
    return frames


def crossfade(tail_frame, head_frame, count):
    out = []
    for i in range(count):
        t = (i + 1) / (count + 1)
        blended = Image.blend(tail_frame, head_frame, t)
        out.append(blended)
    return out


# =================================================================
# AUDIO SYNTHESIS (procedural, numpy only, no external samples)
# =================================================================

def envelope(n, attack, release):
    env = np.ones(n)
    a = min(attack, n // 2)
    r = min(release, n // 2)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return env


def synth_pad(duration, freqs, sr=SR, vol=0.10):
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)
    out = np.zeros(n)
    for f in freqs:
        lfo = 1.0 + 0.03 * np.sin(2 * np.pi * 0.07 * t)
        out += np.sin(2 * np.pi * f * t * lfo)
    out /= len(freqs)
    out *= envelope(n, attack=int(1.2 * sr), release=int(1.5 * sr))
    return out * vol


def synth_whoosh(duration=0.5, sr=SR, vol=0.12):
    n = int(duration * sr)
    noise = np.random.uniform(-1, 1, n)
    t = np.linspace(0, 1, n)
    freq_sweep = 200 + 1800 * t
    phase = np.cumsum(freq_sweep) / sr
    tone = np.sin(2 * np.pi * phase)
    mixed = 0.5 * noise + 0.5 * tone
    mixed *= envelope(n, attack=int(0.05 * n), release=int(0.6 * n))
    return mixed * vol


def synth_chime(duration=1.6, sr=SR, vol=0.16):
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)
    base = 440.0
    out = np.zeros(n)
    for mult, amp in [(1, 1.0), (2, 0.5), (3, 0.3), (4.2, 0.15)]:
        out += amp * np.sin(2 * np.pi * base * mult * t)
    decay = np.exp(-t * 2.2)
    out *= decay
    out *= envelope(n, attack=int(0.01 * sr), release=0)
    return out * vol


def synth_tension(duration, sr=SR, vol=0.06):
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)
    vibrato = 1.0 + 0.015 * np.sin(2 * np.pi * 5 * t)
    tone = np.sin(2 * np.pi * 55 * t * vibrato) + 0.5 * np.sin(2 * np.pi * 110 * t * vibrato)
    tone *= envelope(n, attack=int(0.3 * sr), release=int(0.3 * sr))
    return tone * vol


def synth_stinger_down(duration=0.9, sr=SR, vol=0.14):
    n = int(duration * sr)
    t = np.linspace(0, 1, n)
    freq_sweep = 500 - 380 * t
    phase = np.cumsum(freq_sweep) / sr
    tone = np.sin(2 * np.pi * phase)
    tone *= envelope(n, attack=int(0.02 * n), release=int(0.7 * n))
    return tone * vol


def mix_in(master, clip, start_sample):
    end = start_sample + len(clip)
    if end > len(master):
        clip = clip[:len(master) - start_sample]
        end = len(master)
    master[start_sample:end] += clip


def write_wav(path, samples, sr=SR):
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(pcm.tobytes())


# =================================================================
# BUILD THE FULL FRAME TIMELINE, SCENE BY SCENE
# =================================================================

XFADE = 8  # frames blended between each pair of scenes

scenes = []  # list of (name, frame_list)

scenes.append(("title", build_title_frames(FPS * 4)))
scenes.append(("hook", build_kenburns_photo_frames(
    "../ml-viz-ar-capture3d/source/jaulian-monastery-taxila.jpg",
    ["2,600 years ago, this was a center of learning.", "Older than Oxford. Older than Nalanda."],
    FPS * 5
)))
scenes.append(("threat", build_kenburns_photo_frames(
    "../ml-viz-ar-capture3d/source/jaulian-monastery-taxila.jpg",
    ["Today, it's a UNESCO World Heritage Site", "under active threat."],
    FPS * 5, zoom_end=1.20
)))
scenes.append(("unesco", build_text_frames(
    ["In 2026, UNESCO warned Pakistan that cement",
     "\"restoration\" at two Taxila sites risked the whole listing."],
    FPS * 5
)))
scenes.append(("question", build_text_frames(
    ["So we asked: can we preserve it a different way?"], FPS * 4
)))
scenes.append(("mlviz", build_kenburns_render_frames(
    "../ml-viz-ar-capture3d/output/01_ml_visualization.png",
    ["Step one: teach a computer to see structure.", "24,091 feature points, detected automatically."],
    FPS * 6
)))
scenes.append(("aroverlay", build_kenburns_render_frames(
    "../ml-viz-ar-capture3d/output/02_ar_line_overlay.png",
    ["Step two: trace what an AR app would show", "a visitor live, on their phone."],
    FPS * 6
)))
scenes.append(("sfmfail", build_text_frames(
    ["We tested real multi-view reconstruction first.",
     "It failed honestly: only 12-17 matching points per photo pair. Not enough."],
    FPS * 5
)))
scenes.append(("capture3d", build_kenburns_render_frames(
    "../ml-viz-ar-capture3d/output/03_capture_to_3d.png",
    ["So we built the honest alternative:", "a single-photo depth reconstruction."],
    FPS * 5
)))
scenes.append(("rotation", build_rotation_frames(
    "../week3-3d-reconstruction/output/jaulian_monastery_taxila.ply", FPS * 12
)))
scenes.append(("limitation", build_text_frames(
    ["Not perfect. Not multi-view SfM.", "But real, verified, and yours to explore."], FPS * 5
)))
scenes.append(("credits", build_text_frames(
    ["Built by Team Taxila:"], FPS * 5,
    sub_lines=["Rabeea Iman  |  Ruwaida Shakeel  |  Shahram Shafiq (lead)"]
)))
scenes.append(("end", build_text_frames(
    ["PreserveMy.World x TechRealm 2026"], FPS * 4,
    sub_lines=["Full interactive version:", "shahramshafiq.github.io/PMW-heritage-showcase"]
)))

# stitch scenes together with crossfade transitions, tracking each
# scene's ACTUAL start frame for audio sync (crossfades shift timing)
full_frames = []
scene_start_frame = {}
for idx, (name, frames) in enumerate(scenes):
    if idx > 0:
        prev_tail = full_frames[-1]
        blend = crossfade(prev_tail, frames[0], XFADE)
        full_frames.extend(blend)
    scene_start_frame[name] = len(full_frames)
    full_frames.extend(frames)

total_frames = len(full_frames)
duration_sec = total_frames / FPS
print(f"\nTotal video frames (with crossfades): {total_frames}")
print(f"Duration: {duration_sec:.2f} seconds at {FPS} fps")

print("\nSaving frames to disk...")
for i, img in enumerate(full_frames):
    img.save(os.path.join(FRAMES_DIR, f"frame_{i:05d}.png"))
on_disk = len(os.listdir(FRAMES_DIR))
assert on_disk == total_frames, f"Frame count mismatch: {on_disk} on disk vs {total_frames} expected"
print(f"Verified: {on_disk} frames on disk match expected count exactly")

# =================================================================
# BUILD THE AUDIO TRACK, SYNCED TO ACTUAL SCENE START TIMES
# =================================================================

print("\nBuilding audio track...")
master = np.zeros(int(duration_sec * SR) + SR)  # a little headroom at the end

# ambient pad under the whole video, a slow minor-key drone
pad = synth_pad(duration_sec, freqs=[110.0, 130.81, 164.81], vol=0.09)  # A minor-ish triad, low
mix_in(master, pad, 0)

# soft chime under the title
mix_in(master, synth_chime(1.2, vol=0.10), int(0.3 * SR))

# whoosh at every scene transition
for name, start in scene_start_frame.items():
    if name == "title":
        continue
    t_sec = start / FPS
    mix_in(master, synth_whoosh(0.4, vol=0.09), int(t_sec * SR))

# low tension rumble under the UNESCO warning scene
unesco_start = scene_start_frame["unesco"] / FPS
mix_in(master, synth_tension(5.0, vol=0.05), int(unesco_start * SR))

# descending stinger at the honest SfM failure beat
sfmfail_start = scene_start_frame["sfmfail"] / FPS
mix_in(master, synth_stinger_down(0.9, vol=0.13), int(sfmfail_start * SR))

# the big reveal chime right as the rotation climax begins
rotation_start = scene_start_frame["rotation"] / FPS
mix_in(master, synth_chime(2.0, vol=0.15), int(rotation_start * SR))
mix_in(master, synth_pad(FPS * 12 / FPS, freqs=[164.81, 196.0, 220.0], vol=0.07), int(rotation_start * SR))

wav_path = os.path.join(OUT_DIR, "audio_track.wav")
write_wav(wav_path, master[:int(duration_sec * SR)])
print(f"Saved audio: {wav_path}")

# =================================================================
# ENCODE FINAL VIDEO: frames + audio, muxed together
# =================================================================

output_path = os.path.join(OUT_DIR, "taxila_preserved_in_3d.mp4")
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-i", wav_path,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "160k",
    "-shortest",
    output_path
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("FFMPEG FAILED:")
    print(result.stderr[-3000:])
else:
    print(f"\nSaved final video with audio: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
