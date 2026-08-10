# ใบเสนอโครงการ (Project Proposal)
## โปรเจกต์ที่ 1: OCR Transcript (สจล.)

**วิชา 06026240 Intelligent System Development**

| กลุ่ม / Section | สมาชิกในทีม (3 คน) |
|---|---|
| _______________ | 1. ____________________ (รหัส __________) |
|  | 2. ____________________ (รหัส __________) |
|  | 3. ____________________ (รหัส __________) |

> *เป้าหมายคะแนน: เต็ม 100 (DB 15 · OCR/Keypoint/Skeleton 35 · ความแม่นยำ 40 · แอป+เอกสาร 10) + คะแนนพิเศษ Challenge สูงสุด +10*

---

## ⚠️ ความปลอดภัยของข้อมูลและการปฏิบัติตาม PDPA

Transcript (โดยเฉพาะภาพ Real) มีชื่อ-นามสกุล รหัสนักศึกษา ผลการเรียน และ GPA ซึ่งเป็น **"ข้อมูลส่วนบุคคล"** และผลการเรียนถือเป็นข้อมูลที่มีความอ่อนไหวสูงตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล (PDPA) ทีมได้เซ็นแบบฟอร์ม **PDPA Consent** ของรายวิชาเป็นลายลักษณ์อักษรก่อนเก็บ/ใช้ข้อมูลทุกฉบับ และนำข้อมูลไปใช้เพื่อวัตถุประสงค์การเรียนการสอนในรายวิชานี้เท่านั้น

**Checklist มาตรการที่ทีมต้องปฏิบัติ** (ทุกคนในทีมทำตามอย่างเคร่งครัดทุกครั้ง)

- [x] ใช้ Transcript จริงเฉพาะฉบับที่ได้รับความยินยอมเป็นลายลักษณ์อักษรจากเจ้าของข้อมูลแล้วเท่านั้น
- [x] เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth โดยจำกัดสิทธิ์การเข้าถึง (access control) เฉพาะสมาชิกทีมและอาจารย์ผู้สอน
- [x] เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ในคอมพิวเตอร์ส่วนตัวที่ใส่รหัสผ่านที่ไม่ได้บอกใคร
- [x] ไม่เก็บไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ในคอมพิวเตอร์ที่มีบุคคลอื่นใช้
- [x] ห้าม upload ไฟล์ Transcript (Real หรือ Synthetic) รวมถึง ground truth ขึ้น public GitHub repository
- [x] Anonymize/มาสก์ข้อมูลอ่อนไหว (ชื่อ, รหัสนักศึกษา, เกรดรายวิชา) ก่อนนำไปใส่ใน slide/รายงาน/README ที่เผยแพร่ต่อบุคคลอื่น
- [x] ไม่นำข้อมูลไปใช้เพื่อวัตถุประสงค์อื่นนอกเหนือจากการเรียนการสอนในรายวิชานี้

**มาตรการเพิ่มเติมที่ทีมจะดำเนินการเพื่อคุ้มครองข้อมูล**

1. จำกัดสิทธิ์เข้าถึงโฟลเดอร์ `/dataset/` และ `/ground_truth/` ด้วยการเข้ารหัส (encrypted volume / password-protected archive) เปิดได้เฉพาะสมาชิกทีม 3 คน
2. เก็บ dataset และ ground truth ไว้ใน **private repository / private cloud storage** เท่านั้น และตั้ง `.gitignore` ครอบคลุมโฟลเดอร์ข้อมูลจริงทั้งหมด กันการ push ขึ้น public โดยไม่ตั้งใจ
3. **ประมวลผล OCR แบบ on-premise / local ทั้งหมด** (ไม่ส่งภาพ Transcript ออกไปยัง cloud API ภายนอก) เพื่อลดความเสี่ยงข้อมูลรั่ว — เป็นเหตุผลหลักที่เลือกใช้โมเดล open-source ที่รันเองได้ (ดูหัวข้อ 5)
4. ลบไฟล์ Transcript และ ground truth ทั้งหมดออกจากเครื่องพัฒนาและ cloud storage **ภายใน 7 วันหลังประกาศเกรดรายวิชา**
5. ในสไลด์/รายงาน/README ใช้เฉพาะภาพ **Synthetic ที่เบลอ/มาสก์ข้อมูล** ทั้งหมด ไม่แสดงภาพ Real และไม่แสดงชื่อ-รหัส นศ. จริง

