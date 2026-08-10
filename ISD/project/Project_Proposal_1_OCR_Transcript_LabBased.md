# ใบเสนอโครงการ (Project Proposal) — ฉบับอิงผลงาน Lab จริง (Week 1–6)

## โปรเจกต์ที่ 1: OCR Transcript (สจล.)

**วิชา 06026240 Intelligent System Development**

> เอกสารนี้เขียนจาก **ผลงาน Lab ที่ทำจริงในสัปดาห์ที่ 1–6** (โค้ด, ผลรัน, ตัวเลข evaluation ที่มีอยู่จริงในโฟลเดอร์ `week1/`–`week6/`) ไม่ใช่แผนที่ยังไม่ได้ทำ — ตัวเลขทุกตัวในเอกสารนี้ดึงมาจากไฟล์ผลลัพธ์จริง สามารถตรวจสอบย้อนกลับได้จากไฟล์ที่อ้างอิงในแต่ละหัวข้อ

| กลุ่ม / Section | สมาชิกในทีม (3 คน) |
|---|---|
| _______________ | 1. ____________________ (รหัส __________) |
|  | 2. ____________________ (รหัส __________) |
|  | 3. ____________________ (รหัส __________) |

---

## 0. สรุปผลงาน Lab แต่ละสัปดาห์ (Week 1–6)

| Week | หัวข้อ | สิ่งที่ทำจริง | ไฟล์หลักฐาน |
|---|---|---|---|
| **1** | Intro + Git/GitHub team workflow | อ่านเนื้อหาแนะนำวิชา + วิธีทำงานเป็นทีมด้วย Git/GitHub (ยังไม่มีงาน dataset/โค้ด) | `week1/ch1_Introduction-1.pdf`, `week1/git_github_team_guide-1.pdf` |
| **2** | Introduction to Computer Vision | เนื้อหาบรรยายพื้นฐาน CV (ยังไม่มี lab hands-on) | `week2/ch2_Introduction to Computer Vision.pdf` |
| **3** | สร้างระบบ OCR หลายเอนจิน (`Lab3_ocr_system`) | เขียน pipeline OCR แบบ CLI รองรับ 4 engine (PaddleOCR, Tesseract, TrOCR, Ensemble) พร้อม preprocessing (denoise, CLAHE, deskew, adaptive threshold) และโมดูล evaluation (CER/WER) — รันทดสอบจริงกับ Transcript ตัวอย่าง 3 ฉบับ | `week3/Lab3_ocr_system/.../ocr_system/` (`src/ocr_system/*.py`, `outputs/71010001/`, `outputs/72100002/`, `outputs/73036003/`) |
| **4** | สกัดฟิลด์จาก OCR ให้เป็น JSON โครงสร้าง (`Lab4`) | เขียน `transcript_extraction.py` (regex/rule-based parser) แปลงผล OCR ดิบ → JSON ตามสคีมาเดียวกับ ground truth (`header_detail`/`transcript_detail`/`footer_detail`) — ทดสอบกับฉบับ 71010001 | `week4/Lab4.zip` (`transcript_extraction.py`, `ocr_result.json`, `extracted_transcript.json`, `ground_truth.json`) |
| **5** | สร้างชุดข้อมูล Augmented + Label (`Lab5_transcript_dataset`) | เขียน `build_dataset.py` เรนเดอร์ PDF ต้นฉบับ 48 ฉบับ (ป.ตรี 24 + บัณฑิตศึกษา 24) เป็นภาพ แล้ว augment ภาพละ 5 แบบ → รวม 288 ภาพ พร้อม `manifest.csv` จับคู่ภาพ ↔ ground truth | `week5/Lab5_transcript_dataset/` (`build_dataset.py`, `labels/manifest.csv`, `images/`) |
| **5** (ส่วนแยก — คนละโปรเจกต์) | Curriculum Book QA (`Lab5_curriculum_dsba`) | ทำ mapping ground truth + Q&A จากเล่มหลักสูตร DSBA — เป็นงานของโปรเจกต์ **P2 (OCR หลักสูตร + LLM ตอบคำถาม)** ไม่ใช่ของ P1 จึงไม่นำมานับใน proposal นี้ | `week5/Lab5_curriculum_dsba/` |
| **6** | ประเมินความแม่นยำเต็มชุดข้อมูล (`Lab6_ocr_evaluation`) | รัน Tesseract (`tha+eng`) กับภาพทั้ง 282/288 ภาพที่มี ground truth คู่ วัด Field-level, Page-level, Category-level accuracy จริง พร้อมบันทึกเวลาที่ใช้ | `week6/Lab6_ocr_evaluation/` (`lab6_evaluation.ipynb`, `results/*.csv`) |

