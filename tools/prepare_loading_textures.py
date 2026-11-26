"""Prepare cached WCW loading-screen PNGs; requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageFilter, __version__ as pillow_version

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("cache", type=Path)
    p.add_argument("--scale", type=float, default=2.0, choices=[n/2 for n in range(2,16)])
    p.add_argument("--method", choices=["nearest","bilinear","bicubic","lanczos"], default="lanczos")
    p.add_argument("--sharpen", type=int, choices=range(101), default=0, metavar="0-100")
    args = p.parse_args()
    if not args.source.is_dir():
        p.error("source must be an extracted loading-screen directory")
    if args.cache.resolve().is_relative_to(args.source.resolve()):
        p.error("cache must be outside the source directory")
    files = sorted(args.source.rglob("*.png"))
    if not files:
        p.error("no PNG files found")
    args.cache.mkdir(parents=True, exist_ok=True)
    records = []
    for src in files:
        raw = src.read_bytes()
        with Image.open(src) as im:
            if im.size != (512,240):
                print("Skipping non-loading-screen dimensions:", src)
                continue
            settings = dict(source_sha256=hashlib.sha256(raw).hexdigest(),
                            scale=args.scale, method=args.method, sharpen=args.sharpen,
                            pillow=pillow_version, schema=1)
            key = hashlib.sha256(json.dumps(settings,sort_keys=True).encode()).hexdigest()
            dest = args.cache / (key+".png")
            size = (int(im.width*args.scale),int(im.height*args.scale))
            valid = False
            if dest.exists():
                try:
                    with Image.open(dest) as cached:
                        valid = cached.size == size and cached.mode == "RGBA"
                        cached.verify()
                except (OSError, ValueError):
                    valid = False
            if not valid:
                rgba = im.convert("RGBA")
                # Premultiplied-alpha resampling avoids transparent-edge halos.
                out = rgba.resize(size, getattr(Image.Resampling,args.method.upper()))
                if args.sharpen:
                    alpha = out.getchannel("A")
                    out = out.convert("RGB").filter(ImageFilter.UnsharpMask(
                        radius=1.0,percent=args.sharpen,threshold=3)).convert("RGBA")
                    out.putalpha(alpha)
                tmp = dest.with_suffix(".tmp")
                out.save(tmp,format="PNG")
                tmp.replace(dest)
            records.append(dict(source=src.relative_to(args.source).as_posix(),
                                cache=dest.name,width=size[0],height=size[1],**settings))
            print(("Cached" if valid else "Generated"),src.name,size)
    if not records:
        p.error("no 512x240 loading screens found")
    tmp = args.cache / "manifest.tmp"
    tmp.write_text(json.dumps(records,indent=2)+"\n",encoding="utf-8")
    tmp.replace(args.cache / "manifest.json")
    print("Prepared",len(records),"loading screens")

if __name__ == "__main__":
    main()
