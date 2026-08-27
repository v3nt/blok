TEMPLATE = '<!doctype html><html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Class schedule — BLOK &amp; Mission E1</title><style>\n:root{--bd:#e3e3e8}\n*{box-sizing:border-box}\nbody{margin:0;font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:#16161a;background:#fafafb}\nheader{background:#16161a;color:#fff;padding:14px 18px}\nheader h1{margin:0;font-size:19px;font-weight:700}\nheader p{margin:5px 0 0;font-size:13px;color:#a9a9b4}\nheader a{color:#c8c8d4}\n#lg{margin:7px 0 0;display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px}\n#lg span{display:inline-flex;align-items:center;gap:5px;color:#e6e6ea}\n#lg i{width:8px;height:8px;border-radius:50%;display:inline-block}\n#lg b{font-weight:700}\n.bar{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--bd);padding:10px 18px;font-size:13.5px}\n.bar .top{display:flex;flex-wrap:wrap;gap:9px 18px;align-items:center}\n.bar label{display:inline-flex;gap:6px;align-items:center;cursor:pointer;white-space:nowrap}\n.bar .sep{width:1px;height:18px;background:var(--bd)}\n.bar .n{color:#87878f;font-size:12px}\n#shown{color:#55555f;font-size:12.5px;font-variant-numeric:tabular-nums}\n.grp{margin-top:9px;padding-top:8px;border-top:1px dashed var(--bd)}\n.col{border:0;background:none;font:inherit;font-size:11.5px;color:#4a4a55;cursor:pointer;padding:0 8px 0 0;white-space:nowrap}\n.col:hover{color:#16161a}\n.row.collapsed .chip{display:none}\n.all{display:inline-flex;gap:4px;align-items:center;cursor:pointer;font-size:11.5px;color:#6b6b76;border-right:1px solid var(--bd);padding-right:10px;margin-right:2px;white-space:nowrap}\n.grp h3{margin:0 0 6px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#6b6b76}\n.grp .row{display:flex;flex-wrap:wrap;gap:7px 14px}\n.grp .row.fav{display:none;padding:5px 8px 6px;margin-bottom:6px;background:#fffaeb;border:1px solid #f0dfa8;border-radius:8px}\n.grp .row.fav.on{display:flex}\n.grp .row.fav::before{content:"★";color:#e8a90c;font-size:12px;align-self:center;margin-right:2px}\n.chip{display:inline-flex;gap:6px;align-items:center;white-space:nowrap}\n.dot{width:9px;height:9px;border-radius:50%;display:inline-block}\n.star{border:0;background:none;cursor:pointer;font-size:14px;line-height:1;padding:0 2px;color:#c9c9d1}\n.star[aria-pressed="true"]{color:#e8a90c}\n#reset{border:1px solid var(--bd);background:#f4f4f6;border-radius:7px;padding:5px 11px;font:inherit;font-size:12.5px;cursor:pointer}\n#reset:hover{background:#eaeaee}\n#booked{background:#eaf3fc;border-bottom:1px solid #cfe0f2;padding:11px 18px;font-size:13px;display:none}\n#booked h2{margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#1f7fd1}\n#booked ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:4px}\n#booked li{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}\n#booked .bt{font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}\n#booked .bl{color:#55555f}\n#booked .bn{color:#87878f;font-size:12px}\ntable{width:100%;border-collapse:collapse;background:transparent}\nth{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:#6b6b76;padding:9px 10px;border-bottom:1px solid var(--bd)}\ntd a{color:#1f5fbf}\ntd{padding:8px 10px;border-bottom:1px solid #f0f0f3;font-size:13.5px;vertical-align:middle}\ntr.day td{background:#eeeef1;font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#44444c;padding:7px 10px}\ntbody tr[data-state="full"] td:not(:last-child){opacity:.55}\n.pill.hasd{cursor:help}\n.pill{display:inline-block;padding:2px 8px;border-radius:99px;color:#fff;font-size:11.5px;font-weight:600;white-space:nowrap}\n.t{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600}\n.st{font-weight:600;white-space:nowrap}\n.mut{color:#6b6b76}\n.empty{padding:26px;text-align:center;color:#6b6b76}\n#main{background:#fff}\n@media(max-width:640px){td,th{padding:7px 6px;font-size:12.5px}.mins{display:none}.bar,header,#booked{padding-left:11px;padding-right:11px}}\n</style></head><body>\n<header><h1>Class schedule — BLOK &amp; Mission E1</h1>\n@@SUB@@\n<div id="lg"></div></header>\n<div class="bar">\n<div class="top">\n<label><input type="checkbox" id="av"> Bookable now only</label>\n<label><input type="checkbox" id="hf"> Hide full</label>\n<label><input type="checkbox" id="hw"> Hide weekday 8:00am–5:25pm</label>\n<span class="sep"></span><button id="reset">Reset filters</button>\n<span id="shown"></span>\n</div>\n<div class="grp"><h3>Mission E1</h3><div class="row fav" id="favM"><label class="all"><input type="checkbox" id="allFavM" checked> all</label></div><div class="row" id="catsM"><button type="button" class="col" id="colM" aria-expanded="true"></button><label class="all"><input type="checkbox" id="allCatM" checked> all</label></div></div>\n<div class="grp"><h3>BLOK — Clapton &amp; Shoreditch</h3><div class="row fav" id="favB"><label class="all"><input type="checkbox" id="allFavB" checked> all</label></div><div class="row" id="catsB"><button type="button" class="col" id="colB" aria-expanded="true"></button><label class="all"><input type="checkbox" id="allCatB" checked> all</label></div></div>\n</div>\n<div id="booked"></div>\n<div id="main"><table><thead><tr><th>Time</th><th class="mins">Min</th><th>Class</th><th>Instructor</th><th>Studio</th><th>Booking status</th></tr></thead><tbody id="tb"></tbody></table></div>\n<div class="empty" id="none" style="display:none">No classes match these filters.</div>\n<script>\n@@DATA@@\nvar LS={a:\'blokAvailOnly\',f:\'blokHideFull\',w:\'blokHideWorkHours\',t:\'blokTypes\',m:\'blokTypesM\',v:\'blokFavs\',vv:\'blokFavsSeed\',c:\'blokCollapse\'};\nfunction g(k,d){try{var v=localStorage.getItem(k);return v===null?d:JSON.parse(v)}catch(e){return d}}\nfunction s(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}\nfunction clean(saved,valid){\n if(!Array.isArray(saved))return valid.slice();\n var out=saved.filter(function(c){return valid.indexOf(c)>-1});\n return out.length?out:valid.slice();\n}\nvar selB=clean(g(LS.t,null),orderB), selM=clean(g(LS.m,null),orderM);\n// First visit: start with the calisthenics / strength classes favourited.\n// Once the user has touched a star their saved list wins, including an\n// empty one - DEFAULT_FAVS must not creep back in after they clear it.\nvar favs=g(LS.v,null);\nif(!Array.isArray(favs))favs=DEFAULT_FAVS.slice();\n// A browser that saved favourites under an older build would otherwise never\n// see new defaults - its saved list wins forever, and the star rows look\n// empty. Stamp the defaults; when they change, merge them in ONCE, keeping\n// everything the user starred themselves.\nif(g(LS.vv,\'\')!==DEFAULT_FAVS.join(\'~\')){\n DEFAULT_FAVS.forEach(function(k){if(favs.indexOf(k)<0)favs.push(k)});\n s(LS.v,favs);s(LS.vv,DEFAULT_FAVS.join(\'~\'));\n}\nfavs=favs.filter(function(k){var p=k.split(\'|\');return (p[0]===\'B\'&&orderB.indexOf(p[1])>-1)||(p[0]===\'M\'&&orderM.indexOf(p[1])>-1)});\nvar av=document.getElementById(\'av\'),hf=document.getElementById(\'hf\'),hw=document.getElementById(\'hw\');\nav.checked=!!g(LS.a,false);hf.checked=!!g(LS.f,false);hw.checked=!!g(LS.w,false);\nvar ROWS=[[\'allFavM\',\'favM\',\'M\'],[\'allCatM\',\'catsM\',\'M\'],[\'allFavB\',\'favB\',\'B\'],[\'allCatB\',\'catsB\',\'B\']];\nfunction boxesIn(rowId){return [].slice.call(document.getElementById(rowId).querySelectorAll(\'input[data-c]\'))}\nfunction boxes(venue){return ROWS.filter(function(r){return r[2]===venue})\n .reduce(function(a,r){return a.concat(boxesIn(r[1]))},[])}\nROWS.forEach(function(r){\n var master=document.getElementById(r[0]);\n master.addEventListener(\'change\',function(){\n  boxesIn(r[1]).forEach(function(x){x.checked=master.checked});\n  sync(r[2]);\n });\n});\nfunction refreshAll(){\n ROWS.forEach(function(r){\n  var bs=boxesIn(r[1]),m=document.getElementById(r[0]),n=bs.filter(function(x){return x.checked}).length;\n  m.checked=bs.length>0&&n===bs.length;\n  m.indeterminate=n>0&&n<bs.length;\n  m.disabled=bs.length===0;\n });\n}\n// The non-favourites list is long (35 and 46 types). Collapse it per gym and\n// remember the choice. Collapsing only hides the chips - it never changes\n// which categories are selected, so the table below is untouched.\nvar COL=g(LS.c,null); if(!COL||typeof COL!==\'object\')COL={M:false,B:false};\nfunction paintCol(venue){\n var row=document.getElementById(venue===\'M\'?\'catsM\':\'catsB\');\n var btn=document.getElementById(venue===\'M\'?\'colM\':\'colB\');\n var n=row.querySelectorAll(\'.chip\').length, off=!!COL[venue];\n row.className=\'row\'+(off?\' collapsed\':\'\');\n btn.setAttribute(\'aria-expanded\',off?\'false\':\'true\');\n btn.textContent=(off?\'▸ \':\'▾ \')+n+\' more\';\n btn.title=(off?\'Show\':\'Hide\')+\' the non-favourite filters\';\n}\n[\'M\',\'B\'].forEach(function(v){\n document.getElementById(v===\'M\'?\'colM\':\'colB\').addEventListener(\'click\',function(){\n  COL[v]=!COL[v]; s(LS.c,COL); paintCol(v);\n });\n});\nvar CHIPS={M:[],B:[]};\nfunction build(wrapId,order,sel,venue){\n order.forEach(function(c){\n  var l=document.createElement(\'label\');l.className=\'chip\';\n  var i=document.createElement(\'input\');i.type=\'checkbox\';i.checked=sel.indexOf(c)>-1;i.dataset.c=c;\n  i.addEventListener(\'change\',function(){sync(venue)});\n  var d=document.createElement(\'span\');d.className=\'dot\';d.style.background=PC[c];\n  var t=document.createElement(\'span\');t.textContent=c;\n  var n=document.createElement(\'span\');n.className=\'n\';n.textContent=CATS[c]||0;\n  l.appendChild(i);l.appendChild(d);l.appendChild(t);l.appendChild(n);\n  var b=document.createElement(\'button\');b.className=\'star\';b.type=\'button\';\n  var key=venue+\'|\'+c,on=favs.indexOf(key)>-1;\n  b.setAttribute(\'aria-pressed\',on?\'true\':\'false\');\n  b.textContent=on?\'★\':\'☆\';\n  b.title=(on?\'Unfavourite \':\'Favourite \')+c;\n  b.addEventListener(\'click\',function(){\n   var j=favs.indexOf(key);\n   if(j>-1)favs.splice(j,1);else favs.push(key);\n   s(LS.v,favs);\n   place(venue);\n  });\n  var chip=document.createElement(\'span\');chip.className=\'chip\';\n  chip.appendChild(l);chip.appendChild(b);\n  CHIPS[venue].push({cat:c,key:key,el:chip,star:b});\n });\n place(venue);\n}\nfunction place(venue){\n var favRow=document.getElementById(venue===\'M\'?\'favM\':\'favB\');\n var allRow=document.getElementById(venue===\'M\'?\'catsM\':\'catsB\');\n var nfav=0;\n CHIPS[venue].forEach(function(ch){\n  var on=favs.indexOf(ch.key)>-1;\n  ch.star.setAttribute(\'aria-pressed\',on?\'true\':\'false\');\n  ch.star.textContent=on?\'★\':\'☆\';\n  ch.star.title=(on?\'Unfavourite \':\'Favourite \')+ch.cat;\n  (on?favRow:allRow).appendChild(ch.el);   // master \'all\' label stays first, it is never moved\n  if(on)nfav++;\n });\n favRow.className=\'row fav\'+(nfav?\' on\':\'\');\n paintCol(venue);\n refreshAll();\n}\nbuild(\'catsM\',orderM,selM,\'M\');\nbuild(\'catsB\',orderB,selB,\'B\');\nfunction sync(venue){\n // must read BOTH rows: a favourited chip lives in the fav row, and reading\n // only the main row silently deselects every favourite.\n var picked=boxes(venue).filter(function(x){return x.checked}).map(function(x){return x.dataset.c});\n if(venue===\'M\'){selM=picked;s(LS.m,selM)}else{selB=picked;s(LS.t,selB)}\n refreshAll();\n draw();\n}\n[[av,LS.a],[hf,LS.f],[hw,LS.w]].forEach(function(p){p[0].addEventListener(\'change\',function(){s(p[1],p[0].checked);draw()})});\ndocument.getElementById(\'reset\').addEventListener(\'click\',function(){\n av.checked=false;hf.checked=false;hw.checked=false;\n s(LS.a,false);s(LS.f,false);s(LS.w,false);\n // Reset also restores the default favourites. Without this there is no way\n // back to them once a saved list exists - which reads as "the defaults are\n // missing" on any browser that used an older build.\n favs=DEFAULT_FAVS.slice();s(LS.v,favs);\n place(\'M\');place(\'B\');\n [].slice.call(document.querySelectorAll(\'#catsM input,#catsB input\')).forEach(function(x){x.checked=true});\n selB=orderB.slice();selM=orderM.slice();s(LS.t,selB);s(LS.m,selM);\n refreshAll();\n draw();\n});\nfunction dl(iso){var d=new Date(iso+\'T00:00:00\');return d.toLocaleDateString(\'en-GB\',{weekday:\'long\',day:\'numeric\',month:\'long\'})}\nfunction sd(iso){var d=new Date(iso+\'T00:00:00\');return d.toLocaleDateString(\'en-GB\',{weekday:\'short\',day:\'numeric\',month:\'short\'})}\n(function(){\n // Only classes still to come. A booked class stays flagged in the table as\n // history, but "Your booked classes" is a what\'s-next panel - listing last\n // week\'s sessions in it is noise.\n var now=new Date(), pad=function(n){return (n<10?\'0\':\'\')+n};\n var todayISO=now.getFullYear()+\'-\'+pad(now.getMonth()+1)+\'-\'+pad(now.getDate());\n var nowMins=now.getHours()*60+now.getMinutes();\n var mine=D.filter(function(r){\n  if(r[7]!==\'booked\')return false;\n  if(r[0]>todayISO)return true;\n  return r[0]===todayISO&&r[1]>=nowMins;      // today\'s, not yet started\n });\n if(!mine.length)return;\n var h=\'<h2>Your booked classes (\'+mine.length+\')</h2><ul>\';\n mine.forEach(function(r){\n  h+=\'<li><span class="bt">\'+sd(r[0])+\', \'+r[2]+\'</span><span class="bl">\'+r[4]+\' · \'+r[6]+\'</span><span class="bn">\'+r[5]+\' · \'+r[3]+\' min</span></li>\';\n });\n var bx=document.getElementById(\'booked\');bx.innerHTML=h+\'</ul>\';bx.style.display=\'block\';\n})();\nfunction addRow(tb,r,cur){\n if(r[0]!==cur){var dr=tb.insertRow();var dc=dr.insertCell();dc.colSpan=6;dc.textContent=dl(r[0]);dr.className=\'day\'}\n var tr=tb.insertRow();\n tr.setAttribute(\'data-cat\',r[4]);tr.setAttribute(\'data-state\',r[7]);\n tr.setAttribute(\'data-avail\',r[7]===\'bookable\'?\'1\':\'0\');\n tr.setAttribute(\'data-wd\',r[9]);tr.setAttribute(\'data-mins\',r[1]);\n tr.insertCell().outerHTML=\'<td class="t">\'+r[2]+\'</td>\';\n tr.insertCell().outerHTML=\'<td class="mins mut">\'+r[3]+\'</td>\';\n var d=DESC[r[4]]||\'\';\n tr.insertCell().outerHTML=\'<td><span class="pill\'+(d?\' hasd\':\'\')+\'" style="background:\'+PC[r[4]]+\'"\'\n  +(d?\' title="\'+d.split(\'"\').join(\'&quot;\')+\'"\':\'\')+\'>\'+r[4]+\'</span></td>\';\n tr.insertCell().textContent=r[5];\n var su=STUDIO_URL[r[6]];\n tr.insertCell().outerHTML=su?(\'<td><a href="\'+su+\'" target="_blank" rel="noopener">\'+r[6]+\'</a></td>\'):(\'<td>\'+r[6]+\'</td>\');\n tr.insertCell().outerHTML=\'<td class="st" style="color:\'+SC[r[7]]+\'">\'+r[8]+\'</td>\';\n return r[0];\n}\nfunction draw(){\n var tb=document.getElementById(\'tb\');tb.innerHTML=\'\';\n var cur=\'\',shown=0,cnt={};\n D.forEach(function(r){\n  var sel=r[10]===\'M\'?selM:selB;\n  if(sel.indexOf(r[4])<0)return;\n  if(av.checked&&r[7]!==\'bookable\')return;\n  if(hf.checked&&r[7]===\'full\')return;\n  if(hw.checked&&r[9]<5&&r[1]>=480&&r[1]<=1045)return;\n  cnt[r[7]]=(cnt[r[7]]||0)+1;shown++;\n  cur=addRow(tb,r,cur);\n });\n document.getElementById(\'none\').style.display=shown?\'none\':\'block\';\n document.getElementById(\'shown\').textContent=shown+\' of \'+D.length+\' shown\';\n var lab=[[\'bookable\',\'Bookable\'],[\'full\',\'Full\'],[\'soon\',\'Not yet open\'],[\'booked\',\'Booked\'],[\'closed\',\'Closed\']];\n var lg=document.getElementById(\'lg\');lg.innerHTML=\'\';\n lab.forEach(function(p){\n  if(!cnt[p[0]])return;\n  var e=document.createElement(\'span\');\n  e.innerHTML=\'<i style="background:\'+SC[p[0]]+\'"></i>\'+p[1]+\' <b>\'+cnt[p[0]]+\'</b>\';\n  lg.appendChild(e);\n });\n}\nrefreshAll();\ndraw();\n</script></body></html>\n'
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