**สายงานที่ต่อเนื่องกัน:** week3 สร้างเครื่องมือ OCR → week4 สร้างตัวแปลงผล OCR เป็นฟิลด์โครงสร้าง → week5 ขยายชุดข้อมูลด้วย augmentation → week6 ใช้ชุดข้อมูล week5 มาวัดผลเครื่องมือจาก week3 อย่างเป็นระบบ — ผลลัพธ์ที่ได้ในหัวข้อ 7 (Evaluation) จึงเป็นตัวเลขจริงที่วัดจากงานทั้งสายนี้ ไม่ใช่ตัวเลขประมาณการ

---

## ⚠️ ความปลอดภัยของข้อมูลและการปฏิบัติตาม PDPA

Transcript (โดยเฉพาะภาพ Real) มีชื่อ-นามสกุล รหัสนักศึกษา ผลการเรียน และ GPA ซึ่งเป็น **"ข้อมูลส่วนบุคคล"** และผลการเรียนถือเป็นข้อมูลที่มีความอ่อนไหวสูงตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล (PDPA) ทีมได้เซ็นแบบฟอร์ม **PDPA Consent** ของรายวิชาเป็นลายลักษณ์อักษรก่อนเก็บ/ใช้ข้อมูลทุกฉบับ และนำข้อมูลไปใช้เพื่อวัตถุประสงค์การเรียนการสอนในรายวิชานี้เท่านั้น

**Checklist มาตรการที่ทีมต้องปฏิบัติ**

- [x] ใช้ Transcript จริงเฉพาะฉบับที่ได้รับความยินยอมเป็นลายลักษณ์อักษรจากเจ้าของข้อมูลแล้วเท่านั้น
- [x] เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth โดยจำกัดสิทธิ์การเข้าถึง (access control) เฉพาะสมาชิกทีมและอาจารย์ผู้สอน
- [x] เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ในคอมพิวเตอร์ส่วนตัวที่ใส่รหัสผ่านที่ไม่ได้บอกใคร
- [x] ไม่เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ในคอมพิวเตอร์ที่มีบุคคลอื่นใช้
- [x] ห้าม upload ไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ขึ้น public GitHub repository
- [x] Anonymize/มาสก์ข้อมูลอ่อนไหว (ชื่อ, รหัสนักศึกษา, เกรดรายวิชา) ก่อนนำไปใส่ใน slide/รายงาน/README ที่เผยแพร่ต่อบุคคลอื่น
- [x] ไม่นำข้อมูลไปใช้เพื่อวัตถุประสงค์อื่นนอกเหนือจากการเรียนการสอนในรายวิชานี้

**มาตรการเพิ่มเติมที่ทีมดำเนินการจริง**

1. Dataset/ground truth ทั้งหมดที่ใช้ใน week3–week6 เป็นไฟล์ synthetic ที่อาจารย์จัดเตรียมให้ (ไม่มีข้อมูลนักศึกษาจริงนอกชั้นเรียนปะปน) — ยังไม่มีการใช้ข้อมูล Real ในขั้นตอนนี้
2. รัน OCR/ประเมินผลทั้งหมด **local บนเครื่องทีมเอง** (Tesseract/PaddleOCR/TrOCR แบบ offline) ไม่ส่งภาพออกไป cloud API ภายนอก
3. โฟลเดอร์ dataset ผลลัพธ์ (`week3/.../outputs/`, `week5/.../images/`) เก็บใน repo ส่วนตัว ยังไม่ upload public — จะทำ `.gitignore` ครอบคลุมก่อน push จริง
4. ลบไฟล์ Transcript และ ground truth ทั้งหมดออกจากเครื่องพัฒนาและ cloud storage ภายใน 7 วันหลังประกาศเกรดรายวิชา

---

## 1. ภาพรวมโปรเจกต์ (Overview)

