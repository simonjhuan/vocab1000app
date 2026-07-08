# -*- coding: utf-8 -*-
import re, csv, sys
sys.stdout.reconfigure(encoding="utf-8")

RAW = r"D:\AndroidStudioProjects\vocab1000app\anyflip_atma\pdf_all_raw.txt"
TBL = r"D:\AndroidStudioProjects\vocab1000app\anyflip_atma\pdf_all_table.txt"
OUT = r"D:\AndroidStudioProjects\vocab1000app\anyflip_atma\vocab_m1-3.csv"

POS = r"(n|v|adj|adv|prep|conj|pron|interj)"
ENTRY = re.compile(r"^\s*(\d+)\s+(.+?)\s+" + POS + r"\.?\s+(.+)$")
NEW_ITEM = re.compile(r"^\s*\d+\s+[A-Za-z]")
HEADER_BITS = ("BASIC ENGLISH VOCABULARY", "SUPERVISION MORNITORING",
               "Phrae Primary Educational", "Item Vocabulary",
               "ระดับชั้นมัธยมศึกษาปีที่")

def is_header(s):
    return any(b in s for b in HEADER_BITS)

END_MARKERS = ("คณะผู้จัดทำ", "คณะที่ปรึกษา", "คณะบรรณาธิการ", "ผู้จัดพิมพ์")
def is_end(s):
    return any(b in s for b in END_MARKERS)

def build_entries(path):
    """Merge wrapped lines; track level by item reset. Yields (level,item,word,pos,tail)."""
    # First, group physical lines into logical entries
    groups, cur = [], None
    appended = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if is_end(s) and cur is not None:   # back-matter after last word -> stop
                break
            if not s or is_header(s):
                continue
            if NEW_ITEM.match(line):
                if cur is not None: groups.append(cur)
                cur = line.rstrip("\n")
            elif cur is not None:
                cur += " " + s            # continuation (wrapped pron/meaning)
                appended += 1
        if cur is not None: groups.append(cur)
    sys.stderr.write(f"[{path.rsplit(chr(92),1)[-1]}] continuation lines appended: {appended}\n")
    level, last = 0, None
    for g in groups:
        m = ENTRY.match(g)
        if not m:
            sys.stderr.write("UNPARSED: " + g[:80] + "\n");
            continue
        item = int(m.group(1)); word = m.group(2); pos = m.group(3); tail = m.group(4).strip()
        if last is not None and item == 1 and last != 1: level += 1
        if level == 0: level = 1
        last = item
        yield level, item, word, pos, tail

# pron char-count from -table
tbl_pron_len = {}
for level, item, word, pos, tail in build_entries(TBL):
    parts = re.split(r"\s{2,}", tail.strip())
    tbl_pron_len[(level, item)] = len(parts[0].replace(" ", "")) if parts else 0

def norm(t):
    t = t.replace("ํา", "ำ").replace("าํ", "ำ")
    t = re.sub(r"\s*,\s*", ", ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def norm_meaning(t):
    t = norm(t)
    # remove line-wrap spaces inserted between two Thai characters (Thai has no inter-word spaces)
    t = re.sub(r"(?<=[฀-๿]) (?=[฀-๿])", "", t)
    return t

def split_tail(tail, plen):
    if plen <= 0: return "", tail.strip()
    cnt = 0; i = -1
    for i, ch in enumerate(tail):
        if ch != " ":
            cnt += 1
            if cnt == plen: break
    return tail[:i+1].strip(), tail[i+1:].strip()

# manual fixes for the 2 known glitches
WORD_FIX = {(1, 963): "trousers"}
SPLIT_FIX = {(3, 568): ("แมนนูแฟคเชอะเรอะ", "ผู้ผลิต")}

rows, counts = [], {}
for level, item, word, pos, tail in build_entries(RAW):
    word = re.sub(r"[^\x00-\x7F]+", "", word).strip()  # drop any glued non-ASCII
    word = WORD_FIX.get((level, item), word)
    if (level, item) in SPLIT_FIX:
        pron, meaning = SPLIT_FIX[(level, item)]
    else:
        pron, meaning = split_tail(tail, tbl_pron_len.get((level, item), 0))
    rows.append([level, item, word, pos + ".", norm(pron), norm_meaning(meaning)])
    counts[level] = counts.get(level, 0) + 1

with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["level", "item", "word", "part_of_speech", "pronunciation", "meaning"])
    w.writerows(rows)

print("counts per level:", counts, "total:", len(rows))
bylevel = {}
for r in rows: bylevel.setdefault(r[0], set()).add(r[1])
for lv in sorted(bylevel):
    mx = max(bylevel[lv]); miss = [i for i in range(1, mx+1) if i not in bylevel[lv]]
    print(f"level {lv}: max={mx} present={len(bylevel[lv])} missing={miss}")
print("--- formerly-broken entries ---")
for r in rows:
    if (r[0],r[1]) in ((1,963),(3,568)):
        print(r[0], r[1], "|", r[2], "|", r[3], "|", r[4], "|", r[5])