---

## 1. ภาพรวมโปรเจกต์ (Overview)

ทีมพัฒนาระบบอ่าน Transcript ของ สจล. แบบอัตโนมัติ (OCR) ที่รับภาพ/PDF ใบแสดงผลการเรียนทั้งระดับ **ปริญญาตรีและบัณฑิตศึกษา** ทั้งฉบับ **ภาษาไทยและภาษาอังกฤษ** แล้วดึงข้อมูลออกมาให้ครบทุกฟิลด์ ได้แก่ ข้อมูลนักศึกษา/ปริญญา, รายวิชา (รหัสวิชา ชื่อวิชา หน่วยกิต เกรด), GPA/GPS รายภาคและสะสม โดยใช้ **Computer Vision หา keypoint 4 มุมและโครงเส้นตาราง (skeleton)** ร่วมกับ **โมเดล recognition ที่ fine-tune เองบนฟอนต์และเลย์เอาต์ของ สจล.** ผลลัพธ์ถูกจัดเป็น JSON ตามสคีมาเดียวกับ ground truth แล้ว **บันทึกลงฐานข้อมูลเชิงสัมพันธ์** เพื่อให้ค้นคืน (query) และตรวจสอบย้อนหลังได้ โดยระบบต้องทนต่อภาพที่มี noise (เอียง เงา แสงไม่สม่ำเสมอ ถ่ายจากมือถือ) และวัดผลความแม่นยำเทียบ ground truth ได้เป็นตัวเลข

---

## 2. ข้อมูล (Dataset) และ Ground Truth

ข้อมูลจริงที่ได้รับ: **PDF ต้นฉบับ 48 ไฟล์** (ป.ตรี 24 + บัณฑิตศึกษา 24) แต่ละไฟล์มี ground truth เป็น JSON ครบ 1:1 รวม 48 ไฟล์ แบ่งเป็นภาษาไทย 24 / อังกฤษ 24 ทีมนำต้นฉบับเหล่านี้เป็น "Synthetic" แล้วสร้างชุด "Synthetic & noise" ด้วย augmentation เอง และจัดหา "Real" 1 ฉบับจากสมาชิกในทีม (มี consent)

| ประเภทข้อมูล | แหล่งที่มา | จำนวน (ไฟล์/ภาพ) | Ground Truth มาจากไฟล์ใด (format + ตำแหน่งเก็บ) |
|---|---|---|---|
| **Synthetic** | PDF เทมเพลต Transcript สจล. ที่อาจารย์ให้ (ป.ตรี `input_Bachelor_Degrees/` 24, บัณฑิตศึกษา `input_Master/` 24) เรนเดอร์เป็นภาพ | 48 ต้นฉบับ (TH 24 / EN 24) | `Json_<student_id>_<th\|en>.json` 1 ไฟล์ต่อ 1 ฉบับ ที่ `ground_truth_transcript/` — ฟิลด์ `header_detail`, `transcript_detail.semesters[].subject[]`, `footer_detail` |
| **Synthetic & noise** | นำต้นฉบับ Synthetic มาทำ Data Augmentation (blur/skew/แสง/perspective/เงา — ดูหัวข้อ 3) | ≥ 1,224 ภาพ (ป.ตรี ≥456 + บัณฑิต ≥768) | ใช้ JSON เดิมของภาพต้นฉบับ (augmentation ไม่เปลี่ยนค่าฟิลด์ข้อความ; ใช้ Albumentations `ReplayCompose` เพื่อคง bbox/keypoint ให้ตรง GT) |
| **Real** | Transcript ตัวอย่างจริงของสมาชิกในทีม (ผ่าน PDPA consent + มาสก์ก่อนเผยแพร่) | 1 ฉบับ | Label ด้วยมือ 1 ไฟล์ `Json_real_01.json` สคีมาเดียวกับ Synthetic ที่ `ground_truth_transcript/real/` (เก็บ private) |