ทีมพัฒนาระบบอ่าน Transcript ของ สจล. แบบอัตโนมัติ โดยตลอด 6 สัปดาห์แรกได้ลงมือสร้างและทดสอบส่วนประกอบหลักครบทุกชิ้นแล้ว: **(1)** OCR pipeline หลายเอนจิน + preprocessing (week3), **(2)** ตัวแปลงผล OCR ดิบให้เป็นฟิลด์โครงสร้าง (week4), **(3)** ชุดข้อมูล synthetic + synthetic&noise ที่ label ครบ 288 ภาพ (week5), และ **(4)** การวัดความแม่นยำจริงระดับฟิลด์/หน้า/หมวดหมู่บนชุดข้อมูลทั้งหมด (week6) ผลที่ได้ชี้ชัดว่า **field ข้อความ (ชื่อ, คณะ, ปริญญา) อ่านได้แม่นยำสูง (>95%)** แต่ **field วันที่และตารางรายวิชา/เกรดยังเป็นช่องว่างที่ต้องพัฒนาต่อ** ซึ่งเป็นเป้าหมายหลักของงานหลัง midterm (ดูหัวข้อ 7.4 "แผนก้าวข้าม 91%")

---

## 2. ข้อมูล (Dataset) และ Ground Truth

ต้นฉบับที่อาจารย์ให้คือ **PDF 48 ฉบับ** (ป.ตรี `input_Bachelor_Degrees`/`input` 24 ฉบับ = กลุ่ม `th`, บัณฑิตศึกษา `input_Master`/`input_G` 24 ฉบับ = กลุ่ม `G`) แต่ละฉบับมี ground truth JSON คู่กัน 1:1 ทีมนำมาสร้างเป็นชุดข้อมูลจริงใน week5 (`Lab5_transcript_dataset/build_dataset.py`) ดังนี้

| ประเภทข้อมูล | แหล่งที่มา | จำนวนจริงที่สร้าง | Ground Truth |
|---|---|---|---|
| **Synthetic** (ต้นฉบับ) | เรนเดอร์จาก PDF ที่อาจารย์ให้ เป็น PNG 150 DPI | **48 ภาพ** (`th` 24 + `G` 24) | `ground_truth/<group>/Json_<id>_<th\|en>.json` — คัดลอกจาก `week3/ground_truth_transcript 2/` |
| **Synthetic & noise** | Augment ภาพต้นฉบับ 5 แบบ/ภาพ (ดูหัวข้อ 3) ด้วย `build_dataset.py` (seed ผูกกับรหัส นศ. → รันซ้ำได้ผลเดิม) | **240 ภาพ** (48 × 5) | ใช้ JSON เดิมของภาพต้นฉบับ (augmentation ไม่เปลี่ยนค่าข้อความ) |
| **Real** | — ยังไม่ใช้ในโปรเจกต์นี้ | 0 | — |
| **รวม** | | **288 ภาพ** | — |

**เช็คความครบถ้วนของข้อมูล (ตัวเลขจริงจาก `manifest.csv` และ `Lab6/README.md`)**

- [x] Synthetic (48 ภาพ)
- [x] Synthetic & noise (240 ภาพ)
- [ ] Real *(ไม่ใช้ — ฟอร์มระบุว่าเป็น optional "ถ้ามี")*
- [x] Ground truth ครบ **287/288** ภาพ — ขาด ground truth ของรหัส `74176008` (1 ต้นฉบับ + augmented 5 ภาพ = 6 ภาพที่ไม่มีคู่ label) ตามที่ระบุใน `week6/Lab6_ocr_evaluation/README.md`
- [x] ชุดที่ใช้ประเมินผลจริงใน week6: **282 ภาพ** (47 original + 235 augmented ที่มี ground truth ครบ)
- [ ] แบ่ง train/val/test — **ยังไม่ทำ** (week1–6 เป็นขั้นตอนสร้างข้อมูล/วัดผลบนทั้งชุด ยังไม่เข้าสู่ขั้นตอนเทรนโมเดล) → วางแผนแบ่งช่วงหลัง midterm ตามหัวข้อ 7.4

---

## 3. Data Augmentation

ใช้ `week5/Lab5_transcript_dataset/build_dataset.py` (OpenCV) สร้าง augmentation **5 แบบต่อภาพ** จำลองสภาพเอกสารจริง — พารามิเตอร์ที่ใช้จริงในโค้ด:

