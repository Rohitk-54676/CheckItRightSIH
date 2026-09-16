import re
from difflib import SequenceMatcher
from typing import Any

TEXT_CORRECTIONS = {
    # ── Cosmetic / Personal Care ──
    "LOLLON": "LOTION",
    "LOTTON": "LOTION",
    "L0TION": "LOTION",
    "LOTLON": "LOTION",
    "SUNSCREEM": "SUNSCREEN",
    "SUNSCREN": "SUNSCREEN",
    "PROTECTNE": "PROTECTIVE",
    "PROTECIIVE": "PROTECTIVE",
    "MOISTURISER": "MOISTURIZER",
    "CONDITONER": "CONDITIONER",
    "CONDITIONAR": "CONDITIONER",
    "CLEANSAR": "CLEANSER",
    "EAUDEPARFUM": "EAU DE PARFUM",
    "EAU DEPARFUM": "EAU DE PARFUM",
    "EAUDEPARFUM": "EAU DE PARFUM",
    "DEOPARFUM": "EAU DE PARFUM",
    "PARFUM": "PARFUM",

    # ── Common English OCR misreads ──
    "SKN": "SKIN",
    "DAKENLNG": "DARKENING",
    "DARKENLNG": "DARKENING",
    "DARKSENING": "DARKENING",
    "EVEYDOY": "EVERYDAY",
    "PROTECLON": "PROTECTION",
    "PROTECTON": "PROTECTION",
    "NON-GREASYFORMULA": "NON-GREASY FORMULA",
    "ALSNTYPES": "ALL SKIN TYPES",
    "ALSINTYPES": "ALL SKIN TYPES",
    "ALLSKINTYPES": "ALL SKIN TYPES",

    # ── Plastic / Recycling codes ──
    "GPE": "LDPE",
    "LOPE": "LDPE",

    # ── Ingredient misreads ──
    "ZUTATEN": "INGREDIENTS",
    "PHENANYEFHAROL": "PHENOXYETHANOL",
    "ETIPAOBEN": "ETHYLPARABEN",
    "PROPPOROBEN": "PROPYLPARABEN",
    "MYISTATE": "MYRISTATE",
    "GLVCOL": "GLYCOL",
    "ALCOHOL": "ALCOHOL",

    # ── Brand misreads ──
    "HIMALYA": "HIMALAYA",
    "HIMALAYAWELNESS": "HIMALAYA WELLNESS",
    "HIMALAYAWELLNESS": "HIMALAYA WELLNESS",
    "BEARDD": "BEARDO",
    "BEARDO": "BEARDO",
}


def apply_text_corrections(text: str) -> str:
    """
    Apply OCR correction dictionary to raw text.
    Word-boundary aware, case-insensitive.
    """
    if not text:
        return text

    corrected = text

    for wrong, right in TEXT_CORRECTIONS.items():
        corrected = re.sub(
            rf"\b{re.escape(wrong)}\b",
            right,
            corrected,
            flags=re.IGNORECASE,
        )

    return corrected


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = text.strip()

    text = apply_text_corrections(text)

    return text


def clean_value(value: str) -> str:
    value = normalize_text(value)
    value = value.strip(" :-.,;•")
    return value.strip()


def _compact_text(value: str) -> str:
    return re.sub(
        r"[^A-Z0-9]+",
        "",
        value.upper(),
    )


def _similarity(left: str, right: str) -> float:
    return SequenceMatcher(
        None,
        _compact_text(left),
        _compact_text(right),
    ).ratio()


def _looks_like_label(line: str, labels: list[str], threshold: float = 0.72) -> bool:
    upper = line.upper()

    for label in labels:
        if re.search(
            rf"\b{re.escape(label)}\b",
            upper,
            re.IGNORECASE,
        ):
            return True

    words = re.findall(
        r"[A-Za-z]{3,}",
        line,
    )

    for word in words:
        for label in labels:
            if _similarity(word, label) >= threshold:
                return True

    return False


def _value_after_fuzzy_label(
    line: str,
    labels: list[str],
) -> str | None:
    upper = line.upper()

    for label in sorted(labels, key=len, reverse=True):
        match = re.search(
            rf"\b{re.escape(label)}\b\s*(?:DATE|NO\.?|NUMBER)?\s*[:\-]?\s*(.*)$",
            line,
            re.IGNORECASE,
        )
        if match:
            value = clean_value(match.group(1))
            if value:
                return value

    words = list(
        re.finditer(
            r"[A-Za-z]{3,}",
            line,
        )
    )

    for word_match in words:
        word = word_match.group(0)
        if any(
            _similarity(word, label) >= 0.72
            for label in labels
        ):
            remainder = line[word_match.end():]
            remainder = re.sub(
                r"^\s*(?:DATE|NO\.?|NUMBER)?\s*[:\-]?\s*",
                "",
                remainder,
                flags=re.IGNORECASE,
            )
            value = clean_value(remainder)
            if value:
                return value

    return None


def get_search_text(
    detections: list[dict],
) -> str:
    return "\n".join(
        str(item.get("text", ""))
        for item in detections
        if item.get("text")
    )


