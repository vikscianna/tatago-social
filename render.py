"""Render TataGo Instagram graphics.
Usage: python3 render.py days/YYYY-MM-DD/spec.json
Writes <name>.jpg next to spec.json.
Spec item fields:
  name      file name without extension
  format    post (1080x1350) | story (1080x1920)
  layout    image | quote
  audience  famiglie | babysitter
  title     headline (<br> allowed)
  subtitle  optional
  image     asset file name in assets/
  cta       optional button text
  caption   Instagram caption (posts only, not rendered)
"""
import json, sys, base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
FONT = ROOT / "node_modules/@fontsource/poppins/files"

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

HOUSE = ("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'>"
         "<g fill='none' stroke='%23C9A77C' stroke-width='3' stroke-linejoin='round' opacity='0.28'>"
         "<path d='M40 85 L90 45 L140 85 L140 140 L40 140 Z'/><path d='M118 62 L118 48 L130 48 L130 72'/>"
         "<circle cx='90' cy='105' r='14'/><circle cx='90' cy='105' r='5'/></g></svg>")

BADGE = {"famiglie": ("Per le famiglie", "#5E8C6A"), "babysitter": ("Per le babysitter", "#5F82AE")}

def html(s):
    story = s["format"] == "story"
    W, H = (1080, 1920) if story else (1080, 1350)
    quote = s.get("layout") == "quote"
    label, color = BADGE.get(s.get("audience"), ("", "#5E8C6A"))
    img = b64(ROOT / "assets" / s["image"], "image/png")
    sub = f"<p>{s['subtitle']}</p>" if s.get("subtitle") else ""
    cta = f"<div class=cta>{s['cta']}</div>" if s.get("cta") else ""
    if quote:
        body = f"""<div class=badge>{label}</div>
<div class=card><div class=mark>“</div><h1>{s['title']}</h1>{sub}</div>
<img class=round src="{img}">{cta}"""
    else:
        body = f"""<div class=badge>{label}</div><h1>{s['title']}</h1>{sub}
<div class=img><img src="{img}"></div>{cta}"""
    fonts = "".join(
        f"@font-face{{font-family:P;font-weight:{w};src:url({b64(FONT/f'poppins-latin-{w}-normal.woff2','font/woff2')})}}"
        for w in (500, 700, 800))
    return f"""<!doctype html><html><head><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;font-family:P;color:#4A2A12;
 background:#F7F0D6 url("data:image/svg+xml;utf8,{HOUSE}") repeat;background-size:320px;
 display:flex;flex-direction:column;align-items:center;justify-content:{'space-between' if quote else 'flex-start'};
 padding:{130 if story else 70}px 80px {150 if story else 130}px;position:relative;overflow:hidden}}
.badge{{background:{color};color:#fff;font-weight:700;font-size:{34 if story else 28}px;letter-spacing:2px;
 text-transform:uppercase;padding:12px 34px;border-radius:999px;margin-bottom:{40 if story else 28}px}}
h1{{text-wrap:balance;font-weight:800;font-size:{88 if story else 72}px;line-height:1.08;text-align:center;letter-spacing:-1px}}
p{{text-wrap:balance;font-weight:500;font-size:{44 if story else 36}px;line-height:1.3;text-align:center;margin-top:26px;color:#6B4423}}
.img{{flex:1;display:flex;align-items:center;justify-content:center;width:100%;margin:{50 if story else 30}px 0;min-height:0}}
.img img{{width:{920 if story else 900}px;max-height:100%;object-fit:cover;object-position:center 20%;border-radius:56px;
 box-shadow:0 24px 60px rgba(74,42,18,.18);border:10px solid #fff}}
.card{{background:#FFFBEE;border-radius:56px;padding:{90 if story else 70}px 70px;box-shadow:0 24px 60px rgba(74,42,18,.14);
 position:relative;width:100%}}
.card h1{{font-size:{92 if story else 76}px}}
.mark{{position:absolute;top:-40px;left:50px;font-size:200px;line-height:1;color:{color};font-weight:800}}
.round{{width:{420 if story else 300}px;height:{420 if story else 300}px;border-radius:50%;object-fit:cover;
 border:10px solid #fff;box-shadow:0 20px 50px rgba(74,42,18,.18)}}
.cta{{background:{color};color:#fff;font-weight:700;font-size:{46 if story else 38}px;padding:24px 58px;border-radius:999px;
 box-shadow:0 10px 0 rgba(0,0,0,.25)}}
.site{{position:absolute;right:56px;bottom:{70 if story else 50}px;font-weight:700;font-size:{40 if story else 32}px;color:#6B4423}}
.logo{{position:absolute;left:50px;bottom:{50 if story else 30}px;height:{110 if story else 88}px}}
</style></head><body>{body}
<div class=site>tatago.it</div><img class=logo src="{b64(ROOT/'assets/logo.png','image/png')}">
</body></html>""", W, H

def main(spec):
    spec = pathlib.Path(spec).resolve()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for s in json.loads(spec.read_text()):
            h, W, H = html(s)
            pg = b.new_page(viewport={"width": W, "height": H})
            pg.set_content(h); pg.wait_for_timeout(300)
            dst = spec.parent / f"{s['name']}.jpg"
            pg.screenshot(path=str(dst), type="jpeg", quality=92)
            pg.close()
            print(dst)
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
