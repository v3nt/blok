TEMPLATE = '<!doctype html><html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Class schedule — BLOK &amp; Mission E1</title><style>\n:root{--bd:#e3e3e8}\n*{box-sizing:border-box}\nbody{margin:0;font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:#16161a;background:#fafafb}\nheader{background:#16161a;color:#fff;padding:14px 18px}\nheader h1{margin:0;font-size:19px;font-weight:700}\nheader p{margin:5px 0 0;font-size:13px;color:#a9a9b4}\nheader a{color:#c8c8d4}\n#lg{margin:7px 0 0;display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px}\n#lg span{display:inline-flex;align-items:center;gap:5px;color:#e6e6ea}\n#lg i{width:8px;height:8px;border-radius:50%;display:inline-block}\n#lg b{font-weight:700}\n.bar{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--bd);padding:10px 18px;font-size:13.5px}\n.bar .top{display:flex;flex-wrap:wrap;gap:9px 18px;align-items:center}\n.bar label{display:inline-flex;gap:6px;align-items:center;cursor:pointer;white-space:nowrap}\n.bar .sep{width:1px;height:18px;background:var(--bd)}\n.bar .n{color:#87878f;font-size:12px}\n#shown{color:#55555f;font-size:12.5px;font-variant-numeric:tabular-nums}\n.grp{margin-top:9px;padding-top:8px;border-top:1px dashed var(--bd)}\n.grp h3{margin:0 0 6px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#6b6b76}\n.grp .row{display:flex;flex-wrap:wrap;gap:7px 14px}\n.grp .row.fav{display:none;padding:5px 8px 6px;margin-bottom:6px;background:#fffaeb;border:1px solid #f0dfa8;border-radius:8px}\n.grp .row.fav.on{display:flex}\n.grp .row.fav::before{content:"★";color:#e8a90c;font-size:12px;align-self:center;margin-right:2px}\n.chip{display:inline-flex;gap:6px;align-items:center;white-space:nowrap}\n.dot{width:9px;height:9px;border-radius:50%;display:inline-block}\n.star{border:0;background:none;cursor:pointer;font-size:14px;line-height:1;padding:0 2px;color:#c9c9d1}\n.star[aria-pressed="true"]{color:#e8a90c}\n#reset{border:1px solid var(--bd);background:#f4f4f6;border-radius:7px;padding:5px 11px;font:inherit;font-size:12.5px;cursor:pointer}\n#reset:hover{background:#eaeaee}\n#booked{background:#eaf3fc;border-bottom:1px solid #cfe0f2;padding:11px 18px;font-size:13px;display:none}\n#booked h2{margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#1f7fd1}\n#booked ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:4px}\n#booked li{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}\n#booked .bt{font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}\n#booked .bl{color:#55555f}\n#booked .bn{color:#87878f;font-size:12px}\ntable{width:100%;border-collapse:collapse;background:transparent}\nth{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:#6b6b76;padding:9px 10px;border-bottom:1px solid var(--bd)}\ntd{padding:8px 10px;border-bottom:1px solid #f0f0f3;font-size:13.5px;vertical-align:middle}\ntr.day td{background:#eeeef1;font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#44444c;padding:7px 10px}\ntbody tr[data-state="full"] td:not(:last-child){opacity:.55}\n.pill{display:inline-block;padding:2px 8px;border-radius:99px;color:#fff;font-size:11.5px;font-weight:600;white-space:nowrap}\n.t{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600}\n.st{font-weight:600;white-space:nowrap}\n.mut{color:#6b6b76}\n.empty{padding:26px;text-align:center;color:#6b6b76}\n#main{background:#fff}\n@media(max-width:640px){td,th{padding:7px 6px;font-size:12.5px}.mins{display:none}.bar,header,#booked{padding-left:11px;padding-right:11px}}\n</style></head><body>\n<header><h1>Class schedule — BLOK &amp; Mission E1</h1>\n@@SUB@@\n<div id="lg"></div></header>\n<div class="bar">\n<div class="top">\n<label><input type="checkbox" id="av"> Bookable now only</label>\n<label><input type="checkbox" id="hf"> Hide full</label>\n<label><input type="checkbox" id="hw"> Hide weekday 8:00am–5:25pm</label>\n<span class="sep"></span><button id="reset">Reset filters</button>\n<span id="shown"></span>\n</div>\n<div class="grp"><h3>Mission E1</h3><div class="row fav" id="favM"></div><div class="row" id="catsM"></div></div>\n<div class="grp"><h3>BLOK — Clapton &amp; Shoreditch</h3><div class="row fav" id="favB"></div><div class="row" id="catsB"></div></div>\n</div>\n<div id="booked"></div>\n<div id="main"><table><thead><tr><th>Time</th><th class="mins">Min</th><th>Class</th><th>Instructor</th><th>Studio</th><th>Booking status</th></tr></thead><tbody id="tb"></tbody></table></div>\n<div class="empty" id="none" style="display:none">No classes match these filters.</div>\n<script>\n@@DATA@@\nvar LS={a:\'blokAvailOnly\',f:\'blokHideFull\',w:\'blokHideWorkHours\',t:\'blokTypes\',m:\'blokTypesM\',v:\'blokFavs\'};\nfunction g(k,d){try{var v=localStorage.getItem(k);return v===null?d:JSON.parse(v)}catch(e){return d}}\nfunction s(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}\nfunction clean(saved,valid){\n if(!Array.isArray(saved))return valid.slice();\n var out=saved.filter(function(c){return valid.indexOf(c)>-1});\n return out.length?out:valid.slice();\n}\nvar selB=clean(g(LS.t,null),orderB), selM=clean(g(LS.m,null),orderM);\nvar favs=g(LS.v,null);\nif(!Array.isArray(favs))favs=[];\nfavs=favs.filter(function(k){var p=k.split(\'|\');return (p[0]===\'B\'&&orderB.indexOf(p[1])>-1)||(p[0]===\'M\'&&orderM.indexOf(p[1])>-1)});\nvar av=document.getElementById(\'av\'),hf=document.getElementById(\'hf\'),hw=document.getElementById(\'hw\');\nav.checked=!!g(LS.a,false);hf.checked=!!g(LS.f,false);hw.checked=!!g(LS.w,false);\nvar CHIPS={M:[],B:[]};\nfunction build(wrapId,order,sel,venue){\n order.forEach(function(c){\n  var l=document.createElement(\'label\');l.className=\'chip\';\n  var i=document.createElement(\'input\');i.type=\'checkbox\';i.checked=sel.indexOf(c)>-1;i.dataset.c=c;\n  i.addEventListener(\'change\',function(){sync(venue)});\n  var d=document.createElement(\'span\');d.className=\'dot\';d.style.background=PC[c];\n  var t=document.createElement(\'span\');t.textContent=c;\n  var n=document.createElement(\'span\');n.className=\'n\';n.textContent=CATS[c]||0;\n  l.appendChild(i);l.appendChild(d);l.appendChild(t);l.appendChild(n);\n  var b=document.createElement(\'button\');b.className=\'star\';b.type=\'button\';\n  var key=venue+\'|\'+c,on=favs.indexOf(key)>-1;\n  b.setAttribute(\'aria-pressed\',on?\'true\':\'false\');\n  b.textContent=on?\'★\':\'☆\';\n  b.title=(on?\'Unfavourite \':\'Favourite \')+c;\n  b.addEventListener(\'click\',function(){\n   var j=favs.indexOf(key);\n   if(j>-1)favs.splice(j,1);else favs.push(key);\n   s(LS.v,favs);\n   place(venue);\n  });\n  var chip=document.createElement(\'span\');chip.className=\'chip\';\n  chip.appendChild(l);chip.appendChild(b);\n  CHIPS[venue].push({cat:c,key:key,el:chip,star:b});\n });\n place(venue);\n}\nfunction place(venue){\n var favRow=document.getElementById(venue===\'M\'?\'favM\':\'favB\');\n var allRow=document.getElementById(venue===\'M\'?\'catsM\':\'catsB\');\n var nfav=0;\n CHIPS[venue].forEach(function(ch){\n  var on=favs.indexOf(ch.key)>-1;\n  ch.star.setAttribute(\'aria-pressed\',on?\'true\':\'false\');\n  ch.star.textContent=on?\'★\':\'☆\';\n  ch.star.title=(on?\'Unfavourite \':\'Favourite \')+ch.cat;\n  (on?favRow:allRow).appendChild(ch.el);\n  if(on)nfav++;\n });\n favRow.className=\'row fav\'+(nfav?\' on\':\'\');\n}\nbuild(\'catsM\',orderM,selM,\'M\');\nbuild(\'catsB\',orderB,selB,\'B\');\nfunction sync(venue){\n var id=venue===\'M\'?\'catsM\':\'catsB\';\n var picked=[].slice.call(document.getElementById(id).querySelectorAll(\'input\')).filter(function(x){return x.checked}).map(function(x){return x.dataset.c});\n if(venue===\'M\'){selM=picked;s(LS.m,selM)}else{selB=picked;s(LS.t,selB)}\n draw();\n}\n[[av,LS.a],[hf,LS.f],[hw,LS.w]].forEach(function(p){p[0].addEventListener(\'change\',function(){s(p[1],p[0].checked);draw()})});\ndocument.getElementById(\'reset\').addEventListener(\'click\',function(){\n av.checked=false;hf.checked=false;hw.checked=false;\n s(LS.a,false);s(LS.f,false);s(LS.w,false);\n [].slice.call(document.querySelectorAll(\'#catsM input,#catsB input\')).forEach(function(x){x.checked=true});\n selB=orderB.slice();selM=orderM.slice();s(LS.t,selB);s(LS.m,selM);\n draw();\n});\nfunction dl(iso){var d=new Date(iso+\'T00:00:00\');return d.toLocaleDateString(\'en-GB\',{weekday:\'long\',day:\'numeric\',month:\'long\'})}\nfunction sd(iso){var d=new Date(iso+\'T00:00:00\');return d.toLocaleDateString(\'en-GB\',{weekday:\'short\',day:\'numeric\',month:\'short\'})}\n(function(){\n var mine=D.filter(function(r){return r[7]===\'booked\'});\n if(!mine.length)return;\n var h=\'<h2>Your booked classes (\'+mine.length+\')</h2><ul>\';\n mine.forEach(function(r){\n  h+=\'<li><span class="bt">\'+sd(r[0])+\', \'+r[2]+\'</span><span class="bl">\'+r[4]+\' · \'+r[6]+\'</span><span class="bn">\'+r[5]+\' · \'+r[3]+\' min</span></li>\';\n });\n var bx=document.getElementById(\'booked\');bx.innerHTML=h+\'</ul>\';bx.style.display=\'block\';\n})();\nfunction addRow(tb,r,cur){\n if(r[0]!==cur){var dr=tb.insertRow();var dc=dr.insertCell();dc.colSpan=6;dc.textContent=dl(r[0]);dr.className=\'day\'}\n var tr=tb.insertRow();\n tr.setAttribute(\'data-cat\',r[4]);tr.setAttribute(\'data-state\',r[7]);\n tr.setAttribute(\'data-avail\',r[7]===\'bookable\'?\'1\':\'0\');\n tr.setAttribute(\'data-wd\',r[9]);tr.setAttribute(\'data-mins\',r[1]);\n tr.insertCell().outerHTML=\'<td class="t">\'+r[2]+\'</td>\';\n tr.insertCell().outerHTML=\'<td class="mins mut">\'+r[3]+\'</td>\';\n tr.insertCell().outerHTML=\'<td><span class="pill" style="background:\'+PC[r[4]]+\'">\'+r[4]+\'</span></td>\';\n tr.insertCell().textContent=r[5];\n tr.insertCell().textContent=r[6];\n tr.insertCell().outerHTML=\'<td class="st" style="color:\'+SC[r[7]]+\'">\'+r[8]+\'</td>\';\n return r[0];\n}\nfunction draw(){\n var tb=document.getElementById(\'tb\');tb.innerHTML=\'\';\n var cur=\'\',shown=0,cnt={};\n D.forEach(function(r){\n  var sel=r[10]===\'M\'?selM:selB;\n  if(sel.indexOf(r[4])<0)return;\n  if(av.checked&&r[7]!==\'bookable\')return;\n  if(hf.checked&&r[7]===\'full\')return;\n  if(hw.checked&&r[9]<5&&r[1]>=480&&r[1]<=1045)return;\n  cnt[r[7]]=(cnt[r[7]]||0)+1;shown++;\n  cur=addRow(tb,r,cur);\n });\n document.getElementById(\'none\').style.display=shown?\'none\':\'block\';\n document.getElementById(\'shown\').textContent=shown+\' of \'+D.length+\' shown\';\n var lab=[[\'bookable\',\'Bookable\'],[\'full\',\'Full\'],[\'soon\',\'Not yet open\'],[\'booked\',\'Booked\'],[\'closed\',\'Closed\']];\n var lg=document.getElementById(\'lg\');lg.innerHTML=\'\';\n lab.forEach(function(p){\n  if(!cnt[p[0]])return;\n  var e=document.createElement(\'span\');\n  e.innerHTML=\'<i style="background:\'+SC[p[0]]+\'"></i>\'+p[1]+\' <b>\'+cnt[p[0]]+\'</b>\';\n  lg.appendChild(e);\n });\n}\ndraw();\n</script></body></html>\n'
#!/usr/bin/env python3
"""
refresh.py — scrape ClassPass and rebuild ~/Sites/jynk/blok/index.html.

Standalone: no Claude, no Cowork. Run it from launchd every 4 hours.
push-blok.sh (every 10 min) commits and pushes whatever this writes.

    pip install playwright && playwright install chromium
    python3 login_setup.py     # once, so BOOKED classes show up
    python3 refresh.py

Exit codes: 0 ok, 1 scrape/build failure (page left untouched).
"""
import json, re, sys, datetime, pathlib, argparse

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
AUTH = HERE / "auth_state.json"
OUT  = REPO / "index.html"