# Every class type at every studio is kept. The category is the class name
# with the duration stripped, so CALISTHENICS 50 and CALISTHENICS 60 are one
# filter. Mission E1 additionally folds obvious variants together.
def strip_dur(name):
    return re.sub(r"\s+\d{2,3}$", "", name).strip()

def collapse(cat):
    c = cat
    c = re.sub(r":\s*(All Levels|Beginners?|Foundation|Intermediate|Experienced|Advanced|First Timers)\s*$", "", c, flags=re.I)
    c = re.sub(r"\s+for First Timers$", "", c, flags=re.I)
    c = re.sub(r"\s+(I{1,3})$", "", c)                  # Rocket I / II / III
    c = re.sub(r"\s+for Beginners$", "", c, flags=re.I)
    c = re.sub(r":\s*Shapes & Sequences$", "", c, flags=re.I)
    c = re.sub(r"^Mobility Kulture.*$", "Mobility Kulture", c)
    c = re.sub(r"^Hot Yoga (One|Two|Three)$", "Hot Yoga", c)
    c = re.sub(r"^Iyengar Yoga.*$", "Iyengar Yoga", c)
    c = re.sub(r"^4BEAT.*$", "4BEAT", c)
    c = re.sub(r"^Ashtanga Yoga Guided Self Practice$", "Ashtanga Guided Self Practice", c)
    return c.strip()

