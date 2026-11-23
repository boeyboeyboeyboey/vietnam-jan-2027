import json, base64, html, sys, os, re
pics = json.load(open(sys.argv[1]))
OUTDIR = sys.argv[2]

def url(lid, p):
    for k, v in {'.J': '.jpeg', '.j': '.jpg'}.items():
        if p.endswith(k): p = p[:-2] + v
    if p.startswith('H:'): p = f"hosting/Hosting-{base64.b64encode(('StaySupplyListing:'+lid).encode()).decode()}/original/{p[2:]}"
    elif p.startswith('I:'): p = f"hosting/Hosting-{lid}/original/{p[2:]}"
    elif p.startswith('M:'): p = f"miso/Hosting-{lid}/original/{p[2:]}"
    return "https://a0.muscache.com/im/pictures/" + p

# Hero photos: Unsplash License (free, no attribution required; credited anyway)
HERO = {
 "hcmc": ("https://images.unsplash.com/photo-1673934149508-318260ef31f2", "Anh Phan", "https://unsplash.com/photos/tyMDpHN7BZk"),
 "danang": ("https://images.unsplash.com/photo-1732827503735-511f7ccd187e", "Yash Parashar", "https://unsplash.com/photos/bLn5N9ldqfA"),
}

# id, name, short, dates, nights, checkin, checkout, accent, note, listings
CITIES = [
 ("hcmc", "Ho Chi Minh City", "HCMC", "4–7 Jan 2027", 3, "2027-01-04", "2027-01-07", "#ff9f7a",
  "Ranked best first. Under 1.2 km to Ben Thanh comes first. HCMC1 is no longer available. HCMC6 and HCMC9 added later. HCMC7 and HCMC8 cut for price. All within 2.5 km of Ben Thanh Market, 3+ bathrooms.", [
  ("HCMC3","1731138706065239581","Cozy 5BR/5BA House","District 1 · 1.0 km to Ben Thanh · 2.5 km to shopping street","S$1,091","S$40","5 bedrooms · 8 beds · 5 baths","5.0★ (9) · Guest Favourite · Superhost",
   ["Walkable to Ben Thanh (1.0 km)","Most beds + baths this close to centre","New, clean","Every review 5★"],
   ["Shopping street: 2.5 km, Grab or long walk","Only 9 reviews","Same house also listed at S$1,602, don't book that one","Only 1 bathroom shown in photos","No living-room AC seen","Shophouse alley"]),
  ("HCMC9","39879364","7BR House near Ben Thanh","District 1 · 0.4 km to Ben Thanh · 3.2 km to shopping street","S$853","S$32","7 bedrooms · 7 queen beds · 6.5 baths","4.67★ (9)",
   ["Walkable to Ben Thanh (0.4 km), closest of all","Cheaper than HCMC3 (S$32 vs S$40)","6 bedrooms have their own bathroom","Big ground-floor living room with AC","Rooftop + reading room","Washer + dryer"],
   ["Shopping street: 3.2 km, Grab or long walk","All 9 reviews are from Dec 2019 to Mar 2020, none since","Same house listed again by another host with 0 reviews","Photos show only 5 of 7 bedrooms","Neighbours close, some noise (Mar 2020)","7 queen beds, so 2 pairs share","Free cancel ends soon (5 Dec)"]),
  ("HCMC2","1311605703773163437","Haina's 5BR House","District 3 · 1.6 km to Ben Thanh · 1.8 km to shopping street","S$753","S$28","5 bedrooms · 6 beds · 4.5 baths","4.88★ (16) · Superhost",
   ["Walkable to Ben Thanh (1.6 km)","Enough beds for 9 with little sharing","Living room has AC + TV","Rooftop terrace"],
   ["Shopping street: 1.8 km, Grab or long walk","\"Old house, AC doesn't work well\" (Dec 2024)","Alley","Only 16 reviews"]),
  ("HCMC6","1672471341262461731","5BR Townhouse + Rooftop BBQ","District 1 (Da Kao) · 2.1 km to Ben Thanh · 1.7 km to shopping street","S$1,135","S$42","5 bedrooms · 7 beds · 6 baths","4.97★ (30) · Guest Favourite · Superhost",
   ["Every bedroom has its own bathroom","Beds for 9 (3 king, 2 queen, 2 sofa beds)","Rooftop BBQ","Washer + dryer","Stores luggage before check-in and after check-out","Same hosts as the old HCMC1"],
   ["Ben Thanh: 2.1 km, Grab or long walk","Shopping street: 1.7 km, Grab or long walk","Priciest","Wooden doors let noise through (Sep 2026)","No traffic light to cross outside (Jul 2026)"]),
  ("HCMC4","27990178","Phoenix's 5BR House","District 1 (Da Kao) · 2.0 km to Ben Thanh · 1.8 km to shopping street","S$813","S$30","5 bedrooms · 5 baths","4.85★ (238) · Superhost",
   ["Most reviewed, consistently good","Every room has its own bathroom + AC","Host fixes problems fast"],
   ["Ben Thanh: 2.0 km, Grab or long walk","Shopping street: 1.8 km, Grab or long walk","Weak portable AC in living room","Rooster from ~4:30am","Past ant/cockroach reports (one group moved out, Jan 2024)","5 queen beds, so 4 pairs share"]),
  ("HCMC5","1587035319818469396","D1 Entire-Floor Apartment","District 1 (Tan Dinh) · 2.2 km to Ben Thanh · 1.4 km to shopping street","S$567","S$21","4 bedrooms · 4 beds · 4 baths","4.5★ (8)",
   ["Walkable to shopping street (1.4 km)","Close to budget","Good local food nearby","Whole floor to yourselves"],
   ["Ben Thanh: 2.2 km, Grab or long walk","Only 8 reviews","Faulty shower heater (Mar 2026)","Street horn noise (Feb 2026)","Missing kitchen items, sink smell (Feb 2026)","4 beds for 9"]),
 ]),
 ("danang", "Da Nang", "Da Nang", "7–11 Jan 2027", 4, "2027-01-07", "2027-01-11", "#6fd6d1",
  "Ranked best first. Private pool + central costs about S$26–31 per person per night.", [
  ("DN1","1500369668192839406","Cam On Pool Villa","1.1 km from Han Market","S$923","S$26","4 bedrooms · 5 beds · 4 baths","4.73★ (33) · private pool ~8–10 m",
   ["Biggest private pool","~1 km to Han Market"],
   ["No warm water some evenings, few towels/dishes","Construction + karaoke nearby (Jan 2025)","Dining table seats 6","TV/washer not seen in photos"]),
  ("DN2","1598281711142232998","Luxury 4BR Home","1.9 km from Han Market","S$697","S$19","4 bedrooms · 8 beds · 4.5 baths","5.0★ (10) · Guest Favourite · Superhost",
   ["Under budget","All reviews 5★","Washer + dryer","Rooftop"],
   ["No pool","Only 10 reviews","Living room has a portable cooler, not AC","Construction crane nearby"]),
  ("DN3","1499048958220731670","Da Nang Pool Villa (Olivia)","1.8 km from Han Market","S$1,101","S$31","4 bedrooms · 5 beds · 5 baths","4.94★ (100) · Guest Favourite · Superhost",
   ["Best track record","5 bathrooms","8-seat dining"],
   ["Pool is a small plunge pool (~3×2 m)","\"5 rooms\" was 4 + curtained rooftop (May 2025)","Market-alley entrance","Weak water pressure"]),
  ("DN4","1119292625144112269","Han Market Indoor-Pool Villa","0.3 km from Han Market","S$1,049","S$29","4 bedrooms · 4 beds · 4 baths","4.77★ (13) · indoor pool",
   ["Best location","Indoor pool works in rain","No complaints in reviews"],
   ["Some photos look AI-generated, ask for real ones","4 beds for 9","Washer not shown"]),
  ("DN5","1173705612210421870","CAFE HOUSE","1.5 km from Han Market","S$670","S$19","5 bedrooms · 5 beds · 4 baths","4.8★ (56)",
   ["Cheapest","5 bedrooms, all queen beds","Washer + dryer"],
   ["No pool","Repeated bad-smell reports","Cockroach (Nov 2025)","Living room has fan only","Dining table seats 6"]),
 ]),
]

