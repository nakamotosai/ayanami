#!/usr/bin/env python3
"""Validate jewelry product parameters before composing XiaoHongShu copy."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

REQUIRED_FIELDS: Dict[str, Union[type, Tuple[type, ...]]] = {
    "product_name": str,
    "materials": (list, str),
    "selling_points": (list, str),
    "price": (int, float, str),
    "target_audience": str,
}

OPTIONAL_ENUMS: Dict[str, Tuple[str, ...]] = {
    "tone": ("elegant", "minimal", "luxury"),
    "length": ("short", "medium", "long"),
}

ADVISORY_FIELDS = [
    "story",
    "occasion",
    "brand_keywords",
    "platform_comments",
    "category",
    "size",
    "metal",
    "gemstone_weight",
    "pearl_diameter",
]

UNIT_RULES = {
    "pearl_diameter": r"\b\d+(?:\.\d+)?\s*mm\b",
    "gemstone_weight": r"\b\d+(?:\.\d+)?\s*ct\b",
    "metal": r"(\b\d{2}K\b|\bPt\s*900\b)",
}


def load_input(path: Optional[str]) -> Dict[str, Any]:
    if path and path != "-":
        data_path = Path(path).expanduser()
        if not data_path.exists():
            raise FileNotFoundError(f"Input file not found: {data_path}")
        raw = data_path.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("No input received from stdin")
    return json.loads(raw)


def validate_type(field: str, value: Any, expected: Union[type, Tuple[type, ...]]) -> Optional[str]:
    if not isinstance(value, expected):
        return f"{field} must be {expected}, got {type(value).__name__}"
    if isinstance(value, str) and not value.strip():
        return f"{field} must not be empty"
    if isinstance(value, list) and not value:
        return f"{field} must contain at least one item"
    return None


def validate_units(payload: Dict[str, Any]) -> list:
    errors = []
    for field, pattern in UNIT_RULES.items():
        if field in payload and isinstance(payload[field], str) and payload[field].strip():
            if not re.search(pattern, payload[field], flags=re.IGNORECASE):
                errors.append(f"{field} unit invalid: {payload[field]}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate structured jewelry parameters before generating XiaoHongShu copy."
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Path to JSON file with the jewelry fields. Use '-' or omit to read from stdin.",
    )
    args = parser.parse_args()

    try:
        payload = load_input(args.input)
    except Exception as exc:
        print(f"❌ Failed to read input: {exc}")
        sys.exit(1)

    errors = []
    for field, expected in REQUIRED_FIELDS.items():
        if field not in payload:
            errors.append(f"Missing required field: {field}")
            continue
        issue = validate_type(field, payload[field], expected)
        if issue:
            errors.append(issue)

    for field, allowed in OPTIONAL_ENUMS.items():
        if field in payload and payload[field] not in allowed:
            errors.append(f"{field} must be one of {allowed}, got {payload[field]}")

    errors.extend(validate_units(payload))

    if errors:
        print("❌ Validation failed")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("✅ Parameters validated")
    summary_keys = list(REQUIRED_FIELDS) + list(OPTIONAL_ENUMS) + ADVISORY_FIELDS
    print("Summary:")
    for key in summary_keys:
        if key in payload and payload[key] is not None:
            print(f"- {key}: {payload[key]}")


if __name__ == "__main__":
    main()
