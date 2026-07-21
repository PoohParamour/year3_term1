import cv2
import numpy as np
from .base import BaseOCREngine
from ocr_system.schemas import OCRLine


class PaddleOCREngine(BaseOCREngine):
    name = "paddle"

    def __init__(self, lang: str = "th"):
        from paddleocr import PaddleOCR
        # PaddleOCR 3.x enables a heavy 5-model document pipeline by default
        # (orientation, unwarping, textline rotation, server-size detector).
        # Our inputs are straight PDF renders, so turn those modules off and
        # use the mobile detector — several times faster on CPU.
        # Fall back to the 2.x kwargs for older installs.
        fast_flags = dict(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )
        try:
            # Passing model names makes PaddleOCR ignore `lang`, so the
            # language-specific recognition model must be named explicitly.
            self.model = PaddleOCR(
                text_detection_model_name="PP-OCRv5_mobile_det",
                text_recognition_model_name=f"{lang}_PP-OCRv5_mobile_rec",
                **fast_flags,
            )
        except Exception:
            try:
                # No per-language v5 rec model (e.g. en/ch) - let lang decide.
                self.model = PaddleOCR(lang=lang, **fast_flags)
            except (TypeError, ValueError):
                self.model = PaddleOCR(use_angle_cls=True, lang=lang)

    def recognize(self, image: np.ndarray, page: int | None = None) -> list[OCRLine]:
        # PaddleOCR expects a 3-channel image; preprocessing can hand us a
        # 2D binary/grayscale array, which breaks the 3.x doc pipeline.
        if image.ndim == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # PaddleOCR 3.x dropped the `cls` kwarg from .ocr().
        try:
            result = self.model.ocr(image)
        except TypeError:
            result = self.model.ocr(image, cls=True)
        lines: list[OCRLine] = []
        for block in result or []:
            # 3.x returns dict-like results with parallel lists.
            if isinstance(block, dict) or hasattr(block, "get"):
                texts = block.get("rec_texts", [])
                scores = block.get("rec_scores", [])
                boxes = block.get("rec_polys", block.get("dt_polys", []))
                for i, text in enumerate(texts):
                    conf = float(scores[i]) if i < len(scores) else None
                    box = boxes[i].tolist() if i < len(boxes) and hasattr(boxes[i], "tolist") else (boxes[i] if i < len(boxes) else None)
                    lines.append(OCRLine(text=text, confidence=conf, box=box, engine=self.name, page=page))
                continue
            # 2.x returns nested [box, (text, conf)] lists.
            for item in block or []:
                box = item[0]
                text = item[1][0]
                conf = float(item[1][1])
                lines.append(OCRLine(text=text, confidence=conf, box=box, engine=self.name, page=page))
        return lines
