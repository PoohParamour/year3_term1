import json
import re
from pathlib import Path
from typing import Any


EN_MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

TH_MONTHS = {
    "มกราคม": 1,
    "กุมภาพันธ์": 2,
    "มีนาคม": 3,
    "เมษายน": 4,
    "พฤษภาคม": 5,
    "มิถุนายน": 6,
    "กรกฎาคม": 7,
    "สิงหาคม": 8,
    "กันยายน": 9,
    "ตุลาคม": 10,
    "พฤศจิกายน": 11,
    "ธันวาคม": 12,
}

GRADE_RE = re.compile(r"^(?:[abcdf][+-]?|s|u|w|i|t\([abcdfs][+-]?\)|-)$", re.IGNORECASE)
SUBJECT_ID_RE = re.compile(r"^\d{8}\.?$")


def extract_transcript_from_file(path: str | Path, language: str | None = None) -> dict[str, Any]:
    payload = _load_ocr_payload(path)
    return extract_transcript(payload["text"], payload.get("lines", []), language=language)


def extract_transcript(
    text: str,
    ocr_lines: list[dict[str, Any]] | None = None,
    language: str | None = None,
) -> dict[str, Any]:
    tokens = _clean_tokens(text.splitlines())
    language = language or _detect_language(text)
    is_thai = language.lower().startswith("th")

    header = _extract_header(tokens, text, is_thai=is_thai)
    if ocr_lines:
        semesters = _extract_subjects_from_boxes(ocr_lines, text)
    else:
        semesters = _extract_subjects_from_tokens(tokens, text)

    total_credits, cumulative_gpa = _extract_summary_scores(tokens, text)

    transcript = {
        "semesters": semesters,
        "master_comprehensive": None,
        "master_thesis": None,
        "master_qualify": None,
        "total_credits_earned": total_credits,
        "cumulative_gpa": cumulative_gpa,
    }

    return {
        "header_detail": header,
        "transcript_detail": transcript,
        "footer_detail": _extract_footer(tokens, is_thai=is_thai),
    }


def export_transcript_to_json(
    ocr_json_path: str,
    output_json_path: str = "extracted_transcript.json",
) -> dict[str, Any]:
    """สกัดข้อมูลจาก OCR และบันทึกผลลัพธ์เป็นไฟล์ JSON"""
    data = extract_transcript_from_file(ocr_json_path)
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"บันทึกผลลัพธ์เป็นไฟล์ JSON เรียบร้อยแล้วที่: {output_json_path}")
    return data