STUDIOS = [
    ("Clapton",    "blok-clapton-london",   "B"),
    ("Shoreditch", "blok-shoreditch-london","B"),
    ("Mission E1", "mission-e1-london",     "M"),
]
MAX_DAYS = 14

# BLOK publishes a huge timetable (Open Gym, Reformer Pilates, Barre...).
# Only these are wanted; everything else at a BLOK studio is skipped.
BLOK_RX = re.compile(r"CALISTHENICS|BLOKSTRENGTH|HANDSTAND|POWER YOGA|MOBILITY|YIN", re.I)

def blok_cat(name):
    u = name.upper()
    if "CALISTHENICS" in u: return "Calisthenics"
    if "BLOKSTRENGTH" in u and "UPPER" in u: return "Strength: Upper"
    if "BLOKSTRENGTH" in u and "LOWER" in u: return "Strength: Lower"
    if "BLOKSTRENGTH" in u and "FULL"  in u: return "Strength: Full Body"
    if "HANDSTAND" in u: return "Handstands"
    if "POWER YOGA" in u: return "Power"
    if "MOBILITY" in u: return "Mobility"
    if "YIN" in u: return "Yin"
    return None            # matched the filter but has no category -> hard error

MISSION_RULES = [
    (r"mobility|rolling|backbend|splits",              "Mobility & Rolling"),
    (r"statics|balance|handstand|rings",               "Kulture: Skills"),
    (r"reps kulture|skills & reps|squat kulture|kettlebell|kulture", "Kulture: Reps"),
    (r"boxing",                                        "Boxing"),
    (r"rocket",                                        "Rocket"),
    (r"ashtanga",                                      "Ashtanga"),
    (r"vinyasa",                                       "Vinyasa"),
    (r"dharma",                                        "Dharma"),
    (r"hot ",                                          "Hot Yoga"),
    (r"^yin|yin:",                                     "Yin Yoga"),
    (r"pilates",                                       "Pilates"),
    (r"core",                                          "Core"),
    (r"4beat",                                         "4BEAT"),
    (r"bambu",                                         "Bambu Bodies"),
    (r"yoga|asana|flow|philosophy|kundalini|meditation","Yoga: Other"),
]
def mission_cat(name):
    s = name.lower()
    for rx, cat in MISSION_RULES:
        if re.search(rx, s): return cat
    return "Other"         # never silently drop a Mission class

