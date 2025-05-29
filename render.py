import json
import os
from PIL import Image, ImageDraw
import subprocess

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30

GRID_COLS = 5
GRID_ROWS = 3

def grid_to_px(col, row, w_ratio, h_ratio):
    grid_w = SCREEN_WIDTH / GRID_COLS
    grid_h = SCREEN_HEIGHT / GRID_ROWS
    x = col * grid_w
    y = row * grid_h
    width = w_ratio * grid_w
    height = h_ratio * grid_h
    return int(x), int(y), int(width), int(height)

def load_sprite(path, target_size):
    sprite = Image.open(path).convert("RGBA")
    sprite = sprite.resize(target_size, Image.ANTIALIAS)
    return sprite

def create_frame(background, sprite=None, sprite_pos=None):
    frame = background.copy()
    if sprite and sprite_pos:
        frame.paste(sprite, sprite_pos, sprite)
    return frame

def render_video_from_json(json_path, output_path="output.mp4"):
    with open(json_path) as f:
        actions = json.load(f)

    frames = []
    current_bg = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), "black")
    current_sprite = None
    current_sprite_pos = None

    for action in actions:
        if action["type"] == "modify_background":
            bg_path = os.path.join("assets", action["background"])
            current_bg = Image.open(bg_path).convert("RGBA").resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif action["type"] == "play_music":
            music_path = os.path.join("assets", action["music"])
        elif action["type"] == "show_sprite":
            sprite_path = os.path.join("assets", action["location"])
            col = action.get("column", 0)
            row = action.get("row", 0)
            w_ratio = action.get("wFrameRatio", 1)
            h_ratio = action.get("hFrameRatio", 1)
            sprite_size = grid_to_px(0, 0, w_ratio, h_ratio)[2:]
            current_sprite = load_sprite(sprite_path, sprite_size)
            sprite_pos = grid_to_px(col, row, w_ratio, h_ratio)[:2]
            current_sprite_pos = sprite_pos
        elif action["type"] == "duration":
            duration = action["duration"]
            frame_count = int(duration * FPS)
            for _ in range(frame_count):
                frame = create_frame(current_bg, current_sprite, current_sprite_pos)
                frames.append(frame)
        elif action["type"] == "finish_video":
            break

    # Write video frames to a folder
    os.makedirs("frames", exist_ok=True)
    for i, frame in enumerate(frames):
        frame.save(f"frames/frame_{i:05d}.png")

    # Use ffmpeg to compile video
    subprocess.run([
        "ffmpeg",
        "-y",
        "-r", str(FPS),
        "-f", "image2",
        "-i", "frames/frame_%05d.png",
        "-i", music_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ])

    print(f"Video rendered to {output_path}")

if __name__ == "__main__":
    render_video_from_json("compiled.json")