| รูปแบบ Augmentation (`aug_type`) | พารามิเตอร์ที่ใช้จริง (จากโค้ด) | เหตุผลที่เลือกใช้ |
|---|---|---|
| `rotate_bright` | หมุน ±3° (`rng.uniform(-3, 3)`) + เพิ่มความสว่าง | จำลองวางเอกสารเอียงเล็กน้อย + สแกนสว่างเกิน |
| `noise` | Gaussian noise, σ สุ่ม 8–18 ระดับความเข้ม (`rng.normal(0, rng.uniform(8,18), ...)`) | จำลองเม็ด noise จากเซนเซอร์/เครื่องถ่ายเอกสาร |
| `blur_contrast` | เบลอ + เพิ่มคอนทราสต์ | จำลองภาพโฟกัสหลุด |
| `perspective` | Perspective warp (keystone) | จำลองถ่ายจากมุมเอียงด้วยมือถือ |
| `jpeg_dark` | บีบอัด JPEG คุณภาพต่ำ + ลดความสว่าง | จำลองภาพถ่ายมือถือคุณภาพต่ำในที่แสงน้อย |

การสุ่มใช้ **seed อิงจากรหัสนักศึกษา + เลข variant** → รันสคริปต์ซ้ำได้ผลลัพธ์เดิมทุกครั้ง (reproducible)

**จำนวนข้อมูลจริงที่ทำได้ (แยกตามระดับการศึกษา)**

| ระดับการศึกษา (`group`) | ภาพต้นฉบับ | Augmented ต่อภาพ | รวมที่ทำจริง |
|---|---|---|---|
| ป.ตรี (`th`) | 24 ภาพ | ×5 เท่า | **144 ภาพ** (24 + 120) |
| บัณฑิตศึกษา (`G`) | 24 ภาพ | ×5 เท่า | **144 ภาพ** (24 + 120) |
| **รวม** | **48 ภาพ** | | **288 ภาพ** |

> หมายเหตุ: ตัวเลขนี้ต่ำกว่าเป้าหมายขั้นต่ำที่ระบุในฟอร์ม (ป.ตรี ≥450 / ป.บัณฑิต ≥750) — เป็นจุดที่ทีมวางแผนขยายเพิ่มหลัง midterm โดยเพิ่มจำนวน variant ต่อภาพ (เช่น ×15–×20) ด้วยสคริปต์เดิม

---

## 4. การ Labeling / Annotation

**ฟิลด์ที่มี ground truth อยู่แล้ว** (ใช้ตามที่อาจารย์ให้ ยังไม่ต้อง label เพิ่ม): `header_detail` (uni_name, uni_address, student_id, faculty_name, prename, name, date_of_birth, admis_date, grad_date, grad_reason, degree, major, program, honor), `transcript_detail.semesters[].subject[]` (subject_id, subject_name, type, credit, grade_earn), `footer_detail` (by_signature, by_position, by_reg, updated_at)

**เครื่องมือและ Format ที่ใช้จริง (week5)**

- `build_dataset.py` **จับคู่ภาพกับ ground truth อัตโนมัติ** ผ่านรหัสนักศึกษาในชื่อไฟล์ ไม่ต้อง label ข้อความด้วยมือ — บันทึกผลจับคู่ลง `labels/manifest.csv` (คอลัมน์ `image_path`, `split`, `group`, `student_id`, `aug_type`, `gt_path`, `gt_exists`) รวม **288 แถว**
- ยังไม่มีการ label เพิ่มเติม เช่น bounding box ของตาราง/ลายเซ็น — เป็นงานที่ต้องทำเพิ่มเพื่อรองรับ field-level extraction แบบมีโครงสร้างจริง (ดูหัวข้อ 7.4)

---

## 5. แนวทางการอ่านภาพ (OCR) — สถาปัตยกรรมที่สร้างจริงใน week3–week4