ORDER_B = ["Calisthenics","Strength: Upper","Strength: Lower","Strength: Full Body",
           "Handstands","Power","Mobility","Yin"]
ORDER_M = ["Kulture: Reps","Kulture: Skills","Mobility & Rolling","Boxing","4BEAT","Core",
           "Pilates","Bambu Bodies","Ashtanga","Vinyasa","Rocket","Dharma","Hot Yoga",
           "Yin Yoga","Yoga: Other","Other"]
PC = {"Calisthenics":"#7c5cff","Strength: Upper":"#2e9e5b","Strength: Lower":"#c77d0a",
      "Strength: Full Body":"#1f7fd1","Handstands":"#d6336c","Power":"#e8590c",
      "Mobility":"#0ca678","Yin":"#7048e8",
      "Kulture: Reps":"#b02a37","Kulture: Skills":"#d6336c","Mobility & Rolling":"#0ca678",
      "Ashtanga":"#1f7fd1","Vinyasa":"#3b8ee0","Rocket":"#8a4fd6","Dharma":"#6741d9",
      "Hot Yoga":"#e8590c","Yin Yoga":"#7048e8","Yoga: Other":"#5c7cfa","Pilates":"#2e9e5b",
      "Core":"#c77d0a","4BEAT":"#e64980","Bambu Bodies":"#12897a","Boxing":"#495057",
      "Other":"#8a8a8f"}
