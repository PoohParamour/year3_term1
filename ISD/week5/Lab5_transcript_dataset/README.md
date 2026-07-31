# Lab5 — Transcript Dataset (Augmentation & Labeling)

งานส่วน **Transcript Dataset** ของ Lab5 (ISD / Chapter 5) — augment + label ชุดรูป transcript
แล้วเตรียมเป็นโฟลเดอร์พร้อมอัปโหลดเป็น link จำกัดสิทธิ์

## ที่มาของข้อมูล (อ่านอย่างเดียว ไม่แก้ต้นฉบับ)
| กลุ่ม | รูปต้นฉบับ (PDF) | Ground truth |
|---|---|---|
| `th` | `week3/.../data/input/input` (24) | `week3/ground_truth_transcript 2/ground_truth` (24) |
| `G`  | `week3/.../data/input/input_G` (24) | `week3/ground_truth_transcript 2/ground_truth_G` (24) |

## โครงสร้างโฟลเดอร์
```
Lab5_transcript_dataset/
├── README.md
├── build_dataset.py            ← สคริปต์ที่ใช้สร้างชุดข้อมูล (รันซ้ำได้)
├── images/
│   ├── original/<group>/<id>.png          ← เรนเดอร์จาก PDF (48 รูป)
│   └── augmented/<group>/<id>_aug{1..5}_<type>.png  ← variant (240 รูป)
├── ground_truth/<group>/Json_<id>_*.json  ← label จริง (คัดลอกมา, 47 ไฟล์)
└── labels/
    └── manifest.csv            ← ตารางจับคู่ รูป ↔ รหัส นศ. ↔ ground truth
```

## ชนิดของ Augmentation (5 แบบ/ใบ) จำลองสภาพจริงของการสแกน/ถ่ายรูป
| # | aug_type | จำลองสถานการณ์ |
|---|---|---|
| 1 | `rotate_bright` | วางเอียง ±3° + สแกนสว่างเกิน |
| 2 | `noise` | เม็ด noise จากเซนเซอร์/เครื่องถ่ายเอกสาร |
| 3 | `blur_contrast` | โฟกัสหลุด + คอนทราสต์สูง |
| 4 | `perspective` | ถ่ายจากมุมเอียง (keystone) |
| 5 | `jpeg_dark` | ภาพถ่ายมือถือคุณภาพต่ำ + มืด |

> การสุ่มใช้ seed อิงจากรหัส นศ. + เลข variant → **รันซ้ำได้ผลเหมือนเดิม (reproducible)**

## manifest.csv — คอลัมน์
| คอลัมน์ | ความหมาย |
|---|---|
| `image_path` | พาธรูป (relative จากโฟลเดอร์นี้) |
| `split` | `original` หรือ `augmented` |
| `group` | `th` หรือ `G` |
| `student_id` | รหัสนักศึกษา (คีย์เชื่อมกับ ground truth) |
| `aug_type` | ชนิด augmentation (`none` = ต้นฉบับ) |
| `gt_path` | พาธไฟล์ ground truth JSON |
| `gt_exists` | มี ground truth หรือไม่ |

## สถิติ
- ต้นฉบับ: **48** รูป | augmented: **240** รูป | **รวม 288 รูป**
- Ground truth ที่ label ได้: 47/48 (ขาด 1 ราย)
- ขนาดรวม ~341 MB (PNG, 150 DPI)


2. **การอัปโหลดขึ้น link folder ที่จำกัดสิทธิ์** (Google Drive/อื่น ๆ) และแชร์ให้กลุ่ม+อาจารย์ — ต้องทำเอง (นอกขอบเขตที่ผมทำให้ได้)

## รันสร้างใหม่
```bash
python3 build_dataset.py
```
