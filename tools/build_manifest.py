#!/usr/bin/python3
"""Rebuild thumbs/ and manifest.json from whatever is in images/.

Usage: tools/build_manifest.py
Drop a 5120x3200 JPEG named images/<scene>.jpg (scene = ParticleType case
name, e.g. cherryBlossoms) and run this. Thumbnails are 480x300 JPEGs.
"""
import os, json, datetime
from PIL import Image
from make_placeholders import SCENES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://dsreinhart.github.io/serene-screens-wallpapers/"
THUMB = (480, 300)

def is_placeholder(path):
    # Placeholders carry a JPEG comment written by make_placeholders; real art
    # is simply anything without it. Cheap heuristic: file under 1.5 MB with
    # the placeholder marker in the first bytes is treated as placeholder.
    with Image.open(path) as im:
        return im.info.get("comment", b"") == b"serene-placeholder"

def main():
    os.makedirs(os.path.join(ROOT, "thumbs"), exist_ok=True)
    entries = []
    for key, (title, _, _) in SCENES.items():
        src = os.path.join(ROOT, "images", f"{key}.jpg")
        if not os.path.exists(src):
            continue
        dst = os.path.join(ROOT, "thumbs", f"{key}.jpg")
        with Image.open(src) as im:
            width, height = im.size
            im = im.convert("RGB")
            im.thumbnail((THUMB[0] * 2, THUMB[1] * 2))  # cheap pre-shrink
            im = im.resize(THUMB, Image.LANCZOS)
            im.save(dst, "JPEG", quality=85, optimize=True)
        entries.append({
            "scene": key,
            "title": title,
            "image": f"images/{key}.jpg",
            "thumbnail": f"thumbs/{key}.jpg",
            "width": width,
            "height": height,
            "bytes": os.path.getsize(src),
            "placeholder": is_placeholder(src),
        })
    manifest = {
        "version": 1,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "baseURL": BASE_URL,
        "wallpapers": entries,
    }
    with open(os.path.join(ROOT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"{len(entries)} wallpapers, {sum(e['bytes'] for e in entries) / 1e6:.1f} MB total")

if __name__ == "__main__":
    main()