def extract_mrp(
    text: str,
    detections: list[dict] | None = None,
) -> float | None:
    def parse_numeric_value(value: str) -> float | None:
        value = value.strip().replace(",", "")
        value = re.sub(
            r"^(?:₹|RS\.?|INR)\s*",
            "",
            value,
            flags=re.IGNORECASE,
        )

        if not re.fullmatch(
            r"\d{1,6}(?:\.\d{1,2})?",
            value,
        ):
            return None

        try:
            number = float(value)
        except ValueError:
            return None

        if number <= 0 or number > 100000:
            return None

        return number

    def is_unit_value(value: str) -> bool:
        return bool(
            re.search(
                r"(?:KG|KGS|G|GM|GMS|GRAM|GRAMS|"
                r"MG|ML|L|LTR|LITRE|LITRES|"
                r"PCS|PC|PIECE|PIECES|KCAL)\b",
                value,
                re.IGNORECASE,
            )
        )

    normalized = normalize_text(text)

    explicit_patterns = [
        # MRP : 120.00  |  MRP ₹ : 1500.00  |  MRP Rs. 120
        r"(?<![A-Z])M\s*\.?\s*R\s*\.?\s*P\s*\.?\s*(?:₹|RS\.?|INR)?\s*(?:[:\-]|\s)*"
        r"(?:₹|RS\.?|INR)?\s*"
        r"(\d{1,6}(?:\.\d{1,2})?)",

        r"(?<![A-Z])MAX\s*\.?\s*RETAIL\s*\.?\s*PRICE\s*(?:₹|RS\.?|INR)?\s*(?:[:\-]|\s)*"
        r"(?:₹|RS\.?|INR)?\s*"
        r"(\d{1,6}(?:\.\d{1,2})?)",
    ]

    for pattern in explicit_patterns:
        match = re.search(
            pattern,
            normalized,
            re.IGNORECASE,
        )
        if match:
            value = parse_numeric_value(match.group(1))
            if value is not None:
                return value

    if not detections:
        lines = normalized.splitlines()
        for index, line in enumerate(lines):
            if not _looks_like_label(
                line,
                ["MRP", "MAX RETAIL PRICE"],
                0.76,
            ):
                continue

            block = " ".join(
                lines[index:index + 7]
            )
            match = re.search(
                r"(?:₹|RS\.?|INR)?\s*(\d{1,6}(?:\.\d{1,2})?)",
                block,
                re.IGNORECASE,
            )
            if match:
                value = parse_numeric_value(match.group(1))
                if value is not None:
                    return value

        return None

    cleaned_detections = []

    for index, detection in enumerate(detections):
        raw = str(
            detection.get("text", "")
        ).strip()

        if not raw:
            continue

        try:
            confidence = float(
                detection.get("confidence", 0)
            )
        except (TypeError, ValueError):
            confidence = 0.0

        bbox = detection.get("bbox")
        if bbox is None or len(bbox) < 4:
            continue

        try:
            x1, y1, x2, y2 = [
                float(value)
                for value in bbox[:4]
            ]
        except (TypeError, ValueError):
            continue

        cleaned_detections.append(
            {
                "index": index,
                "text": raw,
                "upper": raw.upper(),
                "confidence": confidence,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "width": max(x2 - x1, 1.0),
                "height": max(y2 - y1, 1.0),
                "center_x": (x1 + x2) / 2,
                "center_y": (y1 + y2) / 2,
            }
        )

    if not cleaned_detections:
        return None

    label_detections = [
        detection
        for detection in cleaned_detections
        if _looks_like_label(
            detection["text"],
            ["MRP", "MAX RETAIL PRICE"],
            0.76,
        )
    ]

    candidates = []

    for label in label_detections:
        for detection in cleaned_detections:
            if detection["index"] == label["index"]:
                continue

            value = parse_numeric_value(
                detection["text"]
            )
            if value is None or is_unit_value(
                detection["text"]
            ):
                continue

            index_distance = abs(
                detection["index"] - label["index"]
            )

            if index_distance > 10:
                continue

            vertical_distance = abs(
                detection["center_y"] - label["center_y"]
            )
            horizontal_distance = abs(
                detection["center_x"] - label["center_x"]
            )

            label_height = max(
                label["height"],
                1.0,
            )

            same_line = (
                vertical_distance <= label_height * 2.0
            )
            directly_right = (
                detection["center_x"] >= label["center_x"]
                and horizontal_distance <= label_height * 25
                and vertical_distance <= label_height * 3
            )
            directly_below = (
                detection["center_y"] >= label["center_y"]
                and vertical_distance <= label_height * 7
                and horizontal_distance <= label_height * 20
            )

            if not (
                same_line
                or directly_right
                or directly_below
            ):
                continue

            distance_score = 1.0 / (
                1.0
                + (
                    vertical_distance + horizontal_distance
                ) / label_height
            )

            index_score = 1.0 / (
                1.0 + index_distance
            )

            confidence_score = min(
                max(detection["confidence"], 0.0),
                1.0,
            )

            relation_bonus = 0.0
            if same_line:
                relation_bonus += 0.22
            if directly_right:
                relation_bonus += 0.12
            if directly_below:
                relation_bonus += 0.08

            decimal_bonus = (
                0.08
                if re.search(
                    r"\.\d{1,2}$",
                    detection["text"].strip(),
                )
                else 0.0
            )

            score = (
                confidence_score * 0.35
                + distance_score * 0.20
                + index_score * 0.15
                + relation_bonus
                + decimal_bonus
            )

            candidates.append(
                {
                    "value": value,
                    "score": score,
                    "confidence": confidence_score,
                    "index_distance": index_distance,
                }
            )

    if candidates:
        candidates.sort(
            key=lambda item: (
                item["score"],
                item["confidence"],
                -item["index_distance"],
            ),
            reverse=True,
        )

        best = candidates[0]
        if (
            best["score"] >= 0.45
            and best["confidence"] >= 0.45
        ):
            return best["value"]

    lines = [
        clean_value(
            str(item.get("text", ""))
        )
        for item in detections
        if item.get("text")
    ]

    for index, line in enumerate(lines):
        if not _looks_like_label(
            line,
            ["MRP", "MAX RETAIL PRICE"],
            0.76,
        ):
            continue

        for candidate_line in lines[index:index + 8]:
            if is_unit_value(candidate_line):
                continue

            currency_match = re.search(
                r"(?:₹|RS\.?|INR)\s*(\d{1,6}(?:\.\d{1,2})?)",
                candidate_line,
                re.IGNORECASE,
            )
            if currency_match:
                value = parse_numeric_value(
                    currency_match.group(1)
                )
                if value is not None:
                    return value

            standalone = re.fullmatch(
                r"\d{1,6}(?:\.\d{1,2})?",
                candidate_line.replace(",", "").strip(),
            )
            if standalone:
                value = parse_numeric_value(
                    candidate_line
                )
                if value is not None:
                    return value

    return None


