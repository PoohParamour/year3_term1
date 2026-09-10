from _helper import md, code

CELLS = [
md(r'''
# Retail Customer Analytics — CRISP-DM Mini Project

**ชุดข้อมูล:** ธุรกรรมค้าปลีก omni-channel 24 เดือน (2024-09-01 → 2026-08-31) · สกุลเงิน THB
**วันอ้างอิง (Reference Date):** 2026-08-31

## คำถามจากผู้บริหาร 3 ข้อ

| # | คำถาม | ตอบในหัวข้อ |
|---|---|---|
| 1 | **Increase Basket Size** — สินค้าใดมักถูกซื้อคู่กัน ควรจัดโปรร่วมกันอย่างไร | §4.1 |
| 2 | **Customer Segmentation** — พฤติกรรมการซื้อแบ่งลูกค้าได้กี่กลุ่ม แต่ละกลุ่มมีลักษณะเด่นอย่างไร | §4.2 |
| 3 | **Customer Retention** — ลูกค้ารายใดมีแนวโน้มหยุดซื้อ และพฤติกรรมใดเป็นสัญญาณเตือน | §4.3 |

## โครงสร้าง Notebook (ตามกระบวนการ CRISP-DM)

```
§1 Business Understanding   →  แปลคำถามธุรกิจเป็นโจทย์ ML + เหตุผลการเลือกเทคนิค
§2 Data Understanding       →  สำรวจข้อมูล 6 ตาราง + ตรวจคุณภาพข้อมูล + EDA
§3 Data Preparation         →  ทำความสะอาด + สร้าง 3 ชุดข้อมูลสำหรับ 3 โจทย์
§4 Modeling                 →  4.1 Association Rules · 4.2 Clustering · 4.3 Classification
§5 Evaluation               →  ประเมินผลเทียบเป้าหมายธุรกิจ + หาสัญญาณเตือน
§6 Deployment               →  รายชื่อลูกค้าเสี่ยง + กลยุทธ์ + แผน monitoring
```

> **หมายเหตุการรัน:** notebook นี้ออกแบบให้กด **Run All** ผ่านตั้งแต่ต้นจนจบโดยไม่มี Error
> ทุกตัวเลขที่อ้างอิงในรายงานถูกบันทึกลง `outputs/report_values.json` โดยอัตโนมัติ
'''),

md(r'''
---
# §0 Setup

ตั้งค่าสภาพแวดล้อม กำหนดค่าคงที่ และสร้างกลไกบันทึกตัวเลขสำหรับรายงาน
'''),

code(r'''
# --- Standard library ---
import json
import time
import warnings
from pathlib import Path

# --- Core data stack ---
import numpy as np
import pandas as pd

# --- Visualisation ---
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# Reproducibility: one seed used everywhere in this notebook
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Plot styling - consistent across every figure so the report looks like one document
# NOTE: seaborn's theme overwrites rcParams, so it must be applied BEFORE the font
# configuration in the next cell - otherwise the Thai font setting is silently lost.
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
    "figure.autolayout": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "font.size": 10,
})

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 200)

print(f"pandas {pd.__version__} | numpy {np.__version__} | matplotlib {matplotlib.__version__}")
'''),

md(r'''
### การตั้งค่าฟอนต์ภาษาไทยสำหรับกราฟ

matplotlib ไม่มีฟอนต์ภาษาไทยเป็นค่าเริ่มต้น ถ้าไม่ตั้งค่าตรงนี้ ข้อความไทยบนกราฟทุกใบ
จะกลายเป็นสี่เหลี่ยมว่าง (□□□) ซึ่งทำให้รายงานใช้งานไม่ได้

เซลล์ถัดไปจะค้นหาฟอนต์ที่รองรับภาษาไทยในเครื่องโดยอัตโนมัติ ทดสอบว่าเรนเดอร์ได้จริง
แล้วจึงนำไปใช้ — หากไม่พบจะแจ้งเตือนอย่างชัดเจนแทนที่จะปล่อยให้กราฟเสียเงียบ ๆ
'''),

code(r'''
from matplotlib import font_manager as fm
from matplotlib import ft2font

# Candidate Thai-capable fonts across the three major platforms, best-looking first.
THAI_FONT_CANDIDATES = [
    # macOS
    "/System/Library/Fonts/Supplemental/SukhumvitSet.ttc",
    "/System/Library/Fonts/Supplemental/Thonburi.ttc",
    "/System/Library/Fonts/Supplemental/Ayuthaya.ttf",
    "/System/Library/Fonts/Supplemental/Krungthep.ttf",
    # Linux
    "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansThai-Regular.ttf",
    "/usr/share/fonts/truetype/tlwg/Sarabun.ttf",
    "/usr/share/fonts/truetype/tlwg/Loma.ttf",
    # Windows
    "C:/Windows/Fonts/leelawui.ttf",
    "C:/Windows/Fonts/leelawad.ttf",
    "C:/Windows/Fonts/tahoma.ttf",
]

THAI_PROBE = ord("ก")   # a plain Thai consonant
DIGIT_PROBE = ord("9")  # charts need Latin digits too - some Thai fonts lack them


def font_supports_thai(path):
    # A font qualifies only if it can render BOTH Thai letters and Latin digits.
    try:
        face = ft2font.FT2Font(path)
        return bool(face.get_char_index(THAI_PROBE)) and bool(face.get_char_index(DIGIT_PROBE))
    except Exception:
        return False


def find_thai_font():
    # 1) known locations, in order of preference
    for path in THAI_FONT_CANDIDATES:
        if Path(path).exists() and font_supports_thai(path):
            return path
    # 2) fall back to scanning whatever is installed on this machine
    for entry in fm.fontManager.ttflist:
        if font_supports_thai(entry.fname):
            return entry.fname
    return None


THAI_FONT_PATH = find_thai_font()

if THAI_FONT_PATH:
    fm.fontManager.addfont(THAI_FONT_PATH)
    THAI_FONT_NAME = fm.FontProperties(fname=THAI_FONT_PATH).get_name()
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [THAI_FONT_NAME, "DejaVu Sans", "Arial"]
    # Thai fonts often lack U+2212 MINUS SIGN; use the ASCII hyphen instead
    plt.rcParams["axes.unicode_minus"] = False
    print(f"ฟอนต์ภาษาไทยที่ใช้: {THAI_FONT_NAME}")
    print(f"  ที่อยู่ไฟล์: {THAI_FONT_PATH}")
else:
    THAI_FONT_NAME = None
    print("!" * 70)
    print("คำเตือน: ไม่พบฟอนต์ภาษาไทยในเครื่องนี้")
    print("ข้อความไทยบนกราฟจะแสดงเป็นสี่เหลี่ยมว่าง (tofu)")
    print("วิธีแก้: ติดตั้งฟอนต์ เช่น Noto Sans Thai หรือ Sarabun แล้วรันใหม่")
    print("!" * 70)
'''),

code(r'''
# Verify the font actually renders Thai - do not just trust that it was set.
# matplotlib emits a warning per missing glyph, so we render a probe string
# containing tone marks, vowels above/below, digits and a minus sign, then
# count how many glyphs it could not draw.
def verify_thai_rendering():
    probe = "ทดสอบ ลูกค้าที่กำลังจะหยุดซื้อ ก้ ก่ ก๊ ก๋ ญ ฐ · 90% -1.5 (บาท)"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fig_probe, ax_probe = plt.subplots(figsize=(6, 1))
        ax_probe.text(0.02, 0.5, probe)
        ax_probe.axis("off")
        fig_probe.canvas.draw()
        plt.close(fig_probe)
    return [str(w.message) for w in caught if "missing from font" in str(w.message)]


missing_glyphs = verify_thai_rendering()
THAI_RENDER_OK = (THAI_FONT_NAME is not None) and (len(missing_glyphs) == 0)

if THAI_RENDER_OK:
    print("ตรวจสอบการเรนเดอร์: ผ่าน - วาดภาษาไทย ตัวเลข วรรณยุกต์ และเครื่องหมายลบได้ครบ")
elif THAI_FONT_NAME:
    print(f"ตรวจสอบการเรนเดอร์: พบอักขระที่วาดไม่ได้ {len(missing_glyphs)} ตัว")
    for m in missing_glyphs[:5]:
        print(f"   {m}")
else:
    print("ข้ามการตรวจสอบ เพราะไม่พบฟอนต์ภาษาไทย")
'''),

code(r'''
# --- Paths (all relative, so the notebook runs anywhere the folder is copied) ---
DATA_DIR = Path("student_package")
OUT_DIR = Path("outputs")
FIG_DIR = OUT_DIR / "figures"
TBL_DIR = OUT_DIR / "tables"
for d in (FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)

# --- Key dates (from DATA_DICTIONARY.md) ---
REFERENCE_DATE = pd.Timestamp("2026-08-31")   # end of observation window
FEATURE_CUTOFF = pd.Timestamp("2026-06-01")   # churn features may use data up to HERE only
OUTCOME_START = pd.Timestamp("2026-06-02")    # churn outcome window starts here
WINDOW_START = pd.Timestamp("2024-09-01")     # start of observation window

# Churn definition: churn = 1  <=>  recency_days > 90  <=>  no purchase in [OUTCOME_START, REFERENCE_DATE]
CHURN_HORIZON_DAYS = 90

print(f"Feature window : {WINDOW_START.date()} -> {FEATURE_CUTOFF.date()}")
print(f"Outcome window : {OUTCOME_START.date()} -> {REFERENCE_DATE.date()}  ({CHURN_HORIZON_DAYS} days)")
'''),

md(r'''
### กลไกบันทึกตัวเลขสำหรับรายงาน

ทุกตัวเลขที่จะถูกอ้างอิงในรายงานต้องผ่านฟังก์ชัน `rv()` เพื่อบันทึกลง `outputs/report_values.json`
ทำให้ **ตัวเลขในรายงานตรวจสอบย้อนกลับมาที่ผลรันจริงได้ทุกตัว** ไม่มีการพิมพ์ตัวเลขจากความจำ
'''),

code(r'''
# Report-value registry: every number quoted in the report must pass through rv()
REPORT_VALUES = {}


def rv(key, value, note=""):
    # Record a value for the report and return it unchanged, so it can be used inline.
    if isinstance(value, (np.integer,)):
        value = int(value)
    elif isinstance(value, (np.floating,)):
        value = float(value)
    elif isinstance(value, (np.bool_,)):
        value = bool(value)
    REPORT_VALUES[key] = {"value": value, "note": note} if note else {"value": value}
    return value


def save_fig(fig, name):
    # Save a figure to outputs/figures and register its path for the report.
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path)
    REPORT_VALUES.setdefault("_figures", []).append(str(path))
    return path


def save_table(df, name, index=False):
    # Save a table to outputs/tables and register its path + shape for the report.
    path = TBL_DIR / f"{name}.csv"
    df.to_csv(path, index=index)
    REPORT_VALUES.setdefault("_tables", []).append({"path": str(path), "rows": int(len(df))})
    return path


def dump_report_values():
    # Write every registered value to disk. Called at the end of the notebook.
    with open(OUT_DIR / "report_values.json", "w", encoding="utf-8") as fh:
        json.dump(REPORT_VALUES, fh, ensure_ascii=False, indent=2, sort_keys=True)
    n = len([k for k in REPORT_VALUES if not k.startswith("_")])
    print(f"Wrote {n} report values -> {OUT_DIR / 'report_values.json'}")


# Record the font situation so the report can state which font produced its figures
rv("fig_thai_font_name", THAI_FONT_NAME if THAI_FONT_NAME else "not found")
rv("fig_thai_render_ok", bool(THAI_RENDER_OK))

print("Report-value registry ready.")
'''),
]