**เช็คความครบถ้วนของข้อมูล**

- [x] Synthetic
- [x] Synthetic & noise
- [x] Real
- [x] Ground truth ครบทุกภาพ — รวม **≈ 1,273 ภาพ** (ต้นฉบับ 48 + augmented ≥1,224 + Real 1)
- [x] แบ่ง **train ≈ 891 ภาพ (70%) / val ≈ 191 ภาพ (15%) / test ≈ 191 ภาพ (15%)** เรียบร้อยแล้ว
      *(หมายเหตุ: split ตาม "ต้นฉบับ" ก่อน แล้วให้ภาพ augment ของต้นฉบับเดียวกันอยู่ set เดียวกัน เพื่อกัน data leakage; ภาพ Real ทั้งหมดอยู่ใน test)*

---

## 3. Data Augmentation

จำลองสภาพเอกสารที่หลากหลาย เพื่อให้โมเดล OCR ทนต่อคุณภาพภาพที่แตกต่างกัน (สแกนเอียง แสงไม่สม่ำเสมอ กระดาษยับ ถ่ายจากมือถือ) — ใช้ **Albumentations `ReplayCompose`** เพื่อให้ transform เชิงเรขาคณิตกระทำกับ keypoint/bbox ของ ground truth อย่างสอดคล้องกัน

| รูปแบบ Augmentation | พารามิเตอร์ที่ใช้ | เหตุผลที่เลือกใช้ |
|---|---|---|
| Rotate / Skew | ±5° | จำลองการวางเอกสารเอียงตอนสแกน |
| Perspective warp | scale 0.02–0.05 | จำลองถ่ายด้วยมือถือไม่ตรงมุม (ป.บัณฑิตใช้ระดับสูงขึ้น) |
| Gaussian noise | σ = 0.01–0.03 | จำลองสแกนเนอร์คุณภาพต่ำ / ISO สูง |
| Brightness / Contrast | ±20% | จำลองแสงถ่ายภาพ/สแกนไม่สม่ำเสมอ |
| Random shadow / gradient illumination | 1–2 เงา, ความเข้ม 0.3–0.6 | จำลองเงามือ/แสงไฟตอนถ่ายด้วยมือถือ |
| Gaussian / Motion blur | kernel 3–5 px | จำลองภาพหลุดโฟกัส/มือสั่น |
| JPEG compression | quality 40–70 | จำลองไฟล์ที่ถูกบีบอัด/ส่งต่อหลายรอบ |
| Paper texture + fold lines (ขั้นสูง) | รอยพับ 1–2 เส้น + noise พื้นผิว | จำลองกระดาษยับ/รอยพับ (ใช้กับชุด ป.บัณฑิต) |

**เป้าหมายจำนวนข้อมูลขั้นต่ำ (แยกตามระดับการศึกษา)**

| ระดับการศึกษา | ภาพต้นฉบับ | Augmented ต่อภาพ | จำนวนที่ทีมทำ |
|---|---|---|---|
| ป.ตรี | 24 ภาพ | ×19 เท่า | **456 ภาพ** (รวมต้นฉบับ ≥ 450) |
| ป.บัณฑิต | 24 ภาพ | ×32 เท่า + augmentation ขั้นสูง (perspective warp / รอยพับ) | **768 ภาพ** (รวมต้นฉบับ ≥ 750) |

---

## 4. การ Labeling / Annotation

**ฟิลด์ที่ label ในแต่ละภาพ Transcript** (สคีมาเดียวกับ ground truth ที่อาจารย์ให้)

- **Header:** `student_id`, `prename`, `name`, `faculty_name`, `degree`, `program`, `major`, `honor`, `date_of_birth`, `admis_date`, `grad_date`, `grad_reason`, `uni_name`, `uni_address`
- **รายวิชา (ต่อ subject):** `subject_id`, `subject_name`, `type` (เช่น `cr` สำหรับบัณฑิตศึกษา), `credit`, `grade_earn`
- **ต่อภาคการศึกษา:** `year`, `sem_num`, `GPA`, `GPS`, `pass_reason`
- **สรุป:** `total_credits_earned`, `cumulative_gpa`, และ (บัณฑิตศึกษา) `master_comprehensive`, `master_thesis`, `master_qualify`
- **Footer:** `by_signature`, `by_position`, `by_reg`, `updated_at`
- **Keypoint / bounding box:** จุด 4 มุมของกรอบตาราง (keypoint), bbox ของบล็อกตาราง, และตำแหน่งลายเซ็น/ตราประทับ