CANC = {'1672471341262461731': 'Free cancel until 30 Dec', '1587035319818469396': 'Free cancel until 3 Jan', '1575977622753200671': 'No free cancellation', '1483784188953758037': 'Free cancel until 30 Dec', '27914684': 'No free cancellation', '1697772649812663470': 'Free cancel until 3 Jan', '1311605703773163437': 'Free cancel until 3 Jan', '27990178': 'Free cancel until 30 Dec', '39342498': 'No free cancellation', '965804095820583217': 'Free cancel until 30 Dec', '1731138706065239581': 'Free cancel until 30 Dec', '1500369668192839406': 'Free cancel until 8 Dec', '1499048958220731670': 'Free cancel until 8 Dec', '1119292625144112269': 'Free cancel until 8 Dec', '1598281711142232998': 'Free cancel until 24 Dec', '1173705612210421870': 'Free cancel until 2 Jan', '1386982353850299078': 'Free cancel until 30 Dec', '39879364': 'Free cancel until 5 Dec', '1733492588128339446': 'Free cancel until 3 Jan'}
WISH = set()
WISH_OUT = {"hcmc": [
 ("Cau Kho 3BR, District 1","S$473","1483784188953758037","Too far: 2.2 km to Ben Thanh, 3.7 km to shopping street. Oct 2025: sewage backup flooded the ground floor."),
 ("Grand Riverside 4BR, District 4","S$585","1232973284686915745","Only 2 bathrooms and 4 beds for 9. Apr 2026: a bathroom unusable + mould. Jun 2026: host charged a guest for a sheet they say they didn't damage."),
 ("The Echo D1 3BR","S$543","1380356239307975966","Only 2 bathrooms and 4 beds for 9. Nov 2025 1★: \"looked NOTHING like the photos\", dirty."),
]}
CHECKED_OUT = {"hcmc": [
 ("HCMC7: Haina's 6BR House, Bui Vien","S$1,374","1386982353850299078","0.9 km, 4.91★ (81), but S$51 per person per night."),
 ("HCMC8: Japanese 5BR Townhouse","S$1,458","1733492588128339446","1.0 km, 5.0★ (6), but S$54 per person per night."),
 ("Cherry Blossom Calmette 7BR","S$1,593–2,547","1484669482261429245","0.6 km. Rooftop city view, but Apr 2026 1★: \"very dirty\". Was a small hotel, rooms have their own locks. Listed twice at different prices. Some reviews look copied."),
 ("Cherry Blossom Bui Vien 6BR","S$1,170–1,919","1468701455317785569","1.1 km. Oct 2026 2★: rooms differ from photos, broken tap, cloudy water. Hostel-style key cards, Bui Vien noise. Listed 3 times."),
 ("Luxury Family Stay 5BR","S$1,602","1743536761663263255","Same house as HCMC3 at a higher price."),
 ("Central 7BR House","S$920","40789691","Same text as HCMC9 under another host, 0 reviews."),
 ("Japanese Home 5BR","S$1,086","1735427000719449892","1.0 km. No reviews, almost no description."),
 ("Luxury Villa 5BR","S$1,242","1697600535579250591","1.0 km. Host is Vihomes (rejected before). Description warns photos may not match. 1 hidden review."),
 ("District 3 Alley House 5BR","S$728","1459896296341870618","1.0 km, cheap, living room has AC. No reviews, 3 full baths, 5 beds for 9."),
 ("Japandi 5BR","S$586","1820275252892652014","1.1 km. No reviews, 5 beds for 9."),
 ("Oula Home 4BR","S$690","1755119692483380160","0.9 km. Washer is in the building, so likely an apartment. 1 hidden review."),
 ("Haina's 6BR, Nguyen Cu Trinh","S$1,120","1469368568115213026","1.5 km to Ben Thanh, too far. 4.83★ (63), same host as HCMC2."),
 ("Ensuite 6BR near Bui Vien","S$1,117","1783917509438296964","1.6 km, too far. 5.0★ (7)."),
 ("House for 14–16, District 1","S$1,891","1297014489961274442","1.4 km and S$70 per person per night."),
 ("Luxury 6BR Villa, sauna","S$2,568","1763826597011214749","0.9 km, 5.0★ (16), but S$95 per person per night."),
 ("7BR 12-bed house","S$2,026","1638432784352009395","1.2 km. No reviews, S$75 per person per night."),
 ("Thien Vi House (5 listings)","S$1,756–5,275","1799978339713900629","All new, no reviews, S$65–195 per person per night."),
 ("Entire Villa 4 or 7 ensuite (3 listings)","S$1,276–2,850","1626126945604830886","4BR ones have 4 beds for 9. The 7BR is S$106 per person per night."),
 ("Other 4–5BR houses (3 listings)","S$681–961","1334823230471706143","1.4–1.6 km, no reviews."),
 ("Bui Vien homestays (2 listings)","S$368–375","1043434707923558492","3 bedrooms, rated 3.9–4.0."),
 ("Resort villas with free car to Nha Trang (3 listings)","S$3,156–8,353","15979750","Odd listings, far over budget."),
 ("About 85 apartments","","","Cut for the apartment legal risk that lost HCMC1."),
]}

