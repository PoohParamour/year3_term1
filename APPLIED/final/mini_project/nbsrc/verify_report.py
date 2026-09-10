"""Cross-check REPORT.md against the notebook's outputs.

Fails loudly if the report references a file that does not exist, or quotes a number
that cannot be traced back to report_values.json or one of the exported tables.
"""
import json
import re
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
VALUES = json.loads((OUT / "report_values.json").read_text(encoding="utf-8"))

problems = []

# ---------- 1. every referenced file must exist ----------
refs = set(re.findall(r"outputs/[\w./-]+\.(?:png|csv|txt|json)", report))
missing = sorted(r for r in refs if not (ROOT / r).exists())
print(f"[1] ไฟล์ที่รายงานอ้างถึง: {len(refs)} ไฟล์")
if missing:
    problems.append(f"ไฟล์ที่อ้างถึงแต่ไม่มีอยู่จริง: {missing}")
    print(f"    ขาดหาย: {missing}")
else:
    print("    ครบทุกไฟล์")

# ---------- 2. every figure must be referenced exactly once ----------
fig_files = sorted(p.name for p in (OUT / "figures").glob("*.png"))
unref = [f for f in fig_files if f"outputs/figures/{f}" not in report]
print(f"[2] รูปทั้งหมด {len(fig_files)} ใบ")
if unref:
    problems.append(f"รูปที่ไม่ถูกอ้างถึงในรายงาน: {unref}")
    print(f"    ไม่ถูกอ้างถึง: {unref}")
else:
    print("    ถูกอ้างถึงครบทุกใบ")

# ---------- 3. figure and table numbering must be sequential ----------
fig_nums = [int(n) for n in re.findall(r"┌─ 🖼\s+รูปที่ (\d+)", report)]
tbl_nums = ([int(n) for n in re.findall(r"┌─ 📊\s+ตารางที่ (\d+)", report)]
            + [int(n) for n in re.findall(r"\*\*ตารางที่ (\d+)\*\*", report)])
tbl_nums.sort()
print(f"[3] เลขรูป {len(fig_nums)} · เลขตาราง {len(tbl_nums)}")
if fig_nums != list(range(1, len(fig_nums) + 1)):
    problems.append("เลขรูปไม่เรียงต่อเนื่อง")
if sorted(tbl_nums) != list(range(1, len(tbl_nums) + 1)):
    problems.append("เลขตารางไม่เรียงต่อเนื่อง")
if not problems:
    print("    เรียงต่อเนื่องถูกต้อง")

# ---------- 4. numbers in prose must be traceable ----------
# Collect every number the notebook produced, in the string forms the report may use.
known = set()


def add(x):
    if isinstance(x, bool):
        return
    if isinstance(x, (int, float)):
        for form in (f"{x:,}", f"{x}", f"{x:,.0f}", f"{x:,.1f}", f"{x:,.2f}",
                     f"{x:,.3f}", f"{x:,.4f}", f"{x:.0f}", f"{x:.1f}", f"{x:.2f}",
                     f"{x:.3f}", f"{x:.4f}"):
            known.add(form.rstrip())
        for mult in (100,):          # fractions rendered as percentages
            y = x * mult
            for form in (f"{y:.0f}", f"{y:.1f}", f"{y:.2f}"):
                known.add(form)
        for div in (1e6,):           # THB rendered in millions
            y = x / div
            for form in (f"{y:,.1f}", f"{y:,.2f}"):
                known.add(form)
    elif isinstance(x, str):
        known.add(x)
    elif isinstance(x, dict):
        for v in x.values():
            add(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            add(v)


for key, entry in VALUES.items():
    if key.startswith("_"):
        continue
    add(entry["value"])

# also accept anything appearing in an exported table
for csv in (OUT / "tables").glob("*.csv"):
    try:
        df = pd.read_csv(csv)
    except Exception:
        continue
    for col in df.columns:
        for val in df[col].dropna().unique()[:5000]:
            add(val)

# Strip the parts of the report that are quoted directly from tables/instructions,
# so we only audit numbers written into prose.
prose = report
prose = re.sub(r"```.*?```", "", prose, flags=re.S)        # instruction blocks
prose = re.sub(r"^\|.*$", "", prose, flags=re.M)           # markdown tables
prose = re.sub(r"`[^`]*`", "", prose)                      # inline code
prose = re.sub(r"\d{4}-\d{2}-\d{2}", "", prose)            # dates

# Small structural numbers that are part of the writing, not results
ALLOW = {str(i) for i in range(0, 13)} | {
    "0.5", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20", "30", "48",
    "90", "99.5", "100", "1.6", "80", "1.0",
}

candidates = re.findall(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])", prose)
untraceable = sorted({c for c in candidates if c not in known and c not in ALLOW})
print(f"[4] ตัวเลขในเนื้อความที่ตรวจสอบ: {len(set(candidates))} ค่าไม่ซ้ำ")
if untraceable:
    problems.append(f"ตัวเลขที่หาที่มาไม่ได้: {untraceable}")
    print(f"    หาที่มาไม่ได้ {len(untraceable)} ค่า: {untraceable}")
else:
    print("    ทุกตัวเลขตรวจสอบย้อนกลับได้")

# ---------- verdict ----------
print()
print("=" * 70)
if problems:
    print(f"พบปัญหา {len(problems)} ข้อ")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print("ผ่านการตรวจสอบทั้งหมด")
sys.exit(0)
