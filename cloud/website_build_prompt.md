# Prompt: สร้างเว็บ Mock Exam — AWS Academy Cloud Foundations (ภาษาไทย)

คัดลอกข้อความด้านล่างทั้งหมดไปวางใน AI builder (เช่น Claude Code, v0, Cursor ฯลฯ) พร้อมแนบไฟล์ `questions.json` ที่แนบมาด้วย

---

## บทบาทและเป้าหมาย

คุณคือ frontend engineer ให้สร้างเว็บแอป **Mock Exam** สำหรับฝึกทำข้อสอบ AWS Academy Cloud Foundations เป็นภาษาไทย โดยใช้ข้อมูลคำถามจากไฟล์ `questions.json` ที่แนบมา (มีทั้งหมด 120 ข้อ)

## Tech Stack (บังคับ)

- **React** (Next.js App Router หรือ Vite ก็ได้ — เลือกที่เหมาะกับ setup)
- **Tailwind CSS**
- **shadcn/ui** — ใช้ component: `Card`, `RadioGroup`, `Checkbox`, `Button`, `Progress`, `Badge`, `Separator`, `Dialog`/`AlertDialog` (สำหรับสรุปผลตอนจบ)
- **animata.design** — ใช้ animation component ของ animata (เช่น transition ตอนเปลี่ยนคำถาม, effect ตอนเฉลยถูก/ผิด, progress bar แบบ animated) เพื่อให้ UI ดูมีชีวิตชีวา ไม่ static จนเกินไป

## โครงสร้างข้อมูล (`questions.json`)

ไฟล์เป็น array ของ object โครงสร้างดังนี้:

```json
{
  "id": 1,
  "module": "Module 1",
  "isNew": false,
  "type": "single",     // "single" | "multiple" | "boolean"
  "question": "ข้อความคำถาม...",
  "options": [
    { "text": "ตัวเลือก A", "correct": false },
    { "text": "ตัวเลือก B", "correct": true }
  ]
}
```

- `type: "single"` → เลือกได้คำตอบเดียว (ใช้ `RadioGroup` / radio button)
- `type: "multiple"` → เลือกได้มากกว่า 1 ข้อ (ใช้ `Checkbox`) — โจทย์จะบอกจำนวนที่ต้องเลือกไว้ในข้อความคำถาม (เช่น "เลือก 2 ข้อ", "เลือก 3 ข้อ")
- `type: "boolean"` → ถูก/ผิด (แสดงเป็นปุ่ม 2 ตัวเลือกหรือ radio ก็ได้ ไม่ต้อง treat ต่างจาก single มากนัก)
- `module` มีไว้เผื่อใช้ tag/badge แสดงว่าข้อนี้มาจาก module ไหน (ไม่ต้องใช้ filter/แยกหน้า — ดูหัวข้อ flow ด้านล่าง)
- `isNew` เป็น flag ภายใน ไม่ต้องแสดงผลให้ผู้ใช้เห็น

## Flow ของเว็บ (สำคัญ)

1. **ไม่มีหน้าเลือก Module** — เข้าเว็บมาแล้วเจอข้อสอบทันที
2. **รวมข้อสอบทั้งหมด 120 ข้อไว้ด้วยกันเป็นชุดเดียว** ไม่แยกตาม Module
3. แสดงคำถามทีละข้อ (one question at a time) พร้อม progress bar/indicator บอกว่าอยู่ข้อที่เท่าไหร่จากทั้งหมด (เช่น "ข้อ 12 / 120") — ใช้ `Progress` component ของ shadcn ผสาน animation ของ animata
4. มีปุ่ม "ข้อถัดไป" (และ "ข้อก่อนหน้า" ถ้าทำได้) และปุ่ม "ส่งคำตอบ/ดูเฉลย" ในข้อนั้นๆ ก่อนไปข้อถัดไป (ให้ feedback ทันทีว่าตอบถูกหรือผิด พร้อม highlight ตัวเลือกที่ถูกต้อง)
5. เมื่อทำครบทุกข้อ ให้แสดงหน้าสรุปผล: คะแนนรวม, จำนวนข้อที่ตอบถูก/ผิด, และปุ่ม "เริ่มทำใหม่"
6. ควรมีตัวเลือกให้สุ่มลำดับคำถามทั้งชุดตอนเริ่ม exam ด้วย (random order ของคำถามเอง) — ทำเป็นค่า default เปิดไว้เลยก็ได้ เพราะจะช่วยให้ฝึกได้หลากหลายขึ้น

## ⭐ Requirement สำคัญที่สุด: สุ่มตำแหน่งตัวเลือกคำตอบ

**ทุกครั้งที่คำถามถูกแสดงผล (render) ตัวเลือกคำตอบ (`options`) ต้องถูกสุ่มลำดับใหม่ (shuffle)** ห้ามให้คำตอบที่ถูกอยู่ตำแหน่งเดิมซ้ำๆ (เช่น อยู่ข้อ A ตลอด) เพื่อไม่ให้ผู้ใช้จำตำแหน่งแทนที่จะจำเนื้อหา

ข้อกำหนดเพิ่มเติม:
- shuffle ต้องเกิดขึ้น **ต่อการแสดงผลคำถามแต่ละครั้ง** (เช่น ถ้าย้อนกลับมาทำข้อเดิมซ้ำ หรือเริ่ม exam ใหม่ ลำดับต้องสุ่มใหม่อีกครั้ง ไม่ใช่ fix ไว้ตอน build)
- ใช้ Fisher-Yates shuffle algorithm หรือเทียบเท่า ให้กระจายแบบสุ่มจริง ไม่ bias
- การ track ว่าผู้ใช้เลือกอะไร ต้อง reference จาก `option.text` หรือ id ที่ผูกกับ option นั้นๆ ไม่ใช่ index เดิมก่อน shuffle เพื่อไม่ให้ตรวจคำตอบผิดพลาด
- แนะนำ implementation: shuffle ที่ระดับ component/state ตอน mount คำถามนั้นๆ (เช่น `useMemo` ที่ผูกกับ question id) ไม่ shuffle ทุก re-render จนตัวเลือกขยับไปมาเวลาผู้ใช้กำลังเลือกอยู่

## UI/UX เพิ่มเติม

- ใช้ธีมสีที่ดูเป็นมิตรกับการอ่านภาษาไทยเป็นเวลานาน (ฟอนต์ที่รองรับไทยชัดเจน เช่น Noto Sans Thai หรือ IBM Plex Sans Thai)
- Card คำถามควรมี animation transition (fade/slide) เวลาเปลี่ยนข้อ (ใช้ animata)
- เมื่อเฉลย: ตัวเลือกที่ถูกต้อง highlight เป็นสีเขียว, ตัวเลือกที่ผู้ใช้เลือกผิด highlight สีแดง, ใช้ animata effect เล็กน้อยตอนแสดงผลถูก/ผิด (เช่น shake หรือ pulse)
- Responsive รองรับมือถือเป็นหลัก เพราะน่าจะใช้ทบทวนระหว่างเดินทาง

## สิ่งที่ไม่ต้องทำ

- ไม่ต้องมีระบบ login/บัญชีผู้ใช้
- ไม่ต้องมี backend/database แยก — เก็บ progress ไว้ใน local state/localStorage พอ
- ไม่ต้องมีหน้าเลือก module หรือ filter ตาม module

---

**ไฟล์ข้อมูลที่ต้องแนบคู่กับ prompt นี้:** `questions.json`

z3KJDSo3uvKu40ID