def esc(s): return html.escape(s, quote=True)

# Single deliberate night look: deep ink background, soft neon accent per city.
CSS = '''
:root{color-scheme:dark;--bg:#0e1116;--panel:#151a22;--ink:#eef1f5;--mut:#9aa4b2;--rule:#252c37;--plus:#8fe3a8;--minus:#ff9b9b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Be Vietnam Pro",system-ui,sans-serif;font-variant-numeric:tabular-nums}
a{color:inherit}
.hero{position:relative;min-height:340px;display:flex;align-items:flex-end;background:var(--bg) center/cover no-repeat;padding:20px max(16px,env(safe-area-inset-left)) 30px}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,17,22,.35) 0%,rgba(14,17,22,.55) 45%,var(--bg) 100%)}
.hero .in{position:relative;width:100%;max-width:880px;margin:0 auto}
.top{position:absolute;z-index:1;top:calc(14px + env(safe-area-inset-top));left:max(16px,env(safe-area-inset-left));right:max(16px,env(safe-area-inset-right));max-width:880px;margin:0 auto;display:flex;justify-content:space-between;font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.top a{text-decoration:none;opacity:.85;background:rgba(14,17,22,.45);padding:6px 10px;border-radius:4px;backdrop-filter:blur(6px)}
.top a:hover{opacity:1}
.hero h1{font-size:clamp(2.6rem,9vw,4.8rem);line-height:.95;margin:0 0 10px;font-weight:800;letter-spacing:-.03em;text-shadow:0 2px 24px rgba(0,0,0,.4)}
.hero .dates{font-size:1.1rem;font-weight:600;color:var(--acc)}
.hero .note{margin:8px 0 0;max-width:60ch;color:#d6dbe3}
.wrap{max-width:880px;margin:0 auto;padding:8px max(16px,env(safe-area-inset-left)) 40px}
.opt{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:18px;margin:0 0 18px}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}
.code{font-weight:800;font-size:1.05rem;letter-spacing:.04em;color:var(--bg);background:var(--acc);padding:6px 10px;border-radius:4px;line-height:1.2}
.row h2{margin:0;font-size:1.2rem;line-height:1.25}
.row h2 a{text-decoration:none;border-bottom:1px solid var(--rule)}.row h2 a:hover{border-color:var(--acc)}
.meta{margin:4px 0 0;color:var(--mut);font-size:.88rem}
.price{text-align:right;border-left:2px solid var(--acc);padding-left:14px;min-width:130px}
.price b{display:block;font-size:2.1rem;line-height:1;font-weight:800;color:var(--acc);letter-spacing:-.02em}
.price span{display:block;font-size:.75rem;color:var(--mut);margin-top:4px}
.price i{display:block;font-style:normal;font-size:.85rem;margin-top:4px}
.price em{display:block;font-style:normal;font-size:.75rem;margin-top:4px}.price em.ok{color:var(--plus)}.price em.no{color:var(--minus)}
.strip{display:flex;gap:4px;overflow-x:auto;margin:16px -18px 4px;padding:0 18px;scroll-snap-type:x proximity}
.strip img{height:230px;width:auto;aspect-ratio:3/2;object-fit:cover;display:block;scroll-snap-align:start;background:var(--rule);border-radius:3px}
.count{font-size:.78rem;color:var(--mut);margin:0 0 12px}
.fa{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.fa h3{margin:0 0 6px;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}
.for h3{color:var(--plus)}.against h3{color:var(--minus)}
ul{margin:0;padding:0;list-style:none}li{padding:4px 0 4px 18px;position:relative;border-top:1px solid var(--rule);font-size:.95rem}
.for li::before{content:"+";position:absolute;left:2px;color:var(--plus);font-weight:800}
.against li::before{content:"−";position:absolute;left:2px;color:var(--minus);font-weight:800}
span.wish{display:inline-block;margin-left:8px;font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--bg);background:var(--acc);padding:2px 7px;border-radius:3px;vertical-align:middle}
span.wish.pick{background:var(--ink);color:var(--bg)}
.sep{margin:28px 0 12px;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}.wl{border:1px dashed var(--rule);border-radius:6px;padding:14px 18px;margin:0 0 18px}.wl h3{margin:0 0 6px;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}.wl li{border-top:1px solid var(--rule);padding:6px 0;font-size:.92rem}.wl li::before{content:none}.wl b{color:var(--acc)}
footer{color:var(--mut);font-size:.78rem;padding-top:6px}
footer a{color:var(--mut)}
@media (max-width:620px){.row{grid-template-columns:auto 1fr}.price{grid-column:1/-1;text-align:left;border-left:0;border-top:1px solid var(--rule);padding:10px 0 0;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}.price span,.price i{margin:0}.strip img{height:180px}.fa{grid-template-columns:1fr}.hero{min-height:300px}}
.home{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.home a{position:relative;text-decoration:none;padding:40px max(20px,env(safe-area-inset-left));display:flex;flex-direction:column;justify-content:flex-end;gap:6px;background:var(--bg) center/cover no-repeat;overflow:hidden}
.home a::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,17,22,.2),rgba(14,17,22,.85));transition:background .2s}
.home a:hover::before,.home a:focus-visible::before{background:linear-gradient(180deg,rgba(14,17,22,.05),rgba(14,17,22,.75))}
.home a>*{position:relative}
.home h2{font-size:clamp(2.4rem,7vw,4.4rem);line-height:.95;margin:0;font-weight:800;letter-spacing:-.03em}
.home p{margin:0;font-size:1.05rem;font-weight:600;color:var(--acc)}
.home small{color:#d6dbe3;font-size:.95rem}
.home .t{position:fixed;top:0;left:0;right:0;z-index:2;text-align:center;padding:calc(14px + env(safe-area-inset-top)) 0 0;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:.78rem;color:#eef1f5;text-shadow:0 1px 8px rgba(0,0,0,.6)}
.home .cr{position:fixed;bottom:8px;right:12px;z-index:2;font-size:.7rem;color:#c9ced6;text-shadow:0 1px 6px rgba(0,0,0,.7)}
@media (max-width:620px){.home{grid-template-columns:1fr}.home a{min-height:50vh}}
'''

HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap">
<style>{css}</style></head>'''

TOPTAG = ' <span class="wish pick">Top pick</span>'
WISHTAG = ' <span class="wish">On your wishlist</span>'
VOTED = {"1483784188953758037"}
VOTEDTAG = ' <span class="wish">Voted from previous wishlist</span>'

def wishout(cid, ci, co, src=WISH_OUT, title="Also on your wishlist, not included"):
    rows = src.get(cid)
    if not rows: return ""
    def one(n, p, lid, why):
        name = f'<a href="https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9" target="_blank" rel="noopener">{esc(n)}</a>' if lid else esc(n)
        return f'<li>{name}{VOTEDTAG if lid in VOTED else ""}{f" <b>{p}</b>" if p else ""} · {esc(why)}</li>'
    li = "".join(one(*r) for r in rows)
    return f'<section class="wl"><h3>{title}</h3><ul>{li}</ul></section>'

def price_from(items): return min(int(i[5][2:]) for i in items)

for idx, (cid, cname, short, dates, nights, ci, co, acc, note, items) in enumerate(CITIES):
    other = CITIES[1-idx]
    himg, hby, hlink = HERO[cid]
    opts = []
    far_done = False
    for code, lid, name, loc, tot, pp, rooms, rating, pro, con in items:
        m = re.search(r'([\d.]+) km to Ben Thanh', loc)
        if m and float(m.group(1)) > 1.2 and not far_done:
            opts.append('<h3 class="sep">Over 1.2 km from Ben Thanh</h3>'); far_done = True
        link = f"https://www.airbnb.com.sg/rooms/{lid}?check_in={ci}&check_out={co}&adults=9"
        imgs = ''.join(f'<a href="{esc(url(lid,p))}?im_w=1200" target="_blank" rel="noopener"><img src="{esc(url(lid,p))}?im_w=480" width="345" height="230" loading="lazy" alt="{code} photo {i+1}"></a>' for i,p in enumerate(pics[lid]))
        opts.append(f'''<article class="opt" id="{code.lower()}">
