"""Download every illustration listed in assets.json from Behance and save
web-ready copies under assets/:

  assets/banner.webp                      profile banner (hero)
  assets/books/<id>/cover.webp            808px cover
  assets/books/<id>/NN.webp               each page, max 1600px wide
  assets/books/<id>/NN-thumb.webp         each page, 480px wide

Run by .github/workflows/fetch-images.yml, or locally: pip install pillow && python tools/fetch_images.py
Existing files are skipped, so re-running only fetches what is new.
"""
import io, json, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CDN = "https://mir-s3-cdn-cf.behance.net/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Referer": "https://www.behance.net/"}

def get(urls):
    for u in urls:
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                    return r.read()
            except Exception as e:
                last = f"{u}: {e}"
                time.sleep(1 + attempt)
    raise RuntimeError(last)

def save(img, path, width, quality=82):
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "WEBP", quality=quality, method=6)

def open_rgb(data):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 250, 243))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")

def main():
    data = json.loads((ROOT / "assets.json").read_text(encoding="utf-8"))
    failed = []
    banner = ROOT / "assets" / "banner.webp"
    if not banner.exists():
        try:
            save(open_rgb(get([data["banner"]])), banner, 2400, 90)
        except Exception as e:
            failed.append(str(e))
    for b in data["books"]:
        d = ROOT / "assets" / "books" / b["id"]
        cover = d / "cover.webp"
        if not cover.exists():
            try:
                save(open_rgb(get([CDN + "projects/808/" + b["cover"], CDN + "projects/404/" + b["cover"]])), cover, 808)
            except Exception as e:
                failed.append(str(e))
        for n, f in enumerate(b["pages"], 1):
            full, thumb = d / f"{n:02d}.webp", d / f"{n:02d}-thumb.webp"
            if full.exists() and thumb.exists():
                continue
            try:
                im = open_rgb(get([CDN + "project_modules/" + s + "/" + f for s in ("1400", "max_1200", "fs", "disp", "max_632")]))
                save(im, full, 1600)
                save(im, thumb, 480, 78)
            except Exception as e:
                failed.append(str(e))
        print(b["title"], "ok")
    if failed:
        print("Failed:", *failed, sep="\n  ")
        sys.exit(1)

if __name__ == "__main__":
    main()