def _load_ocr_payload(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        lines = []
        for page in data.get("pages", []):
            lines.extend(page.get("lines", []))
        return {"text": data.get("text", ""), "lines": lines}

    return {"text": path.read_text(encoding="utf-8"), "lines": []}


def _detect_language(text: str) -> str:
    thai_chars = len(re.findall(r"[\u0e00-\u0e7f]", text))
    return "th" if thai_chars > 0 else "en"


def _clean_tokens(lines: list[str]) -> list[str]:
    tokens = []
    for line in lines:
        value = line.strip()
        if not value or value.startswith("--- Page"):
            continue
        tokens.append(value)
    return tokens


def _token_key(value: str) -> str:
    return re.sub(r"[\s:.,]+", "", value).lower()


def _schema_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip().lower()
    value = re.sub(r"\s+", "", value)
    value = value.replace(".", "")
    return value or None


def _signature_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip().lower()
    value = value.strip("()")
    value = re.sub(r"\s+", "", value)
    return value or None


def _subject_text(tokens: list[str]) -> str:
    return _schema_text("".join(tokens)) or ""


def _find_sequence(tokens: list[str], label: list[str], start: int = 0) -> int:
    label_keys = [_token_key(item) for item in label]
    token_keys = [_token_key(item) for item in tokens]
    for index in range(start, len(token_keys) - len(label_keys) + 1):
        if token_keys[index : index + len(label_keys)] == label_keys:
            return index
    return -1


def _slice_after_until(tokens: list[str], label: list[str], stops: list[list[str]]) -> list[str]:
    start = _find_sequence(tokens, label)
    if start < 0:
        return []
    start += len(label)
    end = len(tokens)
    for stop in stops:
        index = _find_sequence(tokens, stop, start)
        if index >= 0:
            end = min(end, index)
    return [item for item in tokens[start:end] if item not in {":"}]


def _value_after_label(tokens: list[str], label: list[str]) -> str | None:
    values = _slice_after_until(
        tokens,
        label,
        [
            ["gpa"],
            ["cumulative", "gpa"],
            ["end", "of", "transcript"],
            ["not", "valid"],
        ],
    )
    if not values:
        return None
    return " ".join(values[:3])


def _extract_header(tokens: list[str], text: str, is_thai: bool) -> dict[str, Any]:
    student_id = _first_match(tokens, r"^\d{8,12}$") or _first_match([text], r"\b(\d{8,12})\b")

    prename, name = None, None
    name_match = re.search(r"(นางสาว|นาย|นาง|Ms\.|Mr\.|Miss)\s*([^\n\r:=]+)", text)
    if name_match:
        prename = name_match.group(1)
        name_val = name_match.group(2).strip()
        name_val = re.split(r"(?:รหัส|คณะ|วันเกิด|วันเข้า|student|id|faculty)", name_val, flags=re.IGNORECASE)[0].strip()
        name = name_val
    else:
        name_tokens = (
            _slice_after_until(tokens, ["name"], [["student", "id"], ["รหัส", "นักศึกษา"], ["รหัสนักศึกษา"]])
            or _slice_after_until(tokens, ["ชื่อ", "นามสกุล"], [["รหัส"], ["รหัสนักศึกษา"]])
            or _slice_after_until(tokens, ["ชื่อ"], [["รหัส"], ["รหัสนักศึกษา"], ["คณะ"]])
        )
        prename, name = _split_name(name_tokens, is_thai=is_thai)

    dob_match = re.search(r"(?:วันเกิด|วัน\s*เดือน\s*ปีเกิด|date\s*of\s*birth)\s*[:=]?\s*([^\n\r]+)", text, re.IGNORECASE)
    dob_text = dob_match.group(1) if dob_match else " ".join(_slice_after_until(tokens, ["date", "of", "birth"], [["date", "of", "admission"]]))

    admis_match = re.search(r"(?:วันเข้าศึกษา|วันเข้าเรียน|วันเข้า|เข้าศึกษา|date\s*of\s*admission|admission)\s*[:=]?\s*([^\n\r]+)", text, re.IGNORECASE)
    admis_text = admis_match.group(1) if admis_match else " ".join(_slice_after_until(tokens, ["date", "of", "admission"], [["degree"]]))

    grad_match = re.search(r"(?:วันสำเร็จการศึกษา|date\s*of\s*graduation|สำเร็จการศึกษา)\s*[:=]?\s*([^\n\r]+)", text, re.IGNORECASE)
    grad_text = grad_match.group(1) if grad_match else " ".join(_slice_after_until(tokens, ["date", "of", "graduation"], [["program"], ["หลักสูตร"]]))

    grad_date = _parse_date(grad_text)
    grad_reason = None
    if not grad_date:
        reason_match = re.search(r"((?:n/a\s*)?\(?(?:พ้นสภาพ|ลาออก|ไม่สำเร็จ)[^\n\r\)]*\)?)", text, re.IGNORECASE)
        if reason_match:
            grad_reason = _schema_text(reason_match.group(1))
        elif grad_text:
            grad_reason = _schema_text(grad_text)

    deg_match = re.search(r"(?:ปริญญา|degree)\s*[:=]?\s*([^\n\r]+)", text, re.IGNORECASE)
    deg_text = deg_match.group(1) if deg_match else " ".join(_slice_after_until(tokens, ["degree"], [["date", "of", "graduation"], ["program"]]))
    deg_text = re.split(r"(?:วันสำเร็จ|หลักสูตร|program|date)", deg_text, flags=re.IGNORECASE)[0]

    prog_match = re.search(r"(?:หลักสูตร|สาขาวิชา|program)\s*[:=]?\s*([^\n\r]+)", text, re.IGNORECASE)
    prog_text = prog_match.group(1) if prog_match else " ".join(_slice_after_until(tokens, ["program"], [["1st", "semester"], ["2nd", "semester"], ["ภาค"]]))
    prog_text = re.split(r"(?:ภาค|semester|1st|2nd)", prog_text, flags=re.IGNORECASE)[0]

    return {
        "uni_name": _extract_uni_name(tokens, text, is_thai=is_thai),
        "uni_address": _extract_uni_address(tokens, text, is_thai=is_thai),
        "student_id": student_id,
        "faculty_name": _extract_faculty_name(tokens, text, is_thai=is_thai),
        "prename": _schema_text(prename),
        "name": _schema_text(name),
        "date_of_birth": _parse_date(dob_text),
        "admis_date": _parse_date(admis_text),
        "grad_date": grad_date or "0000-00-00",
        "grad_reason": grad_reason,
        "degree": _schema_text(deg_text),
        "major": None,
        "program": _schema_text(prog_text),
        "honor": 0,
    }


def _extract_uni_name(tokens: list[str], text: str, is_thai: bool) -> str | None:
    if "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง" in text or "พระจอมเกล้า" in text:
        return _schema_text("สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง")
    if is_thai:
        m = re.search(r"(สถาบัน[^\n\r]+|มหาวิทยาลัย[^\n\r]+)", text)
        if m:
            return _schema_text(m.group(1))
    end = _find_sequence(tokens, ["chalongkrung"])
    if end < 0:
        end = _find_sequence(tokens, ["transcript"])
    return _schema_text(" ".join(tokens[:end])) if end > 0 else (_schema_text(tokens[0]) if tokens else None)


def _extract_uni_address(tokens: list[str], text: str, is_thai: bool) -> str | None:
    m = re.search(r"(เลขที่\s*\d+[^\n\r]+?(?:กรุงเทพ[^\n\r]*|\d{5}))", text)
    if m:
        return _schema_text(m.group(1))
    if is_thai:
        m_alt = re.search(r"([^\n\r]*ฉลองกรุง[^\n\r]*)", text)
        if m_alt:
            return _schema_text(m_alt.group(1))
        return None
    start = _find_sequence(tokens, ["chalongkrung"])
    end = _find_sequence(tokens, ["transcript"], start)
    return _schema_text(" ".join(tokens[start:end])) if start >= 0 and end > start else None


def _extract_faculty_name(tokens: list[str], text: str, is_thai: bool) -> str | None:
    m = re.search(r"(คณะ[\u0e00-\u0e7f]+)", text)
    if m and is_thai:
        return _schema_text(m.group(1))
    if is_thai:
        value = _slice_after_until(tokens, ["คณะ"], [["ชื่อ"], ["รหัส"], ["หลักสูตร"]])
        return _schema_text(" ".join(["คณะ", *value])) if value else None
    value = _slice_after_until(tokens, ["college", "of"], [["name"]]) or _slice_after_until(tokens, ["faculty", "of"], [["name"]])
    return _schema_text(" ".join(["faculty", "of", *value])) if value else None


def _split_name(tokens: list[str], is_thai: bool) -> tuple[str | None, str | None]:
    if not tokens:
        return None, None
    first = tokens[0].strip()
    if is_thai:
        for p in ["นางสาว", "นาย", "นาง", "ดร."]:
            if first.startswith(p):
                rest = first[len(p) :].strip() + " " + " ".join(tokens[1:])
                return p, rest.strip()
        return None, " ".join(tokens)
    if _token_key(first) in {"mr", "miss", "mrs", "ms"}:
        return tokens[0], " ".join(tokens[1:])
    return None, " ".join(tokens)


def _extract_footer(tokens: list[str], is_thai: bool) -> dict[str, Any]:
    issued = _slice_after_until(tokens, ["date", "of", "issued"], [["not", "valid"], ["director"]])
    signature = _slice_after_until(tokens, ["without", "seal"], [["director"]])
    position_index = _find_sequence(tokens, ["director"])
    by_reg = tokens[position_index + 1 :] if position_index >= 0 else []

    return {
        "updated_at": _parse_date(" ".join(issued)),
        "by": {
            "by_signature": _signature_text(" ".join(signature)),
            "by_position": _schema_text("director") if not is_thai and position_index >= 0 else None,
            "by_reg": _schema_text(" ".join(by_reg)),
        },
    }


def _extract_subjects_from_boxes(ocr_lines: list[dict[str, Any]], text: str) -> list[dict[str, Any]]:
    words = [_line_word(line) for line in ocr_lines if _line_word(line)["text"]]
    words.sort(key=lambda item: (item["page"], item["y"], item["x"]))
    subject_words = [word for word in words if SUBJECT_ID_RE.match(word["key"])]

    sem_boxes = _semester_headers_from_boxes(words)
    sem_text = _semester_headers_from_text(text)
    semesters = sem_boxes if len(sem_boxes) >= len(sem_text) and len(sem_boxes) > 0 else sem_text

    if not semesters and subject_words:
        first_course = next((word for word in subject_words if word["y"] > 700), subject_words[0])
        semesters = [{"year": None, "sem_num": None, "start_y": first_course["y"] - 30}]

    results = []
    for index, semester in enumerate(semesters):
        start_y = semester.get("start_y") or 0
        end_y = semesters[index + 1].get("start_y") if index + 1 < len(semesters) else 10**9
        semester_subjects = []
        ids = [word for word in subject_words if start_y <= word["y"] < end_y]
        for subject_index, subject_id in enumerate(ids):
            next_y = ids[subject_index + 1]["y"] if subject_index + 1 < len(ids) else end_y
            marker_y = _first_marker_y_after(words, subject_id["y"], next_y)
            if marker_y is not None:
                next_y = marker_y
            row_words = [word for word in words if subject_id["y"] - 10 <= word["y"] < next_y - 5]
            semester_subjects.append(_subject_from_box_words(subject_id, row_words))

        gps, gpa = _semester_scores(words, start_y, end_y)
        results.append(
            {
                "year": semester.get("year"),
                "sem_num": semester.get("sem_num"),
                "GPA": gpa,
                "GPS": gps,
                "pass_reason": None,
                "subject": semester_subjects,
            }
        )
    return results


def _semester_headers_from_boxes(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    headers = []
    keys = [word["key"] for word in words]
    for index, key in enumerate(keys):
        if key in {"1st", "2nd", "3rd", "summer"}:
            window = keys[index : index + 5]
            if len(window) >= 5 and window[1] == "semester" and window[2] == "academic" and window[3] == "year":
                if re.fullmatch(r"\d{4}", window[4]):
                    year = int(window[4])
                    sem_num = {"1st": 1, "2nd": 2, "3rd": 3, "summer": 0}[key]
                    headers.append({
                        "year": year + 543 if year < 2400 else year,
                        "sem_num": sem_num,
                        "start_y": words[index]["y"] + 30,
                    })

        w_text = words[index]["text"]
        m = re.search(r"(?:ภาค(?:การศึกษา|เรียน)?ที่?\s*)?([123]|summer)\s*[/.-]\s*(\d{4})", w_text, re.IGNORECASE)
        if m:
            sem_str, year_str = m.group(1), m.group(2)
            sem_num = 0 if sem_str.lower() == "summer" else int(sem_str)
            year = int(year_str)
            headers.append({
                "year": year + 543 if year < 2400 else year,
                "sem_num": sem_num,
                "start_y": words[index]["y"] + 30,
            })
    return headers


def _first_marker_y_after(words: list[dict[str, Any]], start_y: int, fallback_y: int) -> int | None:
    markers = [
        word["y"]
        for word in words
        if start_y < word["y"] < fallback_y and word["key"] in {"gps", "gpa", "total", "cumulative", "end"}
    ]
    return min(markers) if markers else None


def _line_word(line: dict[str, Any]) -> dict[str, Any]:
    text = str(line.get("text", "")).strip()
    box = line.get("box") or [[0, 0]]
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]
    return {
        "text": text,
        "key": _token_key(text),
        "x": min(xs),
        "y": min(ys),
        "page": line.get("page", 1),
    }


def _subject_from_box_words(subject_id: dict[str, Any], row_words: list[dict[str, Any]]) -> dict[str, Any]:
    same_line = [word for word in row_words if abs(word["y"] - subject_id["y"]) <= 18]
    grade = _last_grade(same_line) or _last_grade(row_words)
    credit = _credit_before_grade(same_line, grade) or _credit_before_grade(row_words, grade)
    name_candidates = [
        word
        for word in row_words
        if word["x"] > subject_id["x"] + 80
        and word["x"] < 1000
        and not SUBJECT_ID_RE.match(word["key"])
        and word is not grade
        and word is not credit
    ]
    name_candidates.sort(key=lambda word: (round((word["y"] - subject_id["y"]) / 30), word["x"]))
    return {
        "subject_id": subject_id["key"].rstrip("."),
        "subject_name": _subject_text([word["text"] for word in name_candidates]),
        "type": None,
        "credit": _to_int(credit["text"] if credit else None),
        "grade_earn": _schema_text(grade["text"] if grade else None),
    }


def _last_grade(words: list[dict[str, Any]]) -> dict[str, Any] | None:
    grades = [word for word in words if GRADE_RE.match(word["key"])]
    return max(grades, key=lambda item: (item["x"], item["y"]), default=None)


def _credit_before_grade(words: list[dict[str, Any]], grade: dict[str, Any] | None) -> dict[str, Any] | None:
    candidates = [word for word in words if re.fullmatch(r"\d", word["key"])]
    if grade:
        before_grade = [word for word in candidates if word["x"] < grade["x"] + 20]
        if before_grade:
            return max(before_grade, key=lambda item: item["x"])
    return max(candidates, key=lambda item: item["x"], default=None)


def _semester_scores(words: list[dict[str, Any]], start_y: int, end_y: int) -> tuple[str | None, str | None]:
    scoped = [word for word in words if start_y <= word["y"] < end_y]
    gps = _score_after(scoped, "gps")
    gpa = _score_after(scoped, "gpa")
    return gps, gpa


def _score_after(words: list[dict[str, Any]], label: str) -> str | None:
    labels = [word for word in words if word["key"] == label]
    if not labels:
        return None
    label_word = labels[-1]
    candidates = [
        word for word in words
        if abs(word["y"] - label_word["y"]) <= 20 and word["x"] > label_word["x"] and re.fullmatch(r"\d+\.\d+", word["text"])
    ]
    return candidates[0]["text"] if candidates else None


def _extract_subjects_from_tokens(tokens: list[str], text: str) -> list[dict[str, Any]]:
    semester_headers = _semester_headers_from_text(text)
    if not semester_headers:
        semester_headers = [{"year": None, "sem_num": None}]

    subjects = []
    index = _semester_token_start(tokens)
    while index < len(tokens):
        if SUBJECT_ID_RE.match(_token_key(tokens[index])):
            next_index = index + 1
            while next_index < len(tokens) and not SUBJECT_ID_RE.match(_token_key(tokens[next_index])) and _token_key(tokens[next_index]) not in {"gps", "gpa"}:
                next_index += 1
            chunk = tokens[index + 1 : next_index]
            grade_pos = _last_grade_index(chunk)
            credit_pos = _last_credit_index(chunk[:grade_pos]) if grade_pos is not None else None
            name_tokens = chunk
            if credit_pos is not None and grade_pos is not None:
                name_tokens = [*chunk[:credit_pos], *chunk[grade_pos + 1 :]]
            elif credit_pos is not None:
                name_tokens = chunk[:credit_pos]
            subjects.append(
                {
                    "subject_id": _token_key(tokens[index]).rstrip("."),
                    "subject_name": _subject_text(name_tokens),
                    "type": None,
                    "credit": _to_int(chunk[credit_pos]) if credit_pos is not None else None,
                    "grade_earn": _schema_text(chunk[grade_pos]) if grade_pos is not None else None,
                }
            )
            index = next_index
        else:
            index += 1

    gps = _clean_gpa(_value_after_label(tokens, ["gps"]))
    gpa = _clean_gpa(_value_after_label(tokens, ["gpa"]))

    results = []
    for sem in semester_headers:
        results.append({
            "year": sem.get("year"),
            "sem_num": sem.get("sem_num"),
            "GPA": gpa,
            "GPS": gps,
            "pass_reason": None,
            "subject": subjects if len(semester_headers) == 1 else [],
        })
    return results


def _extract_summary_scores(tokens: list[str], text: str) -> tuple[int | None, str | None]:
    gpa_val = None
    gpa_patterns = [
        r"(?:เกรดเฉลี่ยสะสม|เฉลี่ยสะสม|แต้มเฉลี่ยสะสม|gpax|cumulative\s*gpa|cgpa)\s*[:=]?\s*(\d+\.\d+)",
        r"gpa\s*[:=]?\s*(\d+\.\d+)",
        r"(\d+\.\d+)\s*(?:เกรดเฉลี่ยสะสม|เฉลี่ยสะสม)",
    ]
    for pat in gpa_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            gpa_val = m.group(1)
            break

    if not gpa_val:
        gpa_str = _value_after_label(tokens, ["cumulative", "gpa"]) or _value_after_label(tokens, ["gpa"]) or _value_after_label(tokens, ["เฉลี่ยสะสม"])
        if gpa_str:
            gpa_val = _clean_gpa(gpa_str)

    credits_val = None
    cred_patterns = [
        r"(?:หน่วยกิตสะสม|หน่วยกิตรวม|หน่วยกิตกู้/สะสม|หน่วยกิตกู้|หน่วยกิตที่ผ่าน|total\s*credits\s*earned|credits\s*earned)\s*[:=]?\s*(\d+)",
        r"(\d+)\s*(?:หน่วยกิตสะสม|หน่วยกิตรวม)",
    ]
    for pat in cred_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            credits_val = int(m.group(1))
            break

    if credits_val is None:
        cred_str = _value_after_label(tokens, ["total", "credits", "earned"]) or _value_after_label(tokens, ["credits", "earned"]) or _value_after_label(tokens, ["หน่วยกิตสะสม"])
        if cred_str:
            credits_val = _to_int(cred_str)

    return credits_val, gpa_val


def _semester_token_start(tokens: list[str]) -> int:
    keys = [_token_key(token) for token in tokens]
    for index, key in enumerate(keys):
        if key in {"1st", "2nd", "3rd", "summer"} and keys[index + 1 : index + 4] == ["semester", "academic", "year"]:
            return index + 5
    return 0


def _semester_headers_from_text(text: str) -> list[dict[str, Any]]:
    headers = []
    patterns = [
        r"(?i)\b(1st|2nd|3rd|summer)\s+semester,?\s+(?:academic\s+year\s+)?(\d{4})",
        r"(?:ภาค(?:การศึกษา|เรียน)?ที่?\s*)?([123]|summer)\s*[/.-]\s*(\d{4})",
        r"(?:ภาค(?:การศึกษา|เรียน)?ที่?\s*)([123]|summer)\s*(?:ปีการศึกษา)?\s*(\d{4})",
        r"(?i)semester\s*([123]|summer)\s*[/.-]?\s*(\d{4})",
    ]

    for pat in patterns:
        for match in re.finditer(pat, text):
            s_str = match.group(1).lower()
            sem_num = {"1st": 1, "2nd": 2, "3rd": 3, "summer": 0}.get(s_str)
            if sem_num is None:
                sem_num = 0 if s_str == "summer" else int(s_str)
            year = int(match.group(2))
            headers.append({
                "year": year + 543 if year < 2400 else year,
                "sem_num": sem_num,
                "start_y": _rough_y_from_offset(text, match.end()),
            })

    unique_headers = []
    seen = set()
    for h in headers:
        key = (h["year"], h["sem_num"])
        if key not in seen:
            seen.add(key)
            unique_headers.append(h)

    return unique_headers


def _rough_y_from_offset(text: str, offset: int) -> int:
    return 0 if offset < 0 else 1


def _parse_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()

    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", value)
    if match:
        return match.group(0)

    match = re.search(r"(?i)\b([a-z]+)\s+(\d{1,2}),?\s+(\d{4})", value)
    if match and match.group(1).lower() in EN_MONTHS:
        year = int(match.group(3))
        return f"{year:04d}-{EN_MONTHS[match.group(1).lower()]:02d}-{int(match.group(2)):02d}"

    for month_name, month in TH_MONTHS.items():
        match = re.search(rf"(\d{{1,2}})\s*{re.escape(month_name)}\s*(\d{{4}})", value)
        if match:
            year = int(match.group(2))
            year = year - 543 if year > 2400 else year
            return f"{year:04d}-{month:02d}-{int(match.group(1)):02d}"

    match = re.search(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})", value)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        year = year - 543 if year > 2400 else year
        return f"{year:04d}-{month:02d}-{day:02d}"

    return None


def _first_match(tokens: list[str], pattern: str) -> str | None:
    for token in tokens:
        match = re.search(pattern, token)
        if match:
            return match.group(0)
    return None


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.search(r"\d+", str(value))
    return int(match.group(0)) if match else None


def _clean_gpa(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"\d+\.\d+", value)
    return match.group(0) if match else None


def _last_grade_index(tokens: list[str]) -> int | None:
    for index in range(len(tokens) - 1, -1, -1):
        if GRADE_RE.match(_token_key(tokens[index])):
            return index
    return None


def _last_credit_index(tokens: list[str]) -> int | None:
    for index in range(len(tokens) - 1, -1, -1):
        if re.fullmatch(r"\d", _token_key(tokens[index])):
            return index
    return None


if __name__ == "__main__":
    # บันทึกผลลัพธ์เป็นไฟล์ JSON
    export_transcript_to_json(
        ocr_json_path="ocr_result.json",
        output_json_path="extracted_transcript.json",
    )