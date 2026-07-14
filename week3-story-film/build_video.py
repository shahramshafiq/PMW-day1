"""
Taxila, Preserved in 3D: short story video
PMW Internship 2026, Special: Story, Script, Film & Edit

This is not live-action footage, there is no camera and no physical
filming for this AI-based 3D reconstruction project. Instead, this
script builds an actual video file (not a mockup, a real playable MP4)
from genuine project artifacts: a real photo, real generated
visualizations, and a real rotating render of the actual .ply point
cloud, following the script beats in script.md.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(SCRIPT_DIR, 'frames')
OUT_DIR = os.path.join(SCRIPT_DIR, 'output')
FPS = 24
W, H = 1280, 720

BG = (6, 11, 20)
GOLD = (212, 168, 67)
SAND = (245, 236, 215)
MUTED = (150, 145, 130)


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
    lines = []
    current = ""
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


def make_text_card(lines, sub_lines=None, filename="card.png"):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    title_font = get_font(54, bold=True)
    body_font = get_font(34)
    sub_font = get_font(24)

    all_wrapped = []
    for line in lines:
        all_wrapped.extend(wrap_text(draw, line, body_font, W - 240))

    total_h = len(all_wrapped) * 52
    y = (H - total_h) // 2
    for line in all_wrapped:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        x = (W - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, font=body_font, fill=SAND)
        y += 52

    if sub_lines:
        y += 20
        for line in sub_lines:
            bbox = draw.textbbox((0, 0), line, font=sub_font)
            x = (W - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, font=sub_font, fill=GOLD)
            y += 34

    img.save(os.path.join(FRAMES_DIR, filename))


def make_title_card(filename="00_title.png"):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_font = get_font(64, bold=True)
    sub_font = get_font(26)

    title = "TAXILA, PRESERVED IN 3D"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    x = (W - (bbox[2] - bbox[0])) // 2
    draw.text((x, H // 2 - 60), title, font=title_font, fill=GOLD)

    sub = "Team Taxila | PreserveMy.World x TechRealm 2026"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    x = (W - (bbox[2] - bbox[0])) // 2
    draw.text((x, H // 2 + 30), sub, font=sub_font, fill=SAND)

    draw.rectangle([(0, 0), (W - 1, H - 1)], outline=(int(GOLD[0]*0.3), int(GOLD[1]*0.3), int(GOLD[2]*0.3)), width=2)
    img.save(os.path.join(FRAMES_DIR, filename))


def make_photo_card(photo_path, caption_lines, filename):
    photo = Image.open(photo_path).convert('RGB')
    photo_ratio = photo.width / photo.height
    target_h = int(H * 0.62)
    target_w = int(target_h * photo_ratio)
    if target_w > W - 100:
        target_w = W - 100
        target_h = int(target_w / photo_ratio)
    photo = photo.resize((target_w, target_h))

    img = Image.new('RGB', (W, H), BG)
    img.paste(photo, ((W - target_w) // 2, 50))

    draw = ImageDraw.Draw(img)
    body_font = get_font(30)
    wrapped = []
    for line in caption_lines:
        wrapped.extend(wrap_text(draw, line, body_font, W - 200))

    y = 50 + target_h + 30
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        x = (W - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, font=body_font, fill=SAND)
        y += 42

    img.save(os.path.join(FRAMES_DIR, filename))


def make_render_card(render_path, caption_lines, filename):
    render = Image.open(render_path).convert('RGB')
    render_ratio = render.width / render.height
    target_w = W - 120
    target_h = int(target_w / render_ratio)
    if target_h > H - 180:
        target_h = H - 180
        target_w = int(target_h * render_ratio)
    render = render.resize((target_w, target_h))

    img = Image.new('RGB', (W, H), BG)
    img.paste(render, ((W - target_w) // 2, 30))

    draw = ImageDraw.Draw(img)
    body_font = get_font(28)
    wrapped = []
    for line in caption_lines:
        wrapped.extend(wrap_text(draw, line, body_font, W - 200))

    y = 30 + target_h + 25
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        x = (W - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, font=body_font, fill=SAND)
        y += 38

    img.save(os.path.join(FRAMES_DIR, filename))


def load_ply(path):
    with open(path) as f:
        lines = f.readlines()
    header_end = next(i for i, l in enumerate(lines) if l.strip() == 'end_header')
    data = np.array([list(map(float, l.split())) for l in lines[header_end + 1:]])
    xyz = data[:, :3]
    rgb = data[:, 3:6] / 255.0
    return xyz, rgb


def make_rotation_frames(ply_path, num_frames, start_idx):
    xyz, rgb = load_ply(ply_path)
    print(f"Loaded point cloud for rotation: {len(xyz)} points")

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

        fig.text(0.5, 0.06, "13,375 real 3D points, rotating live",
                  ha='center', color=np.array(SAND) / 255, fontsize=13)

        frame_path = os.path.join(FRAMES_DIR, f"{start_idx + i:05d}_rotate.png")
        plt.savefig(frame_path, facecolor=fig.get_facecolor())
        plt.close('all')

    print(f"Saved {num_frames} rotation frames")


def repeat_frame(src_filename, count, start_idx):
    src_path = os.path.join(FRAMES_DIR, src_filename)
    src = Image.open(src_path)
    for i in range(count):
        src.save(os.path.join(FRAMES_DIR, f"{start_idx + i:05d}_hold.png"))
    src.close()
    os.remove(src_path)  # otherwise this leftover source card becomes one extra stray frame


# --- Build the frame sequence in script order ---
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
for f in os.listdir(FRAMES_DIR):
    os.remove(os.path.join(FRAMES_DIR, f))

idx = 0

# Scene 1: title (4s)
make_title_card("001_scene.png")
repeat_frame("001_scene.png", FPS * 4, idx)
idx += FPS * 4

# Scene 2: real photo, hook (5s)
make_photo_card(
    "../ml-viz-ar-capture3d/source/jaulian-monastery-taxila.jpg",
    ["2,600 years ago, this was a center of learning.", "Older than Oxford. Older than Nalanda."],
    "002_scene.png"
)
repeat_frame("002_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 3: same photo, threat framing (5s)
make_photo_card(
    "../ml-viz-ar-capture3d/source/jaulian-monastery-taxila.jpg",
    ["Today, it's a UNESCO World Heritage Site", "under active threat."],
    "003_scene.png"
)
repeat_frame("003_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 4: text card, the real news (5s)
make_text_card(
    ["In 2026, UNESCO warned Pakistan that cement",
     "\"restoration\" at two Taxila sites risked the whole listing."],
    filename="004_scene.png"
)
repeat_frame("004_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 5: the question (4s)
make_text_card(["So we asked: can we preserve it a different way?"], filename="005_scene.png")
repeat_frame("005_scene.png", FPS * 4, idx)
idx += FPS * 4

# Scene 6: ML feature detection (6s)
make_render_card(
    "../ml-viz-ar-capture3d/output/01_ml_visualization.png",
    ["Step one: teach a computer to see structure.", "24,091 feature points, detected automatically."],
    "006_scene.png"
)
repeat_frame("006_scene.png", FPS * 6, idx)
idx += FPS * 6

# Scene 7: AR line overlay (6s)
make_render_card(
    "../ml-viz-ar-capture3d/output/02_ar_line_overlay.png",
    ["Step two: trace what an AR app would show", "a visitor live, on their phone."],
    "007_scene.png"
)
repeat_frame("007_scene.png", FPS * 6, idx)
idx += FPS * 6

# Scene 8: honest failure of multi-view SfM (5s)
make_text_card(
    ["We tested real multi-view reconstruction first.",
     "It failed honestly: only 12-17 matching points per photo pair. Not enough."],
    filename="008_scene.png"
)
repeat_frame("008_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 9: capture to 3D static (5s)
make_render_card(
    "../ml-viz-ar-capture3d/output/03_capture_to_3d.png",
    ["So we built the honest alternative:", "a single-photo depth reconstruction."],
    "009_scene.png"
)
repeat_frame("009_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 10: LIVE rotating point cloud (12s) - the real climax
rotation_frame_count = FPS * 12
make_rotation_frames(
    "../week3-3d-reconstruction/output/jaulian_monastery_taxila.ply",
    rotation_frame_count,
    idx
)
idx += rotation_frame_count

# Scene 11: honest limitation (5s)
make_text_card(
    ["Not perfect. Not multi-view SfM.", "But real, verified, and yours to explore."],
    filename="011_scene.png"
)
repeat_frame("011_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 12: team credits (5s)
make_text_card(
    ["Built by Team Taxila:"],
    sub_lines=["Rabeea Iman  |  Ruwaida Shakeel  |  Shahram Shafiq (lead)"],
    filename="012_scene.png"
)
repeat_frame("012_scene.png", FPS * 5, idx)
idx += FPS * 5

# Scene 13: end card (4s)
make_text_card(
    ["PreserveMy.World x TechRealm 2026"],
    sub_lines=["Full interactive version:", "shahramshafiq.github.io/PMW-heritage-showcase"],
    filename="013_scene.png"
)
repeat_frame("013_scene.png", FPS * 4, idx)
idx += FPS * 4

total_frames = idx
duration_sec = total_frames / FPS
print(f"\nTotal frames written: {total_frames}")
print(f"Expected duration: {duration_sec:.1f} seconds at {FPS} fps")

# --- Encode into an actual MP4 using ffmpeg ---
output_path = os.path.join(OUT_DIR, "taxila_preserved_in_3d.mp4")

# frames were written with mixed naming (NNN_hold.png / NNN_rotate.png)
# rename everything into one strict zero-padded sequence ffmpeg can read in order
all_frames = sorted(os.listdir(FRAMES_DIR))
assert len(all_frames) == total_frames, (
    f"Frame count mismatch: {len(all_frames)} files on disk vs {total_frames} expected from scene "
    f"durations. This caught a real bug once already (leftover source card files), don't silence it."
)
for i, fname in enumerate(all_frames):
    os.rename(os.path.join(FRAMES_DIR, fname), os.path.join(FRAMES_DIR, f"frame_{i:05d}.png"))

cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    output_path
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("FFMPEG FAILED:")
    print(result.stderr[-2000:])
else:
    print(f"\nSaved video: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