def categorise(name, venue):
    c = strip_dur(name)
    return c if venue == "B" else collapse(c)

# Colours: the classes worth spotting keep a hue, everything else is grey so
# the schedule does not turn into a rainbow.
CORE = {"CALISTHENICS":"#7c5cff","BLOKSTRENGTH: UPPER BODY":"#2e9e5b",
        "BLOKSTRENGTH: LOWER BODY":"#c77d0a","BLOKSTRENGTH: FULL BODY":"#1f7fd1",
        "HANDSTANDS":"#d6336c","POWER YOGA":"#e8590c","BLOKMOBILITY":"#0ca678",
        "YIN YOGA":"#7048e8","YIN YANG FLOW":"#7048e8"}
MISSION_CORE = {"Reps Kulture":"#b02a37","Skills & Reps Kulture":"#b02a37",
        "Skills Kulture":"#d6336c","Statics Kulture":"#d6336c","Squat Kulture":"#c77d0a",
        "Handstands":"#d6336c","Rocket":"#8a4fd6","Dharma":"#6741d9","Vinyasa Flow":"#3b8ee0",
        "Ashtanga":"#1f7fd1","Pilates":"#2e9e5b","Yin":"#7048e8","Boxing":"#495057",
        "4BEAT":"#e64980","Bambu Bodies":"#12897a","Kettlebells":"#b02a37"}
