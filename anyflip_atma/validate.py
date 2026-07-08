# -*- coding: utf-8 -*-
import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")
CSVF = r"D:\AndroidStudioProjects\vocab1000app\anyflip_atma\vocab_m1-3.csv"
rows = list(csv.DictReader(open(CSVF, encoding="utf-8-sig")))
print("total rows:", len(rows))

def has_latin(s): return bool(re.search(r"[A-Za-z]", s))
flags = {"empty_pron":[], "empty_meaning":[], "latin_in_pron":[], "bleed_meaning":[],
         "long_pron":[], "no_thai_pron":[]}
BAD = ("Item","Vocabulary","GRADE","SUPERVISION","Phrae","Speech")
for r in rows:
    key = f'{r["level"]}/{r["item"]} {r["word"]}'
    p, m = r["pronunciation"], r["meaning"]
    if not p.strip(): flags["empty_pron"].append(key)
    if not m.strip(): flags["empty_meaning"].append(key)
    if has_latin(p): flags["latin_in_pron"].append(key+" :: "+p)
    if any(b in m for b in BAD): flags["bleed_meaning"].append(key+" :: "+m)
    if len(p.replace(" ","")) > 22: flags["long_pron"].append(key+" :: "+p)
    if not re.search(r"[฀-๿]", p): flags["no_thai_pron"].append(key+" :: "+p)
for k,v in flags.items():
    print(f"\n## {k}: {len(v)}")
    for x in v[:25]: print("   ", x)

print("\n===== wrapped-meaning entries (sanity) =====")
want = {("1","385"),("2","385"),("2","629"),("2","935"),("1","947"),("3","632")}
for r in rows:
    if (r["level"],r["item"]) in want:
        print(r["level"],r["item"],"|",r["word"],"|",r["part_of_speech"],"|",r["pronunciation"],"|",r["meaning"])