**เครื่องมือและ Format ที่ใช้ labeling**

- **Ground truth ข้อความ:** ใช้ JSON ที่อาจารย์ให้เป็นหลัก และเนื่องจากต้นฉบับเป็น PDF ที่มี text layer เราสามารถ **ดึงตำแหน่งตัวอักษรจาก PDF โดยอัตโนมัติ** (เช่น `pdfplumber`) เพื่อสร้าง label ระดับ crop สำหรับเทรน recognition โดยไม่ต้อง label ข้อความด้วยมือ → ขยายชุดเทรนได้ไม่จำกัด
- **Keypoint/bbox เพิ่มเติม:** ใช้ **Label Studio** (bounding box + keypoint) สำหรับภาพ Real และ subset ที่ใช้ตรวจ layout → export เป็น **COCO-JSON** แล้วเขียนสคริปต์แปลงเป็น `ground_truth.json` สคีมาของโปรเจกต์

---

## 5. แนวทางการอ่านภาพ (OCR)

**สถาปัตยกรรมแบบ 2 สเตจ + fine-tune โมเดลเอง** (open-source ทั้งหมด รันบนเครื่องเอง — สอดคล้อง PDPA และทำให้ผลักความแม่นยำเกิน 91% ได้ตามที่อาจารย์แนะนำ)

**Stage 0 — Preprocessing:** แปลง PDF→ภาพที่ DPI คงที่, แปลง grayscale, adaptive threshold / denoise

**Stage 1 — Keypoint & Skeleton (Computer Vision):**
- ใช้ **OpenCV** ตรวจเส้นตาราง (Hough Line / morphological line extraction) เพื่อหา **keypoint 4 มุมของกรอบตาราง** → ทำ **perspective correction / deskew**
- สกัด **skeleton ของเส้นตาราง** (เส้นแนวนอน + แนวตั้ง) → reconstruct cell แล้ว map เข้าคอลัมน์ (`subject_id | subject_name | type | credit | grade`) เพราะเลย์เอาต์ สจล. เป็นเทมเพลตคงที่ (รองรับทั้งเลย์เอาต์ ป.ตรี 4 คอลัมน์ และ ป.โท 5 คอลัมน์ที่มีคอลัมน์ `ประเภท`)

**Stage 2 — Recognition (โมเดลที่ fine-tune เอง):**
- Baseline เปรียบเทียบ: **PaddleOCR / Tesseract** (Thai + Eng)
- โมเดลหลัก: **fine-tune recognizer** (เช่น **TrOCR** หรือ **PaddleOCR recognition** ที่มี Thai dictionary) บนชุด crop ที่ generate อัตโนมัติจาก text layer ของ PDF + augmentation → โมเดลเรียนรู้ฟอนต์/สไตล์เฉพาะของ Transcript สจล.
- แยกหัวการอ่านตามชนิดฟิลด์: ฟิลด์ตัวเลข (`credit`, `GPA`, `GPS`) และ `grade_earn` ใช้ **constrained vocabulary** (เช่น เกรดจำกัดชุด `a, b+, b, c+, c, d+, d, f, s, u, w, cr, i, ...`) เพื่อลด error

**Stage 3 — Post-processing & validation:** ตรวจ regex ของ GPA/หน่วยกิต, บังคับให้ `grade_earn` อยู่ในชุดที่ถูกต้อง, ตรวจ cross-check ผลรวมหน่วยกิต แล้วประกอบผลลัพธ์เป็น JSON สคีมาเดียวกับ ground truth เพื่อบันทึกลงฐานข้อมูล