def extract_net_quantity(
    text: str,
) -> dict[str, Any] | None:
    unit_pattern = (
        r"KG|KGS|G|GM|GMS|GRAM|GRAMS|"
        r"MG|ML|L|LTR|LITRE|LITRES|"
        r"PCS|PC|PIECE|PIECES"
    )

    unit_map = {
        "KG": "kg",
        "KGS": "kg",
        "G": "g",
        "GM": "g",
        "GMS": "g",
        "GRAM": "g",
        "GRAMS": "g",
        "MG": "mg",
        "ML": "ml",
        "L": "l",
        "LTR": "l",
        "LITRE": "l",
        "LITRES": "l",
        "PC": "pcs",
        "PCS": "pcs",
        "PIECE": "pcs",
        "PIECES": "pcs",
    }

    label_pattern = (
        r"NET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS?|"
        r"VOL\.?|VOLUME)"
    )

    patterns = [
        rf"(?:{label_pattern})"
        rf"\s*[:.\-]?\s*"
        rf"(\d+(?:\.\d+)?)\s*({unit_pattern})\b",

        rf"(?:{label_pattern})"
        rf"\s*[:.\-]?\s*"
        rf"({unit_pattern})\s*(\d+(?:\.\d+)?)\b",
    ]

    for pattern_index, pattern in enumerate(patterns):
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        if pattern_index == 0:
            value_text = match.group(1)
            unit_text = match.group(2)
        else:
            unit_text = match.group(1)
            value_text = match.group(2)

        try:
            value = float(value_text)
        except ValueError:
            continue

        return {
            "value": value,
            "unit": unit_map.get(
                unit_text.upper(),
                unit_text.lower(),
            ),
        }

    quantity_context = re.search(
        rf"(?:{label_pattern}|ETNT)"
        r".{0,100}",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if quantity_context:
        context = quantity_context.group(0)
        match = re.search(
            rf"(\d+(?:\.\d+)?)\s*({unit_pattern})\b",
            context,
            re.IGNORECASE,
        )

        if match:
            try:
                value = float(match.group(1))
            except ValueError:
                value = None

            if value is not None:
                return {
                    "value": value,
                    "unit": unit_map.get(
                        match.group(2).upper(),
                        match.group(2).lower(),
                    ),
                }

    return None


def extract_manufacturer(
    text: str,
) -> str | None:
    normalized = normalize_text(text)

    patterns = [
        r"(?:MANUFACTURED\s*(?:AND|&)\s*MARKETED\s*BY|"
        r"MANUFACTURED\s+BY|"
        r"MANUFACTURER|"
        r"MANOFACTURED\s+BY|"
        r"MFD\.?\s*BY|"
        r"MARKETED\s+BY)"
        r"\s*[:\-]?\s*"
        r"(.+?)(?=\n|"
        r"\bPACKED\s+BY\b|"
        r"\bPACKER\b|"
        r"\bIMPORTED\s+BY\b|"
        r"\bIMPORTER\b|"
        r"\bMRP\b|"
        r"\bNET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS|VOL)\b|"
        r"\bUBD\b|"
        r"\bUSE\s+BY\b|"
        r"\bFSSAI\b|"
        r"\bLIC\.?\s*NO\b|$)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            normalized,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        value = clean_value(
            match.group(1)
        )
        value = re.sub(
            r"\s+",
            " ",
            value,
        )
        value = re.split(
            r"\b(?:PLOT|ADDRESS|WEBSITE|LIC\.?\s*NO|FSSAI|"
            r"CUSTOMER\s+CARE|CONSUMER\s+CARE)\b",
            value,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]
        value = clean_value(value)

        if value and len(value) <= 180:
            return value

    lines = [
        clean_value(line)
        for line in normalized.splitlines()
        if clean_value(line)
    ]

    manufacturer_labels = [
        "MANUFACTURED",
        "MANUFACTURER",
        "MANOFACTURED",
        "MFD",
        "MARKETED",
    ]

    for index, line in enumerate(lines):
        if not _looks_like_label(
            line,
            manufacturer_labels,
            0.72,
        ):
            continue

        candidate = _value_after_fuzzy_label(
            line,
            manufacturer_labels,
        )

        if candidate:
            candidate = re.sub(
                r"^\s*(?:BY|B[YI]|MY)\s*[:\-]?\s*",
                "",
                candidate,
                flags=re.IGNORECASE,
            )
            candidate = re.split(
                r"\b(?:PLOT|ADDRESS|WEBSITE|LIC\.?\s*NO|FSSAI|"
                r"CUSTOMER\s+CARE|CONSUMER\s+CARE|MRP|NET\s*(?:QTY|QUANTITY|WEIGHT|VOL))\b",
                candidate,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]
            candidate = clean_value(candidate)

            if candidate and len(candidate) > 3:
                return candidate

        if index + 1 < len(lines):
            next_line = clean_value(
                lines[index + 1]
            )
            if next_line and not re.search(
                r"\b(?:MRP|NET|BATCH|FSSAI|LIC|MFG|MFD|PKD|EXP)\b",
                next_line,
                re.IGNORECASE,
            ):
                if len(next_line) <= 180:
                    return next_line

    organization_patterns = [
        r"\b[A-Z][A-Za-z&.,'()\- ]{3,120}\b(?:"
        r"CO[\s\-]*OPERATIVE|"
        r"COOPERATIVE|"
        r"FEDERATION|"
        r"FOODS?|"
        r"DAIRY|"
        r"MILK\s+MARKETING|"
        r"INDUSTRIES|"
        r"PRIVATE\s+LIMITED|"
        r"PVT\.?\s*LTD\.?|"
        r"LIMITED|"
        r"LTD\.?"
        r")\b",
    ]

    for pattern in organization_patterns:
        match = re.search(
            pattern,
            normalized,
            re.IGNORECASE,
        )
        if match:
            value = clean_value(
                match.group(0)
            )
            if value and len(value) <= 140:
                return value

    return None


def extract_packer(
    text: str,
) -> str | None:
    patterns = [
        r"(?:PACKED\s+BY|PACKER|PACKED\s+FOR)"
        r"\s*[:\-]?\s*"
        r"(.+?)(?="
        r"\bMANUFACTURED\b|"
        r"\bMANUFACTURER\b|"
        r"\bMFD\b|"
        r"\bIMPORTED\b|"
        r"\bIMPORTER\b|"
        r"\bMRP\b|"
        r"\bNET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS|VOL)\b|$)",

        r"MFD\.?\s*(?:AND|&)\s*/?\s*OR\s*PKD\.?\s*BY"
        r"\s*[:\-]?\s*"
        r"(.+?)(?="
        r"\bMRP\b|"
        r"\bNET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS|VOL)\b|"
        r"\bBEST\s+BEFORE\b|"
        r"\bCONTAINS\b|$)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        value = clean_value(
            match.group(1)
        )
        value = re.sub(
            r"\s+",
            " ",
            value,
        )
        value = value.strip(
            " :-.,;•"
        )

        if value:
            return value

    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        if _looks_like_label(
            line,
            ["PACKED", "PACKER", "PACKED FOR"],
            0.74,
        ):
            candidate = _value_after_fuzzy_label(
                line,
                ["PACKED", "PACKER", "PACKED FOR"],
            )
            candidate = clean_value(
                candidate or ""
            )

            if candidate:
                candidate = re.sub(
                    r"^\s*BY\s*[:\-]?\s*",
                    "",
                    candidate,
                    flags=re.IGNORECASE,
                )
                if candidate:
                    return candidate

            if index + 1 < len(lines):
                next_line = clean_value(
                    lines[index + 1]
                )
                if next_line:
                    return next_line

    return None


def extract_importer(
    text: str,
) -> str | None:
    patterns = [
        r"(?:IMPORTED\s+BY|IMPORTER|IMPORTED\s+FOR)"
        r"\s*[:\-]?\s*"
        r"(.+?)(?=\n|"
        r"\bMANUFACTURED\b|"
        r"\bMANUFACTURER\b|"
        r"\bMFD\b|"
        r"\bPACKED\b|"
        r"\bPACKER\b|"
        r"\bMRP\b|"
        r"\bNET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS|VOL)\b|$)"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        value = clean_value(
            match.group(1)
        )
        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        if value:
            return value

    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        if _looks_like_label(
            line,
            ["IMPORTED", "IMPORTER"],
            0.74,
        ):
            candidate = _value_after_fuzzy_label(
                line,
                ["IMPORTED", "IMPORTER"],
            )
            candidate = clean_value(
                candidate or ""
            )

            if candidate:
                candidate = re.sub(
                    r"^\s*BY\s*[:\-]?\s*",
                    "",
                    candidate,
                    flags=re.IGNORECASE,
                )
                if candidate:
                    return candidate

            if index + 1 < len(lines):
                next_line = clean_value(
                    lines[index + 1]
                )
                if next_line:
                    return next_line

    return None
def extract_date(
    text: str,
    keywords: list[str],
) -> str | None:
    # ── OCR variant expansion (Mfg → Mg, etc.) ──
    expanded_keywords = list(keywords)
    for kw in keywords:
        upper_kw = kw.upper()
        if "MFG" in upper_kw:
            expanded_keywords.append(upper_kw.replace("MFG", "MG"))
        if "MFD" in upper_kw:
            expanded_keywords.append(upper_kw.replace("MFD", "MD"))
        expanded_keywords.append(upper_kw.replace(" ", ". "))
        expanded_keywords.append(upper_kw.replace(" ", ""))

    keywords = list(dict.fromkeys(expanded_keywords))

    keyword_pattern = "|".join(
        re.escape(keyword)
        for keyword in keywords
    )

    date_pattern = (
        # Date range: 03/2025-02/2028
        r"\d{1,2}\s*[\/\-.]\s*\d{2,4}"
        r"\s*(?:-|–|—|to)\s*"
        r"\d{1,2}\s*[\/\-.]\s*\d{2,4}"
        r"|"
        # Full date: 12/03/2025
        r"\d{1,2}\s*[\/\-.]\s*\d{1,2}\s*[\/\-.]\s*\d{2,4}"
        r"|"
        # Month/Year: 03/2025
        r"\d{1,2}\s*[\/\-.]\s*\d{4}"
        r"|"
        # 12 March 2025
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}"
        r"|"
        # 12Mar2025
        r"\d{1,2}\s*[A-Za-z]{3,9}\s*\d{2,4}"
    )

    # 1) Label + value on same line
    pattern = (
        rf"(?:{keyword_pattern})"
        r"\s*(?:DATE|DATED|ON)?"
        r"\s*[:\-]?\s*"
        rf"({date_pattern})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if match:
        return clean_value(
            match.group(1)
        ).replace(".", "/")

    # 2) Label line + value on next 4 lines
    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        if not _looks_like_label(
            line,
            keywords,
            0.72,
        ):
            continue

        block = " ".join(
            lines[index:index + 4]
        )

        match = re.search(
            rf"({date_pattern})",
            block,
            re.IGNORECASE,
        )

        if match:
            return clean_value(
                match.group(1)
            ).replace(".", "/")

    # 3) Standalone date range anywhere in text
    standalone_range = re.search(
        r"\b(\d{1,2}\s*[\/\-.]\s*\d{4}"
        r"\s*(?:-|–|—|to)\s*"
        r"\d{1,2}\s*[\/\-.]\s*\d{4})\b",
        text,
        re.IGNORECASE,
    )

    if standalone_range:
        return clean_value(
            standalone_range.group(1)
        ).replace(".", "/")

    return None


def extract_date_range(
    text: str,
) -> str | None:
    """
    Extracts date ranges. Handles:
      03/2025-02/2028
      03-2025 to 02-2028
      03/2025 - 02/2028
      0872025502/2028 (OCR merged)
    """

    # Pattern 1: Normal date range
    pattern1 = (
        r"\b("
        r"(\d{1,2})\s*[\/\-.]\s*(\d{4})"
        r"\s*(?:-|–|—|to|_)\s*"
        r"(\d{1,2})\s*[\/\-.]\s*(\d{4})"
        r")\b"
    )

    match = re.search(pattern1, text, re.IGNORECASE)
    if match:
        mm1, yyyy1, mm2, yyyy2 = (
            match.group(2), match.group(3),
            match.group(4), match.group(5),
        )
        if 1 <= int(mm1) <= 12 and 1 <= int(mm2) <= 12:
            return f"{mm1}/{yyyy1}-{mm2}/{yyyy2}"

    # Pattern 2: Fully merged (no separators)
    pattern2 = (
        r"\b("
        r"(\d{2})(\d{4})(\d{2})(\d{4})"
        r")\b"
    )

    match = re.search(pattern2, text)
    if match:
        mm1, yyyy1, mm2, yyyy2 = match.groups()
        if 1 <= int(mm1) <= 12 and 1 <= int(mm2) <= 12:
            return f"{mm1}/{yyyy1}-{mm2}/{yyyy2}"

    # Pattern 3: Partially merged with slash
    pattern3 = (
        r"\b("
        r"(\d{2})(\d{4})"
        r"[\s\-–—]*"
        r"(\d{2})\s*/\s*(\d{4})"
        r")\b"
    )

    match = re.search(pattern3, text)
    if match:
        mm1, yyyy1, mm2, yyyy2 = match.groups()
        if 1 <= int(mm1) <= 12 and 1 <= int(mm2) <= 12:
            return f"{mm1}/{yyyy1}-{mm2}/{yyyy2}"

    return None


def extract_best_before(
    text: str,
) -> str | None:
    date_pattern = (
        r"\d{1,2}\s*[\/\-.]\s*\d{1,2}\s*[\/\-.]\s*\d{2,4}"
        r"|"
        r"\d{1,2}\s*[\/\-.]\s*\d{4}"
        r"|"
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}"
        r"|"
        r"[A-Za-z]+\s+\d{2,4}"
    )

    patterns = [
        rf"(?:BEST\s+BEFORE|BEST\s+BEFORE\s+USE)"
        rf"\s*[:\-]?\s*({date_pattern})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )
        if match:
            value = clean_value(
                match.group(1)
            ).replace(".", "/")
            if value:
                return value

    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        if not _looks_like_label(
            line,
            ["BEST BEFORE", "BEST BEFORE USE"],
            0.76,
        ):
            continue

        block = " ".join(
            lines[index:index + 3]
        )
        match = re.search(
            rf"({date_pattern})",
            block,
            re.IGNORECASE,
        )
        if match:
            return clean_value(
                match.group(1)
            ).replace(".", "/")

    return None


def extract_use_by(
    text: str,
) -> str | None:
    # ── NEW: Relative expiry ──
    # "USE BY 36 MONTHS FROM DATE OF MANUFACTURING"
    relative_pattern = (
        r"(?:USE\s*[-]?\s*BY|USE\s+BEFORE|BEST\s+BEFORE|EXP(?:IRY)?)"
        r"\s*[:\-]?\s*"
        r"(\d+\s*(?:MONTHS?|YEARS?|DAYS?|WEEKS?)\s*"
        r"(?:FROM|AFTER|OF)\s*"
        r"(?:DATE\s+OF\s+)?(?:MANUFACTURING|MFG|PACKING|PACKED|PRODUCTION))"
    )

    match = re.search(
        relative_pattern,
        text,
        re.IGNORECASE,
    )

    if match:
        value = clean_value(match.group(1))
        value = re.sub(r"\s+", " ", value)
        return value

    # ── Absolute date (existing logic) ──
    date_pattern = (
        r"\d{1,2}\s*[\/\-.]\s*\d{1,2}\s*[\/\-.]\s*\d{2,4}"
        r"|"
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}"
        r"|"
        r"\d{1,2}\s*[\/\-.]\s*\d{4}"
        r"|"
        r"\d{1,2}\s+[A-Za-z]+\s+\d{2,4}"
    )

    patterns = [
        rf"(?:USE\s*[-]?\s*BY|"
        rf"USE\s+BEFORE|"
        rf"UBD|"
        rf"EXP(?:IRY)?|"
        rf"CONSUME\s+BEFORE)"
        rf"\s*(?:DATE|DATED|ON)?"
        rf"\s*[:\-]?\s*({date_pattern})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            value = clean_value(
                match.group(1)
            ).replace(".", "/")

            if value:
                return value

    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        if not _looks_like_label(
            line,
            ["USE BY", "USE BEFORE", "UBD", "EXP", "EXPIRY", "CONSUME BEFORE"],
            0.72,
        ):
            continue

        block = " ".join(
            lines[index:index + 3]
        )
        match = re.search(
            rf"({date_pattern})",
            block,
            re.IGNORECASE,
        )

        if match:
            return clean_value(
                match.group(1)
            ).replace(".", "/")

    return None


def extract_consumer_care(
    text: str,
) -> str | None:
    values = []

    labeled_patterns = [
        r"(?:CUSTOMER\s+CARE|"
        r"CONSUMER\s+CARE|"
        r"CONSUMER\s+SERVICE|"
        r"CONSUMER\s+CARE\s+CELL|"
        r"HELPLINE|"
        r"FOR\s+FEEDBACK|"
        r"FOR\s+COMPLAINTS?|"
        r"FOR\s+FEEDBACK\s*/?\s*COMPLAINTS?)"
        r"\s*[:\-]?\s*"
        r"(.{0,220})",
    ]

    for pattern in labeled_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        value = clean_value(
            match.group(1)
        )

        value = re.split(
            r"\b(?:MRP|NET\s*(?:QTY|QUANTITY|WEIGHT|CONTENT|CONTENTS)|"
            r"BEST\s+BEFORE|UBD|USE\s+BY|NUTRITIONAL\s+INFORMATION)\b",
            value,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]

        value = clean_value(value)

        if value:
            values.append(value)

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )

    if email_match:
        values.append(
            f"Email: {email_match.group(0)}"
        )

    phone_patterns = [
        r"(?:TOLL\s*FREE|PHONE|TEL|TELEPHONE|MOBILE|CONTACT)"
        r"\s*(?:NO\.?|NUMBER)?\s*[:\-]?\s*"
        r"((?:\+91[\s\-]?)?\d[\d\s\-]{8,14}\d)",

        r"\b1800[\s\-]?\d{3}[\s\-]?\d{4}\b",
    ]

    for pattern in phone_patterns:
        phone_match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if phone_match:
            phone = clean_value(
                phone_match.group(1)
                if phone_match.lastindex
                else phone_match.group(0)
            )

            if phone:
                values.append(
                    f"Phone: {phone}"
                )
                break

    if values:
        unique_values = list(
            dict.fromkeys(values)
        )

        return " | ".join(
            unique_values
        )

    return None