GREY = "#8a8a8f"

# Favourited out of the box on a first visit: the calisthenics and strength
# classes. Mission E1's "Kulture" family is its calisthenics/strength stream.
DEFAULT_FAVS = {
    "CALISTHENICS", "BLOKSTRENGTH: UPPER BODY", "BLOKSTRENGTH: LOWER BODY",
    "BLOKSTRENGTH: FULL BODY", "HANDSTANDS",
    "Reps Kulture", "Total Reps Kulture", "Skills & Reps Kulture", "Skills Kulture",
    "Squat Kulture", "Statics Kulture", "Strength Kulture", "Balance Kulture",
    "Kettlebells", "Rings", "Handstands",
}
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
            cat = categorise(name, venue)
            if not cat:
                warnings.append("%s: unnamed class on %s" % (studio, hdr))
                continue
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
UPCOMING_URL = "https://classpass.com/profile/upcoming"

UPCOMING_JS = r"""
() => {
  const L = document.body.innerText.split('\n').map(s => s.trim()).filter(Boolean);
  const out = [];
  for (let i = 0; i < L.length; i++) {
    const m = L[i].match(/^([A-Z][a-z]{2}) (\d{1,2}), (\d{1,2}):(\d{2}) (AM|PM)$/);
    if (!m) continue;
    out.push({when: L[i], cls: L[i + 1] || '', inst: L[i + 2] || '',
              studio: L[i + 3] || ''});
  }
  return out;
}
"""