**เหตุผลที่เลือก open-source + fine-tune เอง (ได้คะแนนเต็มตามเกณฑ์ P1):**
1. **ฟรี รันบนเครื่องเอง** → ไม่มีค่าใช้จ่ายต่อฉบับ และภาพไม่ต้องออกนอกเครื่อง (PDPA)
2. **เทรนเองบนโดเมนเฉพาะ** → เกินเกณฑ์ 91% ได้จริง (โมเดลสำเร็จรูปทั่วไปมักไม่ถึง)
3. **เร็ว** → รองรับ latency < 30 วินาที/ฉบับ และ batch ได้ (ดู Challenge)

---

## 6. ออกแบบฐานข้อมูล (Database Design)

> 🏷️ *หัวข้อนี้ในฟอร์มระบุว่า "เป็นส่วนหลัง midterm" — ใส่ไว้ให้ครบเผื่อเก็บ/ตัดตอนส่งจริง*

Schema เชิงสัมพันธ์ (≥3 ตาราง) รองรับการ query ข้อมูลนักศึกษา/รายวิชา/เกรดได้จริง — normalize จากสคีมา JSON

| ชื่อตาราง | ฟิลด์หลัก | Primary / Foreign Key | คำอธิบายความสัมพันธ์ |
|---|---|---|---|
| `students` | `student_id`, `prename`, `name`, `faculty_name`, `degree`, `program`, `major`, `honor`, `date_of_birth`, `admis_date`, `grad_date`, `cumulative_gpa`, `total_credits_earned` | `student_id` **PK** | 1 นักศึกษามีได้หลายภาคเรียน (1:N) |
| `semesters` | `semester_id`, `student_id`, `year`, `sem_num`, `GPA`, `GPS` | `semester_id` **PK**, `student_id` **FK → students** | 1 ภาคเรียนมีได้หลายรายวิชาที่ลง (1:N) |
| `subjects` | `subject_id`, `subject_name`, `credit`, `type` | `subject_id` **PK** | 1 รายวิชาถูกลงทะเบียนได้โดยหลายนักศึกษา (1:N ผ่าน enrollments) |
| `enrollments` | `enrollment_id`, `semester_id`, `subject_id`, `grade_earn` | `enrollment_id` **PK**, `semester_id` **FK → semesters**, `subject_id` **FK → subjects** | ตารางเชื่อม (junction) ระหว่างภาคเรียนกับรายวิชา — เก็บเกรดที่ได้จริงต่อ 1 การลงทะเบียน |

**ตัวอย่าง query ที่รองรับ:** ดึง transcript เต็มของ นศ. 1 คน (join 4 ตาราง), หา นศ. ที่ได้ F ในวิชาหนึ่ง, คำนวณ/ตรวจสอบ GPA สะสม, สรุปหน่วยกิตสะสมต่อคน

---

## 7. การประเมินความแม่นยำ (Evaluation Plan)

**Metric ที่ใช้วัดความแม่นยำระดับ Field-level**

- **Field-level accuracy** — เทียบ field ต่อ field กับ ground truth (metric หลัก)
- **Exact-match** สำหรับฟิลด์ที่มีค่าแน่นอน: `student_id`, `subject_id`, `credit`, `grade_earn`, `GPA`, `GPS`
- **Character Error Rate (CER)** สำหรับข้อความอิสระ: `name`, `subject_name`
- **Document-level exact match** — ทั้งฉบับถูกครบทุกฟิลด์ (%)
- **Table structure accuracy** — จำนวนแถว/เซลล์ที่ตรวจได้ถูกต้อง (กันแถวหาย/เกิน)
- **Latency** — เวลาเฉลี่ยต่อฉบับ (รวมเวลาเทียบความเหมือนกับ GT) — เป้าหมาย < 30 วินาที
- รายงานแยก **ป.ตรี vs บัณฑิตศึกษา** และ **ไทย vs อังกฤษ** เพื่อดูจุดอ่อนของแต่ละเวอร์ชัน

**เกณฑ์การให้คะแนนตามความแมนยำ (อ้างอิงเกณฑ์วิชา)**

