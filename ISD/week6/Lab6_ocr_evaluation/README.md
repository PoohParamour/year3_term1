# Lab6 — OCR Evaluation: Field / Page / Category Level

## Scope
- OCR engine: **Tesseract** (`tha+eng`)
- รูปที่ใช้: **282/288 รูป** ที่มี ground truth คู่ (47 original + 235 augmented — ข้าม 6 รูปของรหัส `74176008` ที่ไม่มี ground truth)


### Field Level (ความแม่นยำรายฟิลด์)
| field | accuracy | หมายเหตุ |
|---|---|---|
| student_id | 99.6% | แม่นสุด — เป็นตัวเลขล้วน regex-friendly |
| program, degree, prename | ~98% | ข้อความภาษาไทยไม่มีช่องว่าง OCR อ่านได้ดี |
| faculty_name, name | ~96-97% | |
| **admis_date, date_of_birth** | **0%** | เอกสารพิมพ์วันที่แบบไทย ("3 กันยายน 2542") แต่ ground truth เป็น ISO ("1999-09-03") — **รูปแบบต่างกันโดยธรรมชาติ ไม่ใช่ OCR ผิด** |

### Page Level (ความแม่นยำทั้งหน้า)
- CER/WER สูงกว่า 1 ปกติ เพราะ reference (header เท่านั้น) สั้นกว่า OCR text ทั้งหน้ามาก (รวมตารางผลการเรียน) — ตรงกับ convention เดิมที่ `week3/Lab3_ocr_system` ใช้อยู่แล้ว (ดู `evaluation_cli_demo.json` เดิมที่ cer=1.95)
- **augmented เฉลี่ยดีกว่า original เล็กน้อย** (CER 5.53 vs 5.79) — ผิดจากที่คาดไว้ตอนแรก
- แยกตาม aug_type: `blur_contrast` แม่นที่สุด (CER 4.49), `jpeg_dark` แย่ที่สุด (CER 5.90)

### Category Level (ป.ตรี vs บัณฑิตศึกษา)
| group | field accuracy | page CER | page WER |
|---|---|---|---|
| `th` (ป.ตรี) | 73.7% | 6.83 | 89.0 |
| `G` (บัณฑิตศึกษา: ป.โท+ป.เอก) | 73.4% | 4.27 | 50.1 |

Field-level accuracy ใกล้เคียงกัน แต่ page-level ของกลุ่มบัณฑิตศึกษาดีกว่าชัดเจน (อาจเพราะเอกสารสั้นกว่า/รายวิชาน้อยกว่า)

## ข้อจำกัดของวิธีวัด 
**Field Level ไม่ได้ทำ structured extraction จริง** — เพราะ OCR คืนข้อความดิบไม่มีโครงสร้าง (ไม่มี bounding
box/layout parsing ในเวลาที่จำกัด) จึงใช้ **fuzzy substring matching**: เลื่อนหน้าต่างความยาวเท่ากับค่า
ground truth ไปทาบกับข้อความ OCR ทั้งหมด หาตำแหน่งที่ CER ต่ำสุด ถือว่า field ถูกต้องเมื่อ CER ≤ 0.2
เป็นค่าประมาณความแม่นยำ ไม่ใช่ field extractor ที่สมบูรณ์แบบ production