def upcoming(page, year, warnings):
    """Read the reservations off /profile/upcoming.

    The schedule rows only say "Cancel" on a class you booked, and only while
    logged in - which silently produced a page with no bookings marked. The
    profile page is the authoritative list, so bookings are matched from here
    instead of inferred per row.

    Returns {(iso, minutes, studio)} - empty if logged out, which is a warning,
    never a crash.
    """
    try:
        page.goto(UPCOMING_URL, timeout=60000)
        page.wait_for_timeout(4000)
        entries = page.evaluate(UPCOMING_JS)
    except Exception as e:
        warnings.append("could not read upcoming reservations: %s" % e)
        return set()
    if not entries:
        warnings.append("no upcoming reservations found - logged out? "
                        "run login_setup.py to refresh auth_state.json")
        return set()
    booked = set()
    for e in entries:
        m = re.match(r"^([A-Z][a-z]{2}) (\d{1,2}), (\d{1,2}):(\d{2}) (AM|PM)$", e["when"])
        if not m:
            warnings.append("unparsed reservation date %r" % e["when"])
            continue
        mon, day, hh, mm, ap = m.groups()
        date = datetime.date(year, MONTHS[mon], int(day))
        mins = (int(hh) % 12 + (12 if ap == "PM" else 0)) * 60 + int(mm)
        # "BLOK - Clapton" -> "Clapton"; "Mission E1" stays as it is
        studio = e["studio"].split(" - ")[-1].strip()
        booked.add((date.isoformat(), mins, studio))
    log("  upcoming reservations: %d" % len(booked))
    return booked