**Stage 1 — Preprocessing** (`week3/.../src/ocr_system/preprocessing.py`, ใช้งานจริง)
- `resize_if_small` — ขยายภาพถ้าความกว้าง < 1200px
- `fastNlMeansDenoising` — ลด noise
- CLAHE (`clipLimit=2.0, tileGridSize=(8,8)`) — เพิ่มคอนทราสต์เฉพาะจุด
- `estimate_skew_angle` + `rotate_bound` — หามุมเอียงจาก `cv2.minAreaRect` ของพื้นที่ตัวอักษร แล้วหมุนแก้ (deskew) — ครอบคลุมมุมเอียงจนถึง ±15°
- `adaptiveThreshold` (Gaussian, blockSize=35, C=11) — แปลงเป็นภาพขาวดำ

**Stage 2 — OCR Engine** (`engine_factory.py` + `engines/`) — สร้างและทดสอบจริง 4 engine:
| Engine | สถานะ | ผลทดสอบเบื้องต้น (3 ตัวอย่าง, week3) |
|---|---|---|
| **Tesseract** (`tha+eng`) | ✅ ทดสอบเต็มชุด (282 ภาพ, week6) | อ่านภาษาอังกฤษได้ดี (เช่น `KING MONGKUTI'S...`, ผิดเล็กน้อยที่ apostrophe/ช่องว่างติดกัน) ภาษาไทยมีสัญลักษณ์แปลกปน (เส้นตาราง/สระถูกอ่านผิดเป็นอักขระ) |
| **PaddleOCR** | ✅ ทดสอบตัวอย่าง (week3) ยังไม่ evaluate เต็มชุด | อ่านภาษาอังกฤษได้ใกล้เคียง ground truth มาก (`FOUNDATION ENGLISH 1`, ตัวเลขหน่วยกิต/เกรดถูกต้อง) — ดูมีแนวโน้มดีกว่า Tesseract ในตัวอย่าง EN |
| **TrOCR** | ✅ ใช้งานได้ | ตามที่ README ระบุ ยังไม่เหมาะกับเอกสารเต็มหน้า เหมาะกับข้อความสั้นที่ crop แล้ว |
| **Ensemble** (Paddle+Tesseract) | ✅ ใช้งานได้ | รวมผลแบบง่าย (concat) — พบว่าทำให้ reference/prediction length ต่างกันมาก (CER พุ่งสูงผิดปกติในการวัดแบบ full-text) ต้องปรับวิธีรวมผลก่อนใช้จริง |

**Stage 3 — Structured Field Extraction** (`week4/transcript_extraction.py`, ใช้งานจริง) — ตัวแปลง OCR ดิบ → JSON ตามสคีมา ground truth ด้วย regex/token matching (หา label ภาษาไทย/อังกฤษ เช่น "ชื่อ-สกุล", "Name", "รหัสนักศึกษา", "Student ID" แล้วตัดข้อความส่วนถัดไป) + parser วันที่ไทย/อังกฤษ (`TH_MONTHS`/`EN_MONTHS`) → ISO date

**ผลทดสอบจริง (ฉบับ 71010001):**
- ✅ ถูกต้อง: `uni_name`, `uni_address`, `student_id`, `faculty_name`, `prename`, `date_of_birth`, `degree`, `program`
- ⚠️ เกือบถูก: `name` (`"วศ1วิศวกรรมศาสตร์า1"` มีตัวอักษร `า` เกินมา จาก OCR error)
- ❌ ยังทำไม่ได้: `admis_date` (null), รายวิชาในแต่ละภาคเรียน (`subject: []` ว่างทุกภาค), `GPA`/`GPS` รายภาค, `total_credits_earned`, `cumulative_gpa`, `footer_detail` ทั้งหมด

**สรุป:** โมดูล header extraction ใช้งานได้ดีแล้ว แต่ **ตัวสกัดตารางรายวิชา/เกรดยังไม่ทำงาน** — เป็นช่องว่างหลักที่ทำให้คะแนนความแม่นยำโดยรวมยังไม่ถึงเป้า (ดูหัวข้อ 7.4)

---

## 6. ออกแบบฐานข้อมูล (Database Design)

> 🏷️ *หัวข้อนี้ในฟอร์มระบุว่า "เป็นส่วนหลัง midterm" — ยังไม่มีงาน lab สัปดาห์ 1–6 ที่ตรงหัวข้อนี้ ใส่โครงไว้ล่วงหน้าเผื่อเก็บ/ตัดตอนส่งจริง*