def extract_country_of_origin(
    text: str,
) -> str | None:
    normalized = normalize_text(text)

    patterns = [
        r"(?:COUNTRY\s*OF\s*ORIG[I1]N|MADE\s*IN|PRODUCT\s*OF|ORIGIN\s*[:\-]?)\s*[:\-]?\s*"
        r"([A-Za-z][A-Za-z ]{1,40})",
    ]

    stop_words = (
        r"INGREDIENTS|STORE|NUTRITION(?:AL)?|MRP|BATCH|NET|"
        r"MANUFACTURED|MANUFACTURER|MARKETED|WEBSITE|FSSAI|LIC|"
        r"CUSTOMER|CONSUMER|CARE|USP|USE|BY|PKD|PACKED"
    )

    for pattern in patterns:
        match = re.search(
            pattern,
            normalized,
            re.IGNORECASE,
        )

        if not match:
            continue

        value = clean_value(match.group(1))
        value = re.split(
            rf"\b(?:{stop_words})\b",
            value,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]
        value = clean_value(value)

        if value:
            return value

    lines = [
        clean_value(line)
        for line in normalized.splitlines()
        if clean_value(line)
    ]

    for index, line in enumerate(lines):
        compact = re.sub(r"\s+", "", line.upper())

        if compact.startswith("PRODUCTOF"):
            value = re.sub(
                r"^PRODUCT\s*OF\s*",
                "",
                line,
                flags=re.IGNORECASE,
            )
            value = re.split(
                rf"\b(?:{stop_words})\b",
                value,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]
            value = clean_value(value)
            if value:
                return value

        if compact.startswith("MADEIN"):
            value = re.sub(
                r"^MADE\s*IN\s*",
                "",
                line,
                flags=re.IGNORECASE,
            )
            value = clean_value(value)
            if value:
                return value

        if compact.startswith("COUNTRYOFORIGIN"):
            value = re.sub(
                r"^COUNTRY\s*OF\s*ORIG[I1]N\s*[:\-]?\s*",
                "",
                line,
                flags=re.IGNORECASE,
            )
            value = clean_value(value)
            if value:
                return value

        if re.search(
            r"\b(?:PRODUCT\s*OF|MADE\s*IN|COUNTRY\s*OF\s*ORIG[I1]N)\b",
            line,
            re.IGNORECASE,
        ) and index + 1 < len(lines):
            next_line = clean_value(lines[index + 1])
            if next_line and not re.search(
                rf"\b(?:{stop_words})\b",
                next_line,
                re.IGNORECASE,
            ):
                return next_line

    return None

