# 📝 Homework 2: DBSCAN Manual Calculation

**Instructor:** Panita Thusaranon  
**Topic:** Density-Based Clustering (DBSCAN) — Manual Step-by-Step Calculation

---

## 🎯 Assignment Instruction / โจทย์แบบฝึกหัด

### 🇹🇭 ภาษาไทย
คำนวณ DBSCAN ตามแบบฝึกหัดในสไลด์ โดยระบุประเภทของแต่ละ Point (Core Point, Border Point หรือ Noise Point) พร้อมทั้งอธิบายขั้นตอนการสร้าง Cluster ด้วยมือ

### 🇬🇧 English
Manually calculate DBSCAN clustering following the exercise in the lecture slides.
1. Identify the type of each data point: **Core Point**, **Border Point**, or **Noise Point**
2. Show the step-by-step process of expanding clusters from each core point
3. State the final cluster assignments for all points

---

## 📚 Key Parameters to Use

| Parameter | Symbol | Description |
|---|---|---|
| **Epsilon** | ε | Neighborhood radius — check the slide for the given value |
| **MinPts** | min_samples | Minimum neighbors to be a Core Point — check the slide |

---

## 💡 Suggested Workflow / แนวทางการทำ

1. **Mark neighborhoods:** For each point, count how many other points fall within distance ε
2. **Classify points:**
   - `Core Point` → has ≥ MinPts neighbors within ε (including itself)
   - `Border Point` → has < MinPts neighbors, but is within ε of a Core Point
   - `Noise Point` → not a Core Point and not within ε of any Core Point (label = -1)
3. **Build clusters:** Start from any unvisited Core Point → expand by adding all density-reachable points
4. **Report final labels:** Assign cluster numbers (0, 1, 2, …) and mark noise as -1

---

## 📌 Quick Reference

```
Distance formula (Euclidean):
  d(p, q) = √((x₂ - x₁)² + (y₂ - y₁)²)

Point p is density-reachable from q if:
  d(p, q) ≤ ε  AND  q is a Core Point
```

---

*Applied Machine Learning — DSBA8 | Week 2 Homework*