| ชื่อตาราง | ฟิลด์หลัก | Primary / Foreign Key | คำอธิบายความสัมพันธ์ |
|---|---|---|---|
| `students` | `student_id`, `prename`, `name`, `faculty_name`, `degree`, `program`, `major`, `honor`, `date_of_birth`, `admis_date`, `grad_date`, `cumulative_gpa`, `total_credits_earned` | `student_id` **PK** | 1 นักศึกษามีได้หลายภาคเรียน (1:N) |
| `semesters` | `semester_id`, `student_id`, `year`, `sem_num`, `GPA`, `GPS` | `semester_id` **PK**, `student_id` **FK → students** | 1 ภาคเรียนมีได้หลายรายวิชา (1:N) |
| `subjects` | `subject_id`, `subject_name`, `credit`, `type` | `subject_id` **PK** | 1 รายวิชาถูกลงทะเบียนได้โดยหลายนักศึกษา (ผ่าน `enrollments`) |
| `enrollments` | `enrollment_id`, `semester_id`, `subject_id`, `grade_earn` | `enrollment_id` **PK**, FK → `semesters`, `subjects` | ตารางเชื่อมระหว่างภาคเรียนกับรายวิชา เก็บเกรดที่ได้จริง |

Schema นี้ normalize ตรงจากสคีมา JSON ground truth ที่ใช้อยู่แล้วใน week3–week6 จึงนำผลลัพธ์จาก `transcript_extraction.py` (week4) ไป insert ได้ทันทีเมื่อพัฒนาตัวสกัดตารางรายวิชาเสร็จ

---

## 7. การประเมินความแม่นยำ (Evaluation Plan) — ผลจริงจาก `week6/Lab6_ocr_evaluation`

### 7.1 Scope การวัดผลจริง
- OCR engine ที่ประเมิน: **Tesseract (`tha+eng`)** เท่านั้น (engine อื่นยังไม่ evaluate เต็มชุด)
- ภาพที่ใช้: **282/288 ภาพ** ที่มี ground truth คู่ (47 original + 235 augmented)
- เวลาในการรันจริง: **418.4 วินาที รวม 282 ภาพ ≈ 1.48 วินาที/ภาพ** (รวม OCR + เปรียบเทียบผล) — **ผ่านเกณฑ์ Challenge latency <30 วินาที/ฉบับอย่างมาก**

### 7.2 Field-level accuracy (จริง, `results/field_level_summary.csv`)

วัดด้วย fuzzy substring matching: เลื่อนหน้าต่างความยาวเท่ากับ ground truth ไปทาบข้อความ OCR ทั้งหมด หาตำแหน่งที่ CER ต่ำสุด ถือว่าถูกต้องเมื่อ **CER ≤ 0.2**

| field | mean CER | accuracy | หมายเหตุ |
|---|---|---|---|
| `student_id` | 0.002 | **99.6%** | ตัวเลขล้วน regex-friendly |
| `program` | 0.012 | **98.9%** | |
| `degree` | 0.012 | **98.6%** | |
| `prename` | 0.007 | **97.9%** | |
| `faculty_name` | 0.039 | **97.5%** | |
| `name` | 0.037 | **95.7%** | |
| `admis_date` | 0.594 | **0.0%** | เอกสารพิมพ์วันที่แบบไทย ("3 กันยายน 2542") vs ground truth ISO ("1999-09-03") — รูปแบบต่างกันโดยธรรมชาติ ไม่ใช่ OCR ผิด |
| `date_of_birth` | 0.646 | **0.0%** | สาเหตุเดียวกับ `admis_date` |

### 7.3 Page-level และ Category-level (จริง)

| Category (`group`) | field accuracy | page CER | page WER |
|---|---|---|---|
| `th` (ป.ตรี) | 73.7% | 6.83 | 89.0 |
| `G` (บัณฑิตศึกษา) | 73.4% | 4.27 | 50.1 |

| Split | page CER | page WER |
|---|---|---|
| original | 5.79 | 72.5 |
| augmented | 5.53 | 69.5 |

| aug_type | page CER |
|---|---|
| `blur_contrast` | 4.49 (ดีที่สุด) |
| `rotate_bright` | 5.68 |
| `noise` | 5.79 |
| `perspective` | 5.80 |
| `jpeg_dark` | 5.90 (แย่ที่สุด) |

