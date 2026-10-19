#!/usr/bin/python3
"""Generate placeholder gradient wallpapers, one per scene, into images/.

Run once to seed the repo. Replace any images/<scene>.jpg with real art
(5120x3200 JPEG) and then run tools/build_manifest.py.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 5120, 3200

# scene key (ParticleType case name) -> (title, top colour, bottom colour)
SCENES = {
    "snow": ("Snow", "#9fb8d1", "#e8eef5"),
    "snow2": ("Snow 2", "#1c2a44", "#4b6a95"),
    "blusterySnow": ("Blustery Snow", "#5b6670", "#c9d1d8"),
    "rain": ("Drizzle", "#4e6b73", "#8fa3a8"),
    "heavyRain": ("Heavy Rain", "#1f2a36", "#3c4b5c"),
    "stormy": ("Stormy", "#2b2f3a", "#8a7a4a"),
    "fog": ("Drifting Fog", "#6e7a74", "#b8c1ba"),
    "leaves": ("Autumn Leaves", "#c9671f", "#f0c060"),
    "cherryBlossoms": ("Cherry Blossoms", "#f4b6c7", "#cfe3f5"),
    "fireflies": ("Fireflies", "#0b1230", "#1f2d55"),
    "dandelionSeeds": ("Dandelion Seeds", "#7bb04a", "#f2e36a"),
    "butterflies": ("Butterflies", "#a98bd0", "#e8d6f5"),
    "insects": ("Insects", "#d49a3a", "#4f7a3c"),
    "soapBubbles": ("Soap Bubbles", "#4fa3e8", "#bfe4ff"),
    "embers": ("Rising Embers", "#120a05", "#6a2e0a"),
    "birds": ("Birds", "#f6b28a", "#b4a8d8"),
    "christmasLights": ("Christmas Lights", "#0e1a2e", "#2a3f60"),
    "christmasLights2": ("Christmas Lights 2", "#121826", "#3a4a66"),
    "christmasTree": ("Christmas Tree", "#2a1a10", "#5a3a24"),
    "christmasEve": ("Christmas Eve", "#0e1a40", "#2d4a8a"),
    "stringLights": ("Patio Lights", "#4a3a2a", "#c9884a"),
    "chineseLanterns": ("Chinese Lanterns", "#1a0a0a", "#6a1515"),
    "skyLanterns": ("Sky Lanterns", "#0a1024", "#2a2a5a"),
    "starryNight": ("Starry Night", "#05070f", "#141a33"),
    "sunRays": ("Sun Rays", "#4a3412", "#d9a94a"),
    "aurora": ("Aurora Borealis", "#061423", "#0f3b3a"),
    "shootingStars": ("Shooting Stars", "#060a1a", "#1a2a4a"),
    "confetti": ("Confetti", "#3a1040", "#b03080"),
    "hearts": ("Hearts", "#f3c4d0", "#f9e2e8"),
    "batsAndGhosts": ("Bats & Ghosts", "#1a0c2a", "#e06a1a"),
    "fireworks": ("Fireworks", "#0a0f24", "#1f2d5a"),
    "balloons": ("Balloons", "#a8d8f5", "#e8f6ff"),
    "musicNotes": ("Music Notes", "#3a0f1a", "#7a2a3a"),
    "shamrocks": ("Shamrocks", "#2a6a2a", "#8fd08a"),
    "easterEggs": ("Easter Eggs", "#d8f0c8", "#f8e4f0"),
    "paperPlanes": ("Paper Planes", "#8fc8f5", "#e8f4ff"),
    "umbrellas": ("Umbrellas", "#5a6670", "#a8b0b8"),
    "beachBalls": ("Beach Balls", "#22a8c8", "#f8ecd0"),
    "lunarNewYear": ("Lunar New Year", "#7a0a0a", "#d8a020"),
    "champagne": ("Champagne", "#0a0806", "#6a4a1a"),
    "jellyfish": ("Jellyfish", "#16203f", "#3a2f6a"),
    "schoolingFish": ("Schooling Fish", "#1a8aa8", "#a8e0f0"),
    "plankton": ("Bioluminescent Plankton", "#03061a", "#0a1a3a"),
    "kelp": ("Kelp Forest", "#0a3a2a", "#3a8a5a"),
    "bubbleStream": ("Bubble Streams", "#38b8d8", "#c8f0f8"),
}

def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def gradient(top, bottom):
    # Build a 1xH column and stretch it; cheap and smooth.
    col = Image.new("RGB", (1, H))
    px = col.load()
    for y in range(H):
        t = y / (H - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return col.resize((W, H))

def vignette(img):
    mask = Image.new("L", (W // 8, H // 8), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W // 32, -H // 32, W // 8 + W // 32, H // 8 + H // 32], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(W // 64)).resize((W, H))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, 0.35), mask)

def label(img, title):
    try:
        font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 72)
    except Exception:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(img, "RGBA")
    text = f"Placeholder · {title}"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((W - tw - 120, H - th - 120), text, font=font, fill=(255, 255, 255, 90))

def main():
    only = set(sys.argv[1:])
    for key, (title, top, bottom) in SCENES.items():
        if only and key not in only:
            continue
        out = os.path.join(ROOT, "images", f"{key}.jpg")
        img = vignette(gradient(hex_rgb(top), hex_rgb(bottom)))
        label(img, title)
        img.save(out, "JPEG", quality=82, optimize=True, progressive=True, comment=b"serene-placeholder")
        print(f"{key}: {os.path.getsize(out) // 1024} KB")

if __name__ == "__main__":
    main()