SC = {"bookable":"#1f8a3c","full":"#c0392b","soon":"#b06a00","booked":"#1f7fd1","closed":"#8a8a8f"}

DAY_RX  = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s(\w+)\s(\d+)$")
TIME_RX = re.compile(r"^(\d+):(\d+)\s*(AM|PM)$", re.I)
MONTHS  = {m: i+1 for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

def log(*a): print(*a, flush=True)

# ---------------------------------------------------------------- scraping
READ_DAY_JS = r"""
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < 60; i++) {
    const b = [...document.querySelectorAll('button')]
      .find(x => /see more/i.test(x.textContent));
    if (!b) break;
    b.click();
    await sleep(180);
  }
  const hdr = [...document.querySelectorAll('div,span,h2,h3')]
    .map(e => e.textContent.trim())
    .find(t => /^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s\w+\s\d+$/.test(t)) || '';
  const rows = [...document.querySelectorAll('.Schedule__rows section')].map(s => {
    const L = s.innerText.split('\n').map(x => x.trim()).filter(Boolean);
    const btn = s.querySelector('button[data-tooltip]') || s.querySelector('button');
    return {
      time: L[0] || '', dur: L[1] || '', name: L[2] || '', inst: L[3] || '',
      tip: btn ? (btn.getAttribute('data-tooltip') || '') : '',
      btn: btn ? btn.innerText.replace(/\s+/g, ' ').trim() : ''
    };
  });
  return { hdr, rows };
}
"""

def status(tip, btn):
    """Read the tooltip, not the label: 'Reserve' is shown for several states."""
    if re.search(r"reserved|cancel", btn, re.I):        return "booked", "You're booked"
    if re.search(r"no spots left", tip, re.I):          return "full", "Full — no spots left"
    if re.search(r"booking window opens on", tip, re.I):
        return "soon", "Books open " + re.sub(r".*opens on\s*", "", tip, flags=re.I).rstrip(".")
    if re.search(r"booking window is now closed", tip, re.I): return "closed", "Booking closed"
    m = re.fullmatch(r"(\d+)\s*credits?", btn.strip(), re.I)   # NOT startswith('C')
    if m: return "bookable", "Bookable (%s credits)" % m.group(1)
    return None, btn + " | " + tip

def scrape(page, url, studio, venue, year, warnings):
    page.goto(url, timeout=60000)
    page.wait_for_timeout(4000)
    rows, seen_days = [], []
    for day in range(MAX_DAYS):
        got = page.evaluate(READ_DAY_JS)
        hdr, raw = got["hdr"], got["rows"]
        m = DAY_RX.match(hdr)
        if not m:
            warnings.append("%s: no day header on day %d" % (studio, day + 1))
            break
        date = datetime.date(year, MONTHS[m.group(2)[:3]], int(m.group(3)))
        if not raw and day > 0:
            log("  %s: %s empty -> end of published schedule" % (studio, hdr))
            break
        kept = 0
        for r in raw:
            name = r["name"]
            if venue == "B":
                if not BLOK_RX.search(name): continue
                cat = blok_cat(name)
                if cat is None:
                    raise SystemExit("FATAL: %r matched the BLOK filter but has no category" % name)
            else:
                cat = mission_cat(name)
                if cat == "Other":
                    warnings.append("%s: uncategorised class %r" % (studio, name))
            tm = TIME_RX.match(r["time"])
            if not tm:
                warnings.append("%s: unparseable time %r" % (studio, r["time"]))
                continue
            mins = (int(tm.group(1)) % 12 + (12 if tm.group(3).upper() == "PM" else 0)) * 60 + int(tm.group(2))
            st, lab = status(r["tip"], r["btn"])
            if st is None:
                warnings.append("%s: unknown status %r for %r" % (studio, lab, name))
                continue
            dur = int(re.sub(r"\D", "", r["dur"]) or 0)
            rows.append([date.isoformat(), mins, fmt_time(mins), dur, cat,
                         r["inst"], studio, st, lab, date.weekday(), venue])
            kept += 1
        seen_days.append("%s:%d" % (hdr, kept))
        nxt = page.query_selector('button[aria-label="Next day"]')
        if not nxt: break
        nxt.click()
        page.wait_for_timeout(2600)
    log("  %s -> %d classes  [%s]" % (studio, len(rows), " ".join(seen_days)))
    return rows

def fmt_time(m):
    h, mm = divmod(m, 60)
    return "%d:%02d%s" % (h % 12 or 12, mm, "AM" if h < 12 else "PM")

# ---------------------------------------------------------------- build
def build(rows, template):
    rows.sort(key=lambda r: (r[0], r[1], r[6]))
    states, cats = {}, {}
    for r in rows:
        states[r[7]] = states.get(r[7], 0) + 1
        cats[r[4]] = cats.get(r[4], 0) + 1
    if sum(states.values()) != len(rows):
        raise SystemExit("FATAL: state counts do not sum to row count")
    order_b = [c for c in ORDER_B]
    order_m = [c for c in ORDER_M if cats.get(c)]      # hide empty Mission cats
    for c in order_b + order_m:
        cats.setdefault(c, 0)
        if c not in PC: raise SystemExit("FATAL: no colour for category %r" % c)
    j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    data = ("var D=%s,SC=%s,PC=%s,CATS=%s,orderB=%s,orderM=%s;" % (
        j(rows), j(SC), j(PC), j({c: cats[c] for c in order_b + order_m}),
        j(order_b), j(order_m)))
    now = datetime.datetime.now().astimezone()
    f = lambda iso: datetime.date.fromisoformat(iso).strftime("%-d %b")
    link = '<a href="https://classpass.com/studios/%s" target="_blank" rel="noopener">%s</a>'
    sub = ("<p>" + " &amp; ".join(link % (slug, name) for name, slug, _ in STUDIOS) +
           " · %s – %s %s · %d classes · auto-updated every 4 hours · refreshed %s</p>") % (
          f(rows[0][0]), f(rows[-1][0]), rows[-1][0][:4], len(rows),
          now.strftime("%a %-d %b %Y, %H:%M %Z"))
    html = template.replace("@@DATA@@", data).replace("@@SUB@@", sub)
    if "@@" in html: raise SystemExit("FATAL: unreplaced template token")
    return html, states, cats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright
    year = datetime.date.today().year
    rows, warnings = [], []
    log("BLOK refresh %s" % datetime.datetime.now().strftime("%F %T"))
    if not AUTH.exists():
        log("  ! no auth_state.json - your booked classes will not be marked."
            " Run login_setup.py once.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        ctx = browser.new_context(storage_state=str(AUTH) if AUTH.exists() else None)
        page = ctx.new_page()
        for name, slug, venue in STUDIOS:
            try:
                rows += scrape(page, "https://classpass.com/studios/" + slug, name, venue, year, warnings)
            except SystemExit:
                raise
            except Exception as e:
                warnings.append("%s: scrape failed: %s" % (name, e))
                log("  ! %s failed: %s" % (name, e))
        browser.close()
    if not rows:
        log("FATAL: no rows scraped - leaving %s untouched" % args.out)
        return 1
    html, states, cats = build(rows, TEMPLATE)
    pathlib.Path(args.out).write_text(html, encoding="utf-8")
    log("  wrote %s (%d bytes)" % (args.out, len(html.encode())))
    log("  %d classes  states=%s" % (len(rows), states))
    log("  categories: %s" % {k: v for k, v in sorted(cats.items()) if v})
    for w in warnings: log("  ! " + w)
    return 0

if __name__ == "__main__":
    sys.exit(main())