> Page CER > 1 เป็นเรื่องปกติในการวัดแบบนี้ เพราะ reference (header เท่านั้น) สั้นกว่าข้อความ OCR ทั้งหน้ามาก (ซึ่งมีตารางผลการเรียนรวมอยู่ด้วย) — ไม่ใช่ตัวเลขความแม่นยำระดับเอกสารที่แท้จริง เป็นเพียง proxy metric ชั่วคราว

### 7.4 ข้อจำกัดของวิธีวัดปัจจุบัน + แผนก้าวข้าม 91% (ตามที่อาจารย์แนะนำ)

**ข้อจำกัดที่ทราบแล้ว:**
1. **Field-level ไม่ใช่ structured extraction จริง** — เป็น fuzzy substring matching เพราะยังไม่มี bounding-box/layout parsing ในเวลาที่จำกัด (ตัวเลข 73–99% ข้างต้นจึงเป็น **ค่าประมาณ** ไม่ใช่ accuracy ของระบบสกัดฟิลด์ที่สมบูรณ์)
2. **ฟิลด์ตารางรายวิชา/เกรด/GPA ยังสกัดไม่ได้เลย** (`transcript_extraction.py` คืนค่าว่างสำหรับ `subject[]`) — เป็นสัดส่วนคะแนนที่ใหญ่ที่สุดของเกณฑ์ P1 (หัวข้อ 3 "ความแม่นยำ" 40 คะแนน) จึงเป็นจุดที่ต้องแก้ก่อนอื่น
3. **Ensemble ยังรวมผลแบบหยาบ** ทำให้ full-text CER สูงผิดปกติ ต้องปรับ logic ก่อนใช้เป็น engine หลัก
4. **โมเดลที่ทดสอบทั้งหมดเป็นโมเดลสำเร็จรูป (off-the-shelf)** ยังไม่ได้ fine-tune — สอดคล้องกับที่อาจารย์แจ้งว่าโมเดลทั่วไปจะไม่ถึง >91% ต้อง**เทรนเฉพาะทางเอง**

**แผนงานหลัง midterm เพื่อผลักดันให้เกิน 91%:**
1. เปลี่ยนวิธีสกัดฟิลด์จาก fuzzy text matching → ใช้ **bounding box จาก PaddleOCR** (มีอยู่แล้วใน `engines/paddle_engine.py`) ร่วมกับ layout ของตาราง (คอลัมน์ รหัสวิชา/ชื่อวิชา/หน่วยกิต/เกรด คงที่ตามเทมเพลต สจล.) เพื่อทำ field extraction แบบมีโครงสร้างจริง แทนที่ regex ล้วนของ week4
2. ขยายชุด augmented dataset จาก 288 → ตามเป้าหมายขั้นต่ำของฟอร์ม (≥450 ป.ตรี / ≥750 บัณฑิตศึกษา) ด้วย `build_dataset.py` เดิม (เพิ่มจำนวน variant/ภาพ)
3. **Fine-tune** โมเดล recognition (เช่น PaddleOCR recognition head หรือ TrOCR) บนชุด crop ข้อความจาก dataset ของทีมเอง โดยใช้ text layer ของ PDF ต้นฉบับ generate label อัตโนมัติ (ไม่ต้อง label มือ)
4. จำกัด vocabulary ของฟิลด์ `grade_earn` ให้อยู่ในชุดเกรดที่เป็นไปได้เท่านั้น (`a, b+, b, c+, c, d+, d, f, s, u, w, i, cr, t(...)` — ตรงกับ `GRADE_RE` ที่นิยามไว้แล้วใน `transcript_extraction.py`) เพื่อลด error
5. แก้ field วันที่ให้ parse รูปแบบไทย ("3 กันยายน 2542") ผ่าน `_parse_date()` ที่มีอยู่แล้วใน week4 (โค้ดรองรับแล้วแต่ยังไม่ได้ integrate เข้ากับ evaluation ของ week6) — คาดว่าจะแก้ปัญหา field `admis_date`/`date_of_birth` ที่ได้ 0% ในปัจจุบันได้ทันที
6. วัดผลใหม่ด้วย metric ที่ตรง requirement จริง: **Field-level exact match ต่อฟิลด์ที่สกัดได้แบบมีโครงสร้าง** (ไม่ใช่ fuzzy substring) ตามเกณฑ์ >91% / 80–90% / <80% ของวิชา