<div class="row"><span class="code">{code}</span>
<div><h2><a href="{link}" target="_blank" rel="noopener">{esc(name)} ↗</a>{WISHTAG if lid in WISH else ""}{TOPTAG if code in ("HCMC3", "DN1") else ""}</h2><p class="meta">{esc(loc)}<br>{esc(rooms)} · {esc(rating)}</p></div>
<div class="price"><b>{pp}</b><span>per person / night</span><i>{tot} total · {nights} nights</i><em class="{"no" if CANC[lid].startswith("No") else "ok"}">{CANC[lid]}</em></div></div>
<div class="strip">{imgs}</div><p class="count">{len(pics[lid])} photos · swipe →</p>
<div class="fa"><div class="for"><h3>For</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in pro)}</ul></div>
<div class="against"><h3>Against</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in con)}</ul></div></div>
</article>''')
    page = HEAD.format(title=f"{cname} · Jan 2027 stays", css=CSS) + f'''<body style="--acc:{acc}">
<header class="hero" style="background-image:url('{himg}?auto=format&fit=crop&w=1800&q=70')">
<div class="top"><a href="./">← All cities</a><a href="{other[0]}.html">{esc(other[2])} →</a></div><div class="in">
<h1>{esc(cname)}</h1><div class="dates">{dates} · {nights} nights · 9 people</div><p class="note">{esc(note)}</p>
</div></header>
<main class="wrap">{''.join(opts)}{wishout(cid,ci,co)}{wishout(cid,ci,co,CHECKED_OUT,'Also checked 23 Nov, not included')}
<footer>Airbnb totals before tax. Prices and availability checked 22–23 Nov 2026. Tap a photo for full size, a title to open Airbnb. Header photo: <a href="{hlink}" target="_blank" rel="noopener">{hby} / Unsplash</a>.</footer></main></body></html>'''
    open(os.path.join(OUTDIR, f"{cid}.html"), 'w').write(page)

tiles = ''.join(f'''<a href="{c[0]}.html" style="--acc:{c[7]};background-image:url('{HERO[c[0]][0]}?auto=format&fit=crop&w=1200&q=70')"><h2>{esc(c[1])}</h2><p>{c[3]} · {c[4]} nights</p><small>{len(c[9])} options · from S${price_from(c[9])} per person / night</small></a>''' for c in CITIES)
credit = ' · '.join(f'<a href="{HERO[c[0]][2]}" target="_blank" rel="noopener">{HERO[c[0]][1]}</a>' for c in CITIES)
open(os.path.join(OUTDIR, "index.html"), 'w').write(HEAD.format(title="Vietnam Jan 2027 · stays", css=CSS) + f'<body><div class="home"><div class="t">Vietnam · Jan 2027 · 9 people</div>{tiles}</div><div class="cr">Photos: {credit} / Unsplash</div></body></html>')
print("ok", sum(len(pics[i[1]]) for c in CITIES for i in c[9]))