def mark_booked(rows, booked, warnings, today=None):
    """Stamp booked state from the reservations list, matched on date+time+studio.

    /profile/upcoming is authoritative for anything still to come: a future row
    flagged booked that is NOT in the list is a class since cancelled, so the
    flag is cleared. Past rows keep whatever was true at scrape time - they are
    history, and they never appear in "upcoming".
    """
    today = today or datetime.date.today().isoformat()
    hit = cleared = 0
    for r in rows:
        key = (r[0], r[1], r[6])
        if key in booked:
            r[7], r[8] = "booked", "You're booked"
            hit += 1
        elif r[7] == "booked" and r[0] >= today:
            r[7], r[8] = "bookable", "Bookable"
            cleared += 1
    if cleared:
        warnings.append("%d future row(s) were marked booked but are not in "
                        "upcoming - treated as cancelled" % cleared)
    missed = len(booked) - hit
    if missed > 0:
        warnings.append("%d reservation(s) had no matching class in the schedule" % missed)
    return hit

DESC_FILE = HERE / "class-descriptions.json"

def descriptions(categories):
    """Map each category to a class blurb, for the hover tooltip.

    class-descriptions.json is keyed by the full ClassPass name ("Rocket I:
    All Levels"); categories are the collapsed form ("Rocket"). Match by
    collapsing the keys the same way, preferring the longest blurb when
    several variants map to one category. Produced by class-descriptions.py,
    which is run by hand - a missing file just means no tooltips.
    """
    try:
        raw = json.loads(DESC_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    best = {}
    for group in raw.values():
        for name, entry in group.items():
            text = (entry or {}).get("description") or ""
            if not text:
                continue
            for cat in (categorise(name, "B"), categorise(name, "M")):
                if len(text) > len(best.get(cat, "")):
                    best[cat] = text
    return {c: best[c] for c in categories if c in best}

def build(rows, template):
    rows.sort(key=lambda r: (r[0], r[1], r[6]))
    states, cats = {}, {}
    for r in rows:
        states[r[7]] = states.get(r[7], 0) + 1
        cats[r[4]] = cats.get(r[4], 0) + 1
    if sum(states.values()) != len(rows):
        raise SystemExit("FATAL: state counts do not sum to row count")
    def order_for(v):
        seen = {r[4] for r in rows if r[10] == v}
        return sorted(seen, key=lambda c: (-cats[c], c))     # busiest type first
    order_b, order_m = order_for("B"), order_for("M")
    clash = set(order_b) & set(order_m)
    if clash:
        raise SystemExit("FATAL: category name used by both venues: %s" % sorted(clash))
    pc = {}
    for c in order_b: pc[c] = CORE.get(c, GREY)
    for c in order_m: pc[c] = MISSION_CORE.get(c, GREY)
    favs = [v + "|" + c for v, order in (("B", order_b), ("M", order_m))
            for c in order if c in DEFAULT_FAVS]
    desc = descriptions(order_b + order_m)
    j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    studio_url = {name: "https://classpass.com/studios/" + slug for name, slug, _ in STUDIOS}
    data = ("var D=%s,SC=%s,PC=%s,CATS=%s,orderB=%s,orderM=%s,DEFAULT_FAVS=%s,DESC=%s,STUDIO_URL=%s;" % (
        j(rows), j(SC), j(pc), j({c: cats[c] for c in order_b + order_m}),
        j(order_b), j(order_m), j(favs), j(desc), j(studio_url)))
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
        booked = upcoming(page, year, warnings)
        browser.close()
    if booked:
        log("  marked %d row(s) as booked" % mark_booked(rows, booked, warnings))
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