### 7.5 เกณฑ์การให้คะแนนตามความแม่นยำ (อ้างอิงเกณฑ์วิชา — สถานะปัจจุบัน)

| ช่วงความแม่นยำ (วิธี CV-OCR) | สถานะปัจจุบัน (fuzzy field matching, week6) | เป้าหมายหลัง midterm |
|---|---|---|
| มากกว่า 91% | field ข้อความล้วน (`student_id`, `program`, `degree`) เข้าเกณฑ์นี้แล้ว | ขยายให้ครอบคลุมฟิลด์ตารางรายวิชา/เกรด ด้วย fine-tuned model + structured extraction |
| 80% – 90% | — | — |
| น้อยกว่า 80% | field วันที่ (0%), ฟิลด์ตารางรายวิชา (ยังสกัดไม่ได้) | ต้องปรับปรุง pipeline ตามแผน 7.4 |

---

## 8. แผนแอปพลิเคชันและเอกสารประกอบ

> 🏷️ *หัวข้อนี้ในฟอร์มระบุว่า "เป็นส่วนหลัง midterm" — โค้ดที่มีอยู่แล้ว (`ocr_system` CLI จาก week3 + `transcript_extraction.py` จาก week4) จะถูกห่อเป็นเว็บแอปในขั้นตอนถัดไป*

**รูปแบบแอปพลิเคชันที่วางแผน**
- **Web app (Streamlit)** ครอบ CLI ที่มีอยู่แล้ว: อัปโหลดภาพ/PDF → เรียก `ocr_system.cli` (engine เลือกได้) → ส่งผลให้ `transcript_extraction.py` แปลงเป็น JSON โครงสร้าง → แสดงผลเทียบ ground truth (ถ้ามี) → บันทึกลง DB ตาม schema หัวข้อ 6
- แสดง **latency ต่อฉบับ** (มีข้อมูลจริงแล้วว่าเฉลี่ย ~1.5 วินาที/ภาพสำหรับ Tesseract — เร็วพอสำหรับ batch)

**เช็คลิสต์ส่งงาน**

- [ ] Push code ขึ้น GitHub (private/collaborate) และแชร์กับ `bhattarabhorn.wa@kmitl.ac.th`
- [ ] มี README (README ของ `ocr_system` และ `Lab5_transcript_dataset` มีอยู่แล้ว — รวมเป็น README เดียวของโปรเจกต์)
- [ ] URL folder All Dataset (เข้าถึงจำกัดตาม PDPA)
- [ ] มี Presentation/Slide หรือคู่มือการใช้งาน
- [ ] ส่งลิงก์ใน Discord กลุ่ม

---

## สรุปเกณฑ์การให้คะแนนโปรเจกต์นี้ (อ้างอิง) เทียบกับสถานะจริง

| องค์ประกอบ | คะแนนเต็ม | สถานะจากผลงาน Week 1–6 |
|---|---|---|
| 1. ออกแบบฐานข้อมูล / RAG | 15 | ออกแบบ schema แล้ว (หัวข้อ 6) ยังไม่ได้ implement จริง |
| 2. การอ่านภาพ: OCR / Keypoint, Skeleton | 35 | **ทำแล้ว** — pipeline 4 engine + preprocessing (deskew/CLAHE/denoise) ใช้งานได้จริง (week3) |
| 3. ความแม่นยำ / คุณภาพผลลัพธ์ | 40 | **วัดผลจริงบางส่วนแล้ว** (week6) — field ข้อความแม่นยำสูง แต่ตารางรายวิชา/เกรดยังต้องพัฒนาต่อ (แผนในหัวข้อ 7.4) |
| 4. LLM / Recommend | 0 | (ไม่มีในโปรเจกต์นี้) |
| 5. แอปใช้งานได้จริง + เอกสาร | 10 | ยังไม่ได้ห่อเป็นแอป — มี README/โค้ดของแต่ละ lab พร้อมนำมาประกอบ |
| **รวม** | **100 (+10 พิเศษ)** | Latency **ผ่านเกณฑ์พิเศษแล้วจริง** (~1.5s/ภาพ ≪ 30s) — multi-format (TH/EN, ป.ตรี/บัณฑิตศึกษา) รองรับแล้วในโครงสร้างโค้ด |
