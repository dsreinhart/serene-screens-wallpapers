#!/usr/bin/python3
"""Generate wallpapers with fal.ai (FLUX 1.1 Pro Ultra) and stamp the logo.

Usage:
  tools/generate.py snow                 one scene
  tools/generate.py snow fog rain        several scenes
  tools/generate.py --all                every scene in prompts.json
  tools/generate.py --watermark-only X   re-stamp images/X.jpg from raw/X.jpg

The fal key is read from the login keychain (account fal.ai-api-key, the
item Wallz created) and is never printed. Each image costs $0.06.

Raw, unstamped results are kept in raw/<scene>.jpg (git-ignored) so the
logo can be re-applied without regenerating. Run tools/build_manifest.py
afterwards to refresh thumbs/ and manifest.json.
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.dirname(os.path.abspath(__file__))
MODEL = "fal-ai/flux-pro/v1.1-ultra"
QUEUE = "https://queue.fal.run"

# Same geometry as Wallz/ImageStore.swift: logo in the lower-right corner of
# the region a 16:10 Mac display shows after fill scaling.
LOGO_WIDTH_FRACTION = 0.035
LOGO_MARGIN_FRACTION = 0.018        # inset from the bottom edge
LOGO_RIGHT_INSET_FRACTION = 0.08    # inset from the right edge, clear of a Dock in the corner
TARGET_SCREEN_ASPECT = 16 / 10


def keychain_key():
    out = subprocess.run(
        ["security", "find-generic-password", "-a", "fal.ai-api-key", "-w"],
        capture_output=True, text=True, check=True,
    )
    key = out.stdout.strip()
    if not key:
        sys.exit("fal key not found in keychain")
    return key


def request(url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Key {key}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def generate(scene, prompt, key):
    submit = request(f"{QUEUE}/{MODEL}", key, {
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "enable_safety_checker": True,
        "output_format": "jpeg",
    })
    status_url, response_url = submit["status_url"], submit["response_url"]
    delay, deadline = 1.5, time.time() + 300
    while time.time() < deadline:
        time.sleep(delay)
        delay = min(delay * 1.3, 5)
        status = request(status_url, key)
        state = status.get("status", "").upper()
        if state == "COMPLETED":
            break
        if state in ("FAILED", "ERROR"):
            raise RuntimeError(f"{scene}: fal reported {state}: {status}")
    else:
        raise RuntimeError(f"{scene}: timed out waiting for fal")
    result = request(response_url, key)
    image = result["images"][0]
    # The CDN download carries no key.
    with urllib.request.urlopen(image["url"], timeout=120) as r:
        return r.read(), image.get("width"), image.get("height")


def letterboxed(data, max_pixel=10, min_rows=8):
    """True when the image carries black bars at the top or bottom, which
    FLUX occasionally renders for wide aspect ratios. A bar row is one whose
    brightest pixel is near zero; genuinely dark scenes (night skies, deep
    water) still have highlights well above that."""
    import io
    im = Image.open(io.BytesIO(data)).convert("L")
    w, h = im.size
    def bars(rows):
        return sum(1 for y in rows if im.crop((0, y, w, y + 1)).getextrema()[1] < max_pixel)
    return bars(range(0, 120)) >= min_rows or bars(range(h - 120, h)) >= min_rows


def generate_clean(scene, prompt, key, attempts=3):
    """Generate, retrying when the result is letterboxed."""
    for attempt in range(1, attempts + 1):
        data, w, h = generate(scene, prompt, key)
        if not letterboxed(data):
            return data, w, h
        rejected = os.path.join(ROOT, "raw", f"{scene}-rejected{attempt}.jpg")
        with open(rejected, "wb") as f:
            f.write(data)
        print(f"{scene}: letterboxed result on attempt {attempt} (kept as raw/{os.path.basename(rejected)}), retrying", flush=True)
    raise RuntimeError(f"{scene}: still letterboxed after {attempts} attempts")


def visible_rect(width, height):
    """Part of the image a TARGET_SCREEN_ASPECT display shows after fill scaling."""
    vis_w = min(width, height * TARGET_SCREEN_ASPECT)
    vis_h = min(height, width / TARGET_SCREEN_ASPECT)
    return ((width - vis_w) / 2, (height - vis_h) / 2, vis_w, vis_h)


def watermark(src_path, dst_path):
    logo = Image.open(os.path.join(TOOLS, "WatermarkLogo.png")).convert("RGBA")
    base = Image.open(src_path).convert("RGBA")
    w, h = base.size
    vx, vy, vw, vh = visible_rect(w, h)

    logo_w = max(48, int(round(vw * LOGO_WIDTH_FRACTION)))
    logo_h = int(round(logo_w * logo.height / logo.width))
    margin = vw * LOGO_MARGIN_FRACTION
    x = int(round(vx + vw - vw * LOGO_RIGHT_INSET_FRACTION - logo_w))
    y = int(round(vy + vh - margin - logo_h))   # PIL y grows downward
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # Soft shadow: offset down 3% of logo width, blur 12%, 45% black, as in Wallz.
    pad = int(logo_w * 0.5)
    shadow = Image.new("RGBA", (logo_w + 2 * pad, logo_h + 2 * pad), (0, 0, 0, 0))
    alpha = logo.split()[3].point(lambda a: int(a * 0.45))
    shadow.paste((0, 0, 0, 255), (pad, pad + int(logo_w * 0.03)), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(logo_w * 0.12))

    base.alpha_composite(shadow, (x - pad, y - pad))
    base.alpha_composite(logo, (x, y))
    base.convert("RGB").save(dst_path, "JPEG", quality=92, optimize=True, progressive=True)


def main(argv):
    with open(os.path.join(TOOLS, "prompts.json")) as f:
        prompts = json.load(f)
    scenes = prompts["scenes"]
    suffix = prompts["suffix"]

    watermark_only = "--watermark-only" in argv
    args = [a for a in argv if not a.startswith("--")]
    wanted = list(scenes) if "--all" in argv else args
    if not wanted:
        sys.exit(__doc__)
    unknown = [s for s in wanted if s not in scenes]
    if unknown:
        sys.exit(f"unknown scene(s): {', '.join(unknown)}")

    os.makedirs(os.path.join(ROOT, "raw"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    key = None if watermark_only else keychain_key()

    for scene in wanted:
        raw_path = os.path.join(ROOT, "raw", f"{scene}.jpg")
        out_path = os.path.join(ROOT, "images", f"{scene}.jpg")
        if not watermark_only:
            print(f"{scene}: generating…", flush=True)
            data, w, h = generate_clean(scene, scenes[scene] + suffix, key)
            with open(raw_path, "wb") as f:
                f.write(data)
            print(f"{scene}: raw {w}x{h}, {len(data) // 1024} KB", flush=True)
        watermark(raw_path, out_path)
        print(f"{scene}: stamped -> images/{scene}.jpg ({os.path.getsize(out_path) // 1024} KB)", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