def extract_batch_number(
    text: str,
) -> str | None:
    patterns = [
        r"\bBATCH\b\s*(?:NO\.?|NUMBER|CODE)?\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]{2,30})",

        r"\bLOT\b\s*(?:NO\.?|NUMBER|CODE)?\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]{2,30})",

        # OCR misread: Bach No
        r"\bBA?CH\b\s*(?:NO\.?|NUMBER|CODE)?\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]{2,30})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        value = clean_value(
            match.group(1)
        )

        if value and not re.fullmatch(
            r"\d{8,14}",
            value,
        ):
            return value

    return None


def _is_valid_ean13(value: str) -> bool:
    if not re.fullmatch(
        r"\d{13}",
        value,
    ):
        return False

    digits = [
        int(char)
        for char in value
    ]

    checksum = sum(
        digits[index]
        * (
            1
            if index % 2 == 0
            else 3
        )
        for index in range(12)
    )

    check_digit = (
        10 - (checksum % 10)
    ) % 10

    return check_digit == digits[12]


def _is_valid_upca(value: str) -> bool:
    if not re.fullmatch(
        r"\d{12}",
        value,
    ):
        return False

    digits = [
        int(char)
        for char in value
    ]

    checksum = sum(
        digits[index]
        * (
            3
            if index % 2 == 0
            else 1
        )
        for index in range(11)
    )

    check_digit = (
        10 - (checksum % 10)
    ) % 10

    return check_digit == digits[11]


def extract_barcode(
    text: str,
) -> str | None:
    explicit_patterns = [
        r"(?:BARCODE|BAR\s*CODE|EAN|UPC|GTIN)"
        r"\s*[:\-]?\s*(\d{8,14})",
    ]

    for pattern in explicit_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1)

            if _is_valid_ean13(value):
                return value

            if _is_valid_upca(value):
                return value

    matches = re.findall(
        r"\b\d{8,14}\b",
        text,
    )

    license_value = extract_fssai_license(
        text
    )

    if license_value:
        matches = [
            value
            for value in matches
            if value != license_value
        ]

    valid_barcodes = []

    for value in matches:
        if _is_valid_ean13(value):
            valid_barcodes.append(value)

        elif _is_valid_upca(value):
            valid_barcodes.append(value)

    if valid_barcodes:
        return valid_barcodes[0]

    return None


def extract_fssai_license(
    text: str,
) -> str | None:
    patterns = [
        r"(?:FSSAI|FSSAI\s+LIC(?:ENCE|ENSE)?|LIC(?:ENCE|ENSE)?\s*NO\.?)"
        r"\s*[:\-]?\s*(\d{10,14})",
        r"\b(\d{14})\b",
    ]

    for index, pattern in enumerate(
        patterns
    ):
        matches = re.finditer(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            value = match.group(1)

            if index == 1:
                nearby = text[
                    max(
                        0,
                        match.start() - 50,
                    ):
                    min(
                        len(text),
                        match.end() + 50,
                    )
                ]

                if not re.search(
                    r"FSSAI|LIC",
                    nearby,
                    re.IGNORECASE,
                ):
                    continue

            return value

    return None


def extract_tax_status(
    text: str,
) -> str | None:
    patterns = [
        r"(INCL\.?\s+OF\s+ALL\s+TAXES)",
        r"(INCLUSIVE\s+OF\s+ALL\s+TAXES)",
        r"(INCLUSIVE\s+OF\s+TAXES)",
        r"(IND\.?\s+OF\s+ALL\s+TAXES)",
        r"(INCL?\.?\s+OF\s+ALL\s+TAXES)",
        r"(INCLUSIVE\s+OF\s+ALL\s+TAXES?)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return clean_value(
                match.group(1)
            )

    lines = [
        clean_value(line)
        for line in normalize_text(text).splitlines()
        if clean_value(line)
    ]

    for line in lines:
        compact = _compact_text(line)
        if (
            "INCL" in compact
            or "IND" in compact
        ) and "ALLTAXES" in compact:
            return line

    return None


def extract_email(
    text: str,
) -> str | None:
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )

    if match:
        return match.group(0)

    return None


def extract_phone(
    text: str,
) -> str | None:
    patterns = [
        r"(?:PHONE|TEL|TELEPHONE|MOBILE|CONTACT)"
        r"\s*(?:NO\.?|NUMBER)?\s*[:\-]?\s*"
        r"((?:\+91[\s\-]?)?\d[\d\s\-]{8,14}\d)",

        r"\b(?:0\d{2,4}[\s\-]?)\d{6,8}\b",

        # Customer Care Number
        r"(?:CUSTOMER\s+CARE\s+NUMBER|CARE\s+NUMBER)"
        r"\s*[:\-]?\s*"
        r"(\+?\d[\d\s\-]{8,14}\d)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            value = clean_value(
                match.group(1)
                if match.lastindex
                else match.group(0)
            )

            value = re.sub(
                r"\s+",
                " ",
                value,
            )

            return value

    return None