| ช่วงความแม่นยำ (วิธี CV-OCR) | คะแนนที่ได้ | จำนวนภาพ (test) | หมายเหตุ |
|---|---|---|---|
| **มากกว่า 91%** | เต็ม | ตั้งเป้าให้ครอบคลุม test set (~191 ภาพ) | **เป้าหมายที่ทีมตั้งไว้** — บรรลุด้วยการ fine-tune โมเดลเอง |
| 80% – 90% | ~2/3 | — | ยอมรับได้ในช่วงพัฒนา |
| น้อยกว่า 80% | ~1/3 | — | ต้องปรับปรุง pipeline เพิ่มเติม (preprocessing / เพิ่ม augment / เทรนต่อ) |

---

## 8. แผนแอปพลิเคชันและเอกสารประกอบ

> 🏷️ *หัวข้อนี้ในฟอร์มระบุว่า "เป็นส่วนหลัง midterm" — ใส่ไว้ให้ครบเผื่อเก็บ/ตัดตอนส่งจริง · เกี่ยวข้องกับเกณฑ์ #5 แอปใช้งานได้จริง + เอกสาร 10 คะแนน*

**รูปแบบแอปพลิเคชันและแผน Deploy/Demo**

- **Web app (Streamlit)**: อัปโหลดภาพ/PDF Transcript → แสดง keypoint/ตารางที่ตรวจได้ → แสดงผล OCR เทียบ ground truth (ถ้ามี) → บันทึกลงฐานข้อมูล → query กลับมาแสดงได้ พร้อม **demo end-to-end**
- แสดง **latency ต่อฉบับ** และรองรับ **batch** หลายไฟล์ (ตอบโจทย์ Challenge)

**เช็คลิสต์ส่งงาน**

- [ ] Push code ขึ้น GitHub (private/collaborate) และแชร์กับ `bhattarabhorn.wa@kmitl.ac.th`
- [ ] มี README (วิธีติดตั้ง/รัน/สคีมา/ผลการวัด)
- [ ] URL folder All Dataset (เข้าถึงจำกัดตาม PDPA)
- [ ] มี Presentation/Slide หรือคู่มือการใช้งาน
- [ ] ส่งลิงก์ใน Discord กลุ่ม

---

## 🌟 คะแนนพิเศษ (Challenge — P1) ที่ทีมตั้งเป้า

| เกณฑ์ Challenge | คะแนนพิเศษ | ทีมทำอย่างไร |
|---|---|---|
| ความแม่นยำบนภาพสถานการณ์จริง (ป.ตรี + บัณฑิตศึกษา) | +0 (นับรวมในเกณฑ์หลัก) | ทดสอบบนชุด augment ที่จำลองภาพเอียง/เงา/ลายน้ำ/ถ่ายมือถือ |
| **รองรับหลายเวอร์ชัน/ฟอร์แมต (≥2 แบบ)** | **+10** | รองรับทั้ง **ไทย/อังกฤษ** และ **ป.ตรี (4 คอลัมน์)/บัณฑิตศึกษา (5 คอลัมน์ มี `ประเภท`)** โดยไม่ต้องแก้โค้ด |
| **ความเร็ว (Latency) เฉลี่ย < 30 วินาที/ฉบับ** (รวมเปรียบเทียบความเหมือน) | **+10** | โมเดลรัน local + batch processing |

> *นับคะแนนความแม่นยำสูงสุดเพียงระดับเดียว · รวมคะแนนพิเศษสูงสุด +10 คะแนน*

---

## สรุปเกณฑ์การให้คะแนนโปรเจกต์นี้ (อ้างอิง)

| องค์ประกอบ | คะแนนเต็ม | สัมพันธ์กับหัวข้อในใบเสนอโครงการ |
|---|---|---|
| 1. ออกแบบฐานข้อมูล / RAG | 15 | หัวข้อ 6 |
| 2. การอ่านภาพ: OCR / Keypoint, Skeleton | 35 | หัวข้อ 5 |
| 3. ความแม่นยำ / คุณภาพผลลัพธ์ | 40 | หัวข้อ 7 |
| 4. LLM / Recommend | 0 | (ไม่มีในโปรเจกต์นี้) |
| 5. แอปใช้งานได้จริง + เอกสาร | 10 | หัวข้อ 8 |
| **รวม** | **100 (+10 พิเศษ)** | |
