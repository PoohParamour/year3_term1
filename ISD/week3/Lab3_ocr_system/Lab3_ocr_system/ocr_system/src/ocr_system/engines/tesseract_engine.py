import cv2
import numpy as np
from .base import BaseOCREngine
from ocr_system.schemas import OCRLine


class TesseractOCREngine(BaseOCREngine):
    name = "tesseract"

    def __init__(self, languages: str = "tha+eng", psm: int = 6):
        import pytesseract
        self.pytesseract = pytesseract
        self.languages = languages
        self.config = f"--oem 3 --psm {psm}"

    def recognize(self, image: np.ndarray, page: int | None = None) -> list[OCRLine]:
        if len(image.shape) == 2:
            rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        data = self.pytesseract.image_to_data(
            rgb,
            lang=self.languages,
            config=self.config,
            output_type=self.pytesseract.Output.DICT,
        )
        # image_to_data returns word-level tokens; for Thai these are tiny
        # sub-word fragments. Group them back into text lines using
        # (block, paragraph, line), then join tokens by the real horizontal
        # gap on the image so spaces only appear where the page has them.
        groups: dict[tuple, list[dict]] = {}
        n = len(data["text"])
        for i in range(n):
            text = (data["text"][i] or "").strip()
            if not text:
                continue
            key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
            try:
                conf = float(data["conf"][i]) / 100.0
            except ValueError:
                conf = None
            groups.setdefault(key, []).append({
                "text": text,
                "conf": conf,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
            })

        lines: list[OCRLine] = []
        for key in sorted(groups):
            words = sorted(groups[key], key=lambda w: w["left"])
            heights = [w["height"] for w in words]
            gap_threshold = max(6.0, 0.3 * (sum(heights) / len(heights)))
            parts = [words[0]["text"]]
            for prev, cur in zip(words, words[1:]):
                gap = cur["left"] - (prev["left"] + prev["width"])
                parts.append((" " if gap > gap_threshold else "") + cur["text"])
            text = "".join(parts)
            confs = [w["conf"] for w in words if w["conf"] is not None]
            conf = sum(confs) / len(confs) if confs else None
            x0 = min(w["left"] for w in words)
            y0 = min(w["top"] for w in words)
            x1 = max(w["left"] + w["width"] for w in words)
            y1 = max(w["top"] + w["height"] for w in words)
            box = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
            lines.append(OCRLine(text=text, confidence=conf, box=box, engine=self.name, page=page))
        return lines
