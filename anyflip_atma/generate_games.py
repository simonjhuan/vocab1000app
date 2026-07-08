# -*- coding: utf-8 -*-
import csv, json, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"D:\AndroidStudioProjects\vocab1000app"
TEMPLATE = os.path.join(BASE, "www", "mton", "index.html")
GRADE_DIR = os.path.join(BASE, "vocab_by_grade")

tpl = open(TEMPLATE, encoding="utf-8").read()

# literal fragments to rebrand (must each appear exactly once)
T_TITLE = "<title>ศัพท์อังกฤษ ม.ต้น 1000 คำ</title>"
T_LOGO  = '<div class="logo">✦ ภาษาอังกฤษ ม.ต้น ✦</div>'
T_H1    = "<h1>คำศัพท์ ม.ต้น</h1>"
T_SUB   = '<p class="subtitle">1,000 คำ • วันละ 30 คำ • พร้อมคำอ่าน • บันทึกคะแนนอัตโนมัติ</p>'
T_STORE = "const STORE_KEY = 'mton_v1';"
T_CAP   = '<script src="../capacitor.js"></script>'
ARRAY_RE = re.compile(r"const allWords = \[[\s\S]*?\n\];")

def cap(w):
    return w[:1].upper() + w[1:] if w else w

def build(level):
    rows = list(csv.DictReader(open(os.path.join(GRADE_DIR, f"M{level}", f"vocab_M{level}.csv"), encoding="utf-8-sig")))
    words = [{"word": cap(r["word"]), "phon": r["pronunciation"], "meaning": r["meaning"]} for r in rows]
    arr = "const allWords = " + json.dumps(words, ensure_ascii=False, indent=2) + ";"
    n = len(words)

    html = tpl
    def rep(s, old, new):
        assert s.count(old) == 1, f"fragment not found exactly once: {old[:40]!r}"
        return s.replace(old, new)

    html = ARRAY_RE.sub(lambda m: arr, html, count=1)  # function repl = literal
    html = rep(html, T_TITLE, f"<title>ศัพท์อังกฤษ ม.{level} ({n:,} คำ)</title>")
    html = rep(html, T_LOGO,  f'<div class="logo">✦ ภาษาอังกฤษ ม.{level} ✦</div>')
    html = rep(html, T_H1,    f"<h1>คำศัพท์ ม.{level}</h1>")
    html = rep(html, T_SUB,   f'<p class="subtitle">{n:,} คำ • วันละ 30 คำ • พร้อมคำอ่าน • บันทึกคะแนนอัตโนมัติ</p>')
    html = rep(html, T_STORE, f"const STORE_KEY = 'mton_m{level}_v1';")
    html = rep(html, T_CAP,   '<script src="capacitor.js"></script>')

    out = os.path.join(GRADE_DIR, f"M{level}", "index.html")
    open(out, "w", encoding="utf-8").write(html)
    # quick sanity: count word objects actually in output
    got = html.count('"word":')
    print(f"M{level}: words={n} (in-html word-keys={got})  size={len(html)//1024}KB -> {out}")

for lv in ("1", "2", "3"):
    build(lv)
print("done")