def extract_website(
    text: str,
) -> str | None:
    patterns = [
        r"\bhttps?://[^\s,;]+\b",
        r"\b(?:www\.)?[A-Za-z0-9][A-Za-z0-9.-]*\.(?:com|in|co\.in|org|net)\b",
    ]

    candidates = []

    for pattern in patterns:
        for match in re.finditer(
            pattern,
            text,
            re.IGNORECASE,
        ):
            value = match.group(0).strip(
                ".,;:)]}"
            )

            if "@" not in value:
                candidates.append(value)

    if not candidates:
        return None

    candidates.sort(
        key=lambda value: (
            value.lower().startswith("www."),
            len(value),
        ),
        reverse=True,
    )

    return candidates[0]


def extract_ingredients(
    text: str,
) -> str | None:
    patterns = [
        r"\bINGREDIENTS?\s*[:\-]?\s*(.+?)(?="
        r"\bNUTRITION"
        r"|\bSTORE\b"
        r"|\bPRODUCT\s+OF\b"
        r"|\bFOR\s+ALLERGENS\b"
        r"|\bNOT\s+TO\s+BE\s+SOLD\b"
        r"|$)",

        r"\bZUTATEN\s*[:\-]?\s*(.+?)(?="
        r"\bNUTRITION"
        r"|\bSTORE\b"
        r"|\bPRODUCT\s+OF\b"
        r"|$)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if match:
            value = clean_value(
                match.group(1)
            )

            value = re.sub(
                r"\s+",
                " ",
                value,
            )

            if value:
                return value

    return None


def extract_allergen_information(
    text: str,
) -> str | None:
    patterns = [
        r"\bALLERGEN\s+INFORMATION\s*[:\-]?\s*"
        r"(.{1,220}?)(?="
        r"\bNUTRITIONAL\s+INFORMATION\b|"
        r"\bNUTRITION\b|"
        r"\bNET\s*(?:CONTENT|CONTENTS|QTY|QUANTITY|WEIGHT)\b|"
        r"\bMRP\b|$)",

        r"\bFOR\s+ALLERGENS?\s+SEE\s+INGREDIENTS?\s+IN\s+BOLD\b",

        r"\bMAY\s+CONTAIN\s*[:\-]?\s*(.+?)(?="
        r"\bZUTATEN\b|"
        r"\bSTORE\b|"
        r"\bPRODUCT\s+OF\b|"
        r"\bNUTRITION\b|$)",

        r"\bCONTAINS\s+"
        r"((?:MILK|MILK\.|WHEAT|GLUTEN|SOYA|SOY|"
        r"PEANUTS?|NUTS?|ALMOND|CASHEW|SESAME)"
        r"(?:\s*,?\s*(?:MILK|WHEAT|GLUTEN|SOYA|SOY|"
        r"PEANUTS?|NUTS?|ALMOND|CASHEW|SESAME))*)",
    ]

    values = []

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        if match.lastindex:
            value = clean_value(
                match.group(1)
            )

            if not re.search(
                r"\b(?:contains|may\s+contain)\b",
                value,
                re.IGNORECASE,
            ):
                value = (
                    "Contains "
                    + value
                )
        else:
            value = clean_value(
                match.group(0)
            )

        if value:
            values.append(value)

    if values:
        return " | ".join(
            dict.fromkeys(values)
        )

    return None


def extract_storage_instruction(
    text: str,
) -> str | None:
    patterns = [
        r"\bKEEP\s+REFRIGERATED\b"
        r".{0,180}",

        r"\bREFRIGERATED\s+AT\s+"
        r".{0,220}?(\.|"
        r"\bAND\s+CONSUME\b|$)",

        r"\bREFRIGERATE\s+"
        r".{0,220}?(\.|$)",

        r"\bSTORE\s+(?:IN|AT)\s+"
        r".{0,220}?("
        r"\bPRODUCT\s+OF\b|"
        r"\bINGREDIENTS\b|"
        r"\bNUTRITION\b|"
        r"\bCONSUME\b|$)",

        r"\bSTORE\s+IN\s+A\s+COOL\s+AND\s+DRY\s+PLACE\b",

        r"\bSTORE\s+IN\s+A\s+C[O0]OL\s*&?\s*DRY\s+PLACE\b",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        value = clean_value(
            match.group(0)
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        value = re.sub(
            r"\s*(?:PRODUCT\s+OF|INGREDIENTS|NUTRITION)\b.*$",
            "",
            value,
            flags=re.IGNORECASE,
        )

        value = clean_value(
            value
        )

        if value and len(value) <= 260:
            return value

    return None


def extract_nutrition(
    text: str,
) -> dict[str, str]:
    nutrition: dict[str, str] = {}

    def extract_number_after_label(
        labels: list[str],
        max_chars: int = 80,
    ) -> str | None:
        label_pattern = "|".join(
            labels
        )

        pattern = (
            rf"(?:{label_pattern})"
            r"[^0-9]{0,"
            rf"{max_chars}"
            r"}"
            r"(\d+(?:\.\d+)?)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            return None

        return match.group(1)

    field_specs = {
        "energy": (
            [
                r"ENERGY(?:\s*\(?(?:KCAL|KJ)\)?)?",
            ],
            "energy",
        ),
        "fat": (
            [
                r"TOTAL\s+FAT",
                r"\bFAT\b",
            ],
            "g",
        ),
        "saturated_fat": (
            [
                r"SATURATED\s+FAT",
                r"OF\s+WHICH\s+SATURATES",
            ],
            "g",
        ),
        "trans_fat": (
            [
                r"TRANS\s+FAT",
            ],
            "g",
        ),
        "cholesterol": (
            [
                r"CHOLESTEROL",
            ],
            "mg",
        ),
        "carbohydrate": (
            [
                r"CARBOHYDRATE",
            ],
            "g",
        ),
        "sugars": (
            [
                r"TOTAL\s+SUGARS",
                r"\bSUGARS\b",
            ],
            "g",
        ),
        "added_sugars": (
            [
                r"ADDED\s+SUGARS",
            ],
            "g",
        ),
        "protein": (
            [
                r"PROTEIN",
            ],
            "g",
        ),
        "sodium": (
            [
                r"SODIUM",
            ],
            "mg",
        ),
        "calcium": (
            [
                r"CALCIUM",
            ],
            "mg",
        ),
        "vitamin_b12": (
            [
                r"VITAMIN\s+B12",
                r"VITAMIN\s+B\s*12",
            ],
            "ug",
        ),
        "salt": (
            [
                r"\bSALT\b",
            ],
            "g",
        ),
    }

    for field, (
        labels,
        unit,
    ) in field_specs.items():
        number = extract_number_after_label(
            labels
        )

        if number is None:
            continue

        if field == "energy":
            energy_match = re.search(
                r"(?:ENERGY)[^0-9]{0,80}"
                r"(\d+(?:\.\d+)?)"
                r"\s*(KCAL|KJ)?",
                text,
                re.IGNORECASE,
            )

            if energy_match:
                energy_unit = (
                    energy_match.group(2)
                    or "kcal"
                )

                nutrition[field] = (
                    f"{energy_match.group(1)} "
                    f"{energy_unit.lower()}"
                )
        else:
            nutrition[field] = (
                f"{number} {unit}"
            )

    return nutrition


def extract_brand_name(
    detections: list[dict],
    product_name: str | None,
) -> str | None:
    texts = []

    for detection in detections:
        value = clean_value(
            str(
                detection.get(
                    "text",
                    "",
                )
            )
        )

        if value:
            texts.append(value)

    if not texts:
        return None

    # ── Known brands (expandable, generic) ──
    known_brands = [
        # FMCG / Food
        "Amul", "Parle", "Oreo", "Britannia", "Nestle", "Nestlé",
        "Cadbury", "Kellogg's", "Kelloggs", "Maggi", "Bournvita",
        "Horlicks", "Complan", "Dabur", "Patanjali", "Haldiram",
        "Bikaji", "Balaji", "Lays", "Kurkure", "Bingo",
        # Personal Care / Cosmetic
        "Himalaya", "Nivea", "Ponds", "Pond's", "Lakme", "Lakmé",
        "Garnier", "Loreal", "L'Oréal", "Maybelline", "Colgate",
        "Pepsodent", "Dove", "Pears", "Santoor", "Medimix",
        "Mamaearth", "WOW", "Plum", "Biotique", "Forest Essentials",
        "Kama Ayurveda", "VLCC", "Lotus", "Lotus Herbals",
        # Perfume / Deo
        "Beardo", "Wild Stone", "Fogg", "Engage", "Denver",
        "Park Avenue", "Nivea Men", "Axe", "Old Spice", "Bella Vita",
        "Skinn", "Titan Skinn", "Ajmal", "Armaf",
        # Pharma / Health
        "Dettol", "Savlon", "Hansaplast", "Volini", "Moov",
        "Zandu", "Baidyanath", "Zydus",
        # Other
        "GoodFood", "NutriBite",
    ]

    for brand in known_brands:
        for value in texts:
            if re.search(
                rf"\b{re.escape(brand)}\b",
                value,
                re.IGNORECASE,
            ):
                return brand

    product_upper = (
        product_name.upper()
        if product_name
        else ""
    )

    candidates = []

    for index, value in enumerate(
        texts
    ):
        upper = value.upper()

        if product_name and upper in {
            product_upper,
        }:
            continue

        if re.search(
            r"\d|MRP|NET|MILKY|MILK|"
            r"PASTEURISED|PASTEURIZED|"
            r"NUTRITION|INFORMATION|"
            r"ALLERGEN|MANUFACTURED|"
            r"MARKETED|FSSAI|LIC|"
            r"USP|LDPE|GPE|RECYCLABLE|"
            r"SINCE|PROTECTION|SUNSCREEN|LOTION|"
            r"PARFUM|PERFUME|EAU",
            upper,
        ):
            continue

        if not re.fullmatch(
            r"[A-Z][A-Z0-9&' .\-]{1,40}",
            value,
            re.IGNORECASE,
        ):
            continue

        word_count = len(
            re.findall(
                r"[A-Za-z]+",
                value,
            )
        )

        score = 0.0

        if word_count <= 3:
            score += 0.3

        if index < 12:
            score += 0.25

        if value.isupper():
            score += 0.15

        score += min(
            0.3,
            float(
                detection.get(
                    "confidence",
                    0,
                )
            ),
        )

        candidates.append(
            {
                "value": value,
                "score": score,
            }
        )

    if not candidates:
        return None 
    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return candidates[0]["value"]


def extract_usp(
    text: str,
) -> str | None:
    patterns = [
        # USP ₹ : 15.00/ml  or  USP : 15.00/ml
        r"\bUSP\s*[₹]?\s*[:\-]?\s*"
        r"(?:₹|RS\.?|INR)?\s*"
        r"(\d+(?:\.\d+)?\s*/\s*(?:ML|L|G|KG|MG))",

        r"\bUNIT\s+SELLING\s+PRICE\s*[:\-]?\s*"
        r"(?:₹|RS\.?|INR)?\s*"
        r"(\d+(?:\.\d+)?\s*/\s*(?:ML|L|G|KG|MG))",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            value = clean_value(match.group(1))
            value = re.sub(
                r"(?:RS\.?|₹|INR)\s*",
                "Rs. ",
                value,
                flags=re.IGNORECASE,
            )
            return "Rs. " + value.lstrip("Rs. ").strip()

    return None


def extract_product_name(
    detections: list[dict],
) -> str | None:
    candidates = []

    known_brands = {
        "AMUL", "PARLE", "OREO", "BRITANNIA", "NESTLE", "NESTLÉ",
        "CADBURY", "KELLOGG'S", "KELLOGGS", "MAGGI", "BOURNVITA",
        "HORLICKS", "COMPLAN", "DABUR", "PATANJALI", "HALDIRAM",
        "BIKAJI", "BALAJI", "LAYS", "KURKURE", "BINGO",
        "HIMALAYA", "NIVEA", "PONDS", "POND'S", "LAKME", "LAKMÉ",
        "GARNIER", "LOREAL", "L'ORÉAL", "MAYBELLINE", "COLGATE",
        "PEPSODENT", "DOVE", "PEARS", "SANTOOR", "MEDIMIX",
        "MAMAEARTH", "WOW", "PLUM", "BIOTIQUE", "VLCC",
        "LOTUS", "LOTUS HERBALS", "BEARDO", "WILD STONE", "FOGG",
        "ENGAGE", "DENVER", "PARK AVENUE", "AXE", "OLD SPICE",
        "BELLA VITA", "SKINN", "TITAN SKINN", "AJMAL", "ARMAF",
        "DETTOL", "SAVLON", "HANSAPLAST", "VOLINI", "MOOV",
        "ZANDU", "BAIDYANATH", "ZYDUS", "GOODFOOD",
    }

    ignored_words = {
        "MRP", "NET", "QTY", "QUANTITY", "WEIGHT", "CONTENTS",
        "MANUFACTURED", "MANUFACTURER", "MFD", "MFD.", "MANOFACTURED",
        "PACKED", "PACKER", "PKD", "IMPORTED", "IMPORTER", "BEST",
        "BEFORE", "USE", "BY", "CUSTOMER", "CONSUMER", "CARE",
        "HELPLINE", "FEEDBACK", "COMPLAINT", "CONTACT", "MADE", "IN",
        "CONTAINS", "CONTAIN", "TRACES", "INGREDIENTS", "NUTRITIONAL",
        "INFORMATION", "ENERGY", "PROTEIN", "CARBOHYDRATE", "SUGAR",
        "FAT", "TRANS", "SATURATED", "STORE", "COOL", "DRY", "PLACE",
        "BISCUITS", "BATCH", "LIC", "LICENSE", "FSSAI", "USP", "LDPE",
        "GPE", "RECYCLABLE", "SINCE", "SINCE1930", "PROTECTION", "HELPS",
        "PREVENT", "SKIN", "DARKENING", "EVERYDAY", "FROM", "THE", "SUN",
        "NON-GREASY", "FORMULA", "ALL", "TYPES", "FOR", "EXTERNAL",
        "ONLY", "VOL", "VOLUME", "ML", "LTR", "RS", "DIRECTIONS",
        "CAUTION", "PRODUCT", "CATEGORY", "FLAMMABLE", "IGNITION",
        "KEEP", "AWAY", "SOURCES", "WARNING", "NOT", "TO", "BE",
        "SOLD", "WITHOUT", "OUTER", "CARTON", "EXECUTIVE", "TOLL",
        "FREE", "EMAIL", "WEBSITE", "PLOT", "FOOD", "PARK", "SECTOR",
        "HARYANA", "INDIA", "GURUGRAM", "MANESAR",
    }

    forbidden_patterns = [
        r"CUSTOMER\s+CARE",
        r"CONSUMER\s+CARE",
        r"CUSTOMER\s+CARE\s+EXECUTIVE",
        r"FOR\s+CONSUMER",
        r"FOR\s+CUSTOMER",
        r"COMPLAINT",
        r"FEEDBACK",
        r"MANUFACTURED\s*(?:&|AND)?\s*MARKETED",
        r"MANUFACTURED\s+BY",
        r"MARKETED\s+BY",
        r"GOODFOOD\s+FOODS",
        r"INGREDIENTS",
        r"NUTRITION(?:AL)?\s+INFORMATION",
        r"LIC\.?\s*NO",
        r"PRODUCT\s+OF",
        r"MADE\s+IN",
        r"STORE\s+IN",
        r"KEEP\s+AWAY",
        r"SCAN\s+FOR",
    ]

    product_keywords = [
        "SUNSCREEN", "LOTION", "CREAM", "GEL", "SERUM", "SHAMPOO",
        "CONDITIONER", "SOAP", "FACE", "WASH", "BODY", "HAIR", "OIL",
        "BALM", "MOISTURIZER", "PROTECTIVE", "SPF", "PARFUM", "PERFUME",
        "FRAGRANCE", "DEODORANT", "DEO", "BODY SPRAY", "COLOGNE",
        "BISCUIT", "COOKIE", "CHOCOLATE", "CREAM", "FILLED", "MILK",
        "DRINK", "JUICE", "SNACK", "CHIPS", "OREO", "PARLE", "DARK",
        "FANTASY", "CHOCO", "TABLET", "CAPSULE", "SYRUP", "OINTMENT",
        "DROPS",
    ]

    for index, detection in enumerate(detections):
        text = clean_value(str(detection.get("text", "")))
        if not text:
            continue

        try:
            confidence = float(detection.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = 0.0

        upper_text = text.upper()
        words = {w.upper() for w in re.findall(r"[A-Za-z]+", text)}

        if len(text) < 3 or len(text) > 100:
            continue

        if re.fullmatch(r"[\d\s.,:/\-₹]+", text):
            continue

        if words and words.issubset(ignored_words):
            continue

        if upper_text.strip() in known_brands:
            continue

        if any(re.search(pattern, upper_text, re.IGNORECASE) for pattern in forbidden_patterns):
            continue

        if re.search(
            r"\b(?:MRP|NET\s*(?:QTY|QUANTITY|WEIGHT)|MFD|PKD|PACKED|"
            r"MANUFACTURED|IMPORTED|BEST\s+BEFORE|CONTAINS|INGREDIENTS|"
            r"NUTRITIONAL|BATCH|LIC\.?\s*NO|FSSAI|USP|LDPE|GPE|"
            r"RECYCLABLE|DIRECTIONS\s+FOR\s+USE|CAUTION)\b",
            upper_text,
        ):
            continue

        if re.search(r"\d+\s*(?:KG|KGS|G|GM|GMS|MG|ML|L|LTR|PCS?)\b", text, re.IGNORECASE):
            continue

        if "@" in text or re.search(r"\b\d{10,14}\b", text):
            continue

        score = confidence
        word_count = len(re.findall(r"[A-Za-z]+", text))

        if re.search(r"[A-Za-z]", text):
            score += 0.10
        if 2 <= word_count <= 6:
            score += 0.10
        if word_count <= 3:
            score += 0.08
        if index < 20:
            score += 0.08

        for keyword in product_keywords:
            if keyword in upper_text:
                score += 0.35
                break

        if re.fullmatch(r"[A-Z][A-Z0-9&' .\-]{2,60}", text, re.IGNORECASE):
            score += 0.05

        candidates.append({
            "text": text,
            "confidence": confidence,
            "score": score,
            "index": index,
        })

    if not candidates:
        return None

    candidates.sort(key=lambda item: item["index"])

    groups = []
    current = []

    for candidate in candidates:
        if not current:
            current = [candidate]
            continue

        previous = current[-1]
        if candidate["index"] - previous["index"] <= 1:
            current.append(candidate)
        else:
            groups.append(current)
            current = [candidate]

    if current:
        groups.append(current)

    final_candidates = []

    for group in groups:
        group_texts = [item["text"] for item in group]
        combined = clean_value(" ".join(group_texts))

        if len(combined) > 100:
            combined = combined[:100].rsplit(" ", 1)[0]

        if any(re.search(pattern, combined, re.IGNORECASE) for pattern in forbidden_patterns):
            continue

        combined_upper = combined.upper()
        combined_words = {w.upper() for w in re.findall(r"[A-Za-z]+", combined)}

        if combined_words and combined_words.issubset(ignored_words):
            continue

        avg_conf = sum(item["confidence"] for item in group) / len(group)
        avg_score = sum(item["score"] for item in group) / len(group)

        keyword_bonus = 0.0
        if any(keyword in combined_upper for keyword in product_keywords):
            keyword_bonus = 0.30

        brand_prefix_bonus = 0.0
        first_word = combined_words
        if first_word and any(brand not in combined_upper for brand in known_brands):
            brand_prefix_bonus = 0.0

        final_candidates.append({
            "text": combined,
            "confidence": avg_conf,
            "score": avg_score + 0.20 + keyword_bonus + brand_prefix_bonus,
            "index": group[0]["index"],
        })

    final_candidates.extend(candidates)

    unique = []
    seen = set()

    for candidate in final_candidates:
        value = clean_value(candidate["text"])
        if not value:
            continue

        if value.upper() in known_brands:
            continue

        if any(re.search(pattern, value, re.IGNORECASE) for pattern in forbidden_patterns):
            continue

        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)

    if not unique:
        return None

    unique.sort(
        key=lambda item: (
            item["score"],
            item["confidence"],
            len(item["text"]),
        ),
        reverse=True,
    )

    return unique[0]["text"]

def extract_fields(
    detections: list[dict],
) -> dict[str, Any]:
    raw_text = get_search_text(
        detections
    )

    normalized_text = normalize_text(
        raw_text
    )

    net_quantity = extract_net_quantity(
        normalized_text
    )

    nutrition = extract_nutrition(
        normalized_text
    )

    product_name = extract_product_name(
        detections
    )

    extracted = {
        "product_name": product_name,

        "brand_name": extract_brand_name(
            detections,
            product_name,
        ),

        "mrp": extract_mrp(
            normalized_text,
            detections,
        ),

        "net_quantity_value": (
            net_quantity["value"]
            if net_quantity
            else None
        ),

        "net_quantity_unit": (
            net_quantity["unit"]
            if net_quantity
            else None
        ),

        "manufacturer": extract_manufacturer(
            normalized_text
        ),

        "packer": extract_packer(
            normalized_text
        ),

        "importer": extract_importer(
            normalized_text
        ),

        "manufacturing_date": extract_date(
            normalized_text,
            [
                "MANUFACTURED",
                "MANUFACTURING DATE",
                "MFG",
                "MFD",
                "MFG DATE",
                "MFG DT",
                "MFG. DATE",
                "MFD. DATE",
                "MG",
                "MG DATE",
                "MG. DATE",
            ],
        ),

        # NEW: Date range (MFG-EXP)
        "date_range": extract_date_range(
            normalized_text
        ),

        "packing_date": extract_date(
            normalized_text,
            [
                "PACKED",
                "PACKING DATE",
                "PKD",
                "PACK DATE",
                "PACKED DATE",
            ],
        ),

        "best_before": extract_best_before(
            normalized_text
        ),

        "use_by": extract_use_by(
            normalized_text
        ),

        "consumer_care_details": (
            extract_consumer_care(
                normalized_text
            )
        ),

        "country_of_origin": (
            extract_country_of_origin(
                normalized_text
            )
        ),

        "batch_number": extract_batch_number(
            normalized_text
        ),

        "barcode": extract_barcode(
            normalized_text
        ),

        "fssai_license": extract_fssai_license(
            normalized_text
        ),

        "tax_status": extract_tax_status(
            normalized_text
        ),

        "email": extract_email(
            normalized_text
        ),

        "phone": extract_phone(
            normalized_text
        ),

        "website": extract_website(
            normalized_text
        ),

        "usp": extract_usp(
            normalized_text
        ),

        "ingredients": extract_ingredients(
            normalized_text
        ),

        "allergen_information": (
            extract_allergen_information(
                normalized_text
            )
        ),

        "storage_instruction": (
            extract_storage_instruction(
                normalized_text
            )
        ),

        "nutrition": nutrition or None,
    }

    return extracted