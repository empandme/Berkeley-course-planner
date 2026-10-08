"""Validate a plan.json dict: JSON Schema first, then cross-field rules.

validate_plan(plan) returns a list of error strings. An empty list means the
plan is valid. Every message starts with the JSON path of the offending field
followed by a colon, for example ``sections.breadth[0].label: ...``.
"""

import json
import math
import re
from pathlib import Path

from jsonschema import Draft202012Validator

# Rubric thresholds (spec section 7).
THRESHOLDS = {"review_mean": 4.0, "min_reviews": 3, "a_range_pct": 40.0}

LABELS = (
    "Recommended (reviews)",
    "Below bar (reviews)",
    "Recommended (grades)",
    "Below bar (grades)",
    "No data",
    "Interest match",
)

# Flags with a fixed text. Two more flags carry a parameter and are matched by
# the patterns below: "Variable units: <range>" and "Conflicts with <COURSE>".
FIXED_FLAGS = (
    "Schedule unconfirmed",
    "Instructor unconfirmed",
    "Reviews not checked",
    "Not confirmed",
    "Check prerequisite",
    "Not yet confirmed",
)

_FLAG_PATTERNS = (
    re.compile(r"Variable units: \S+"),
    re.compile(r"Conflicts with .+"),
)

_SECTIONS = ("breadth", "major", "personal", "decal")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
# The characters openpyxl refuses to write to a cell (its ILLEGAL_CHARACTERS_RE;
# tab, newline and carriage return are allowed). Copied, not imported: this
# module must load without openpyxl, for the CSV fallback.
_CONTROL_CHARACTER = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
_MAX_MESSAGE_CHARS = 200
_KEEP_HEAD, _KEEP_TAIL = 80, 50

_SCHEMA = json.loads(
    Path(__file__).with_name("schema.json").read_text(encoding="utf-8")
)
_VALIDATOR = Draft202012Validator(_SCHEMA)


def expected_label(row: dict) -> str:
    """The label the rubric (section 7 D) gives a non-DeCal row's numbers.

    Requires ``review_score`` whenever ``reviews_kept`` meets the minimum.
    """
    if row["reviews_kept"] >= THRESHOLDS["min_reviews"]:
        if row["review_score"] >= THRESHOLDS["review_mean"]:
            return "Recommended (reviews)"
        return "Below bar (reviews)"
    pct = row["a_range_pct"]
    if pct is None:
        return "No data"
    if pct >= THRESHOLDS["a_range_pct"]:
        return "Recommended (grades)"
    return "Below bar (grades)"


def _expected_grading(pct) -> str:
    if pct is None:
        return "No data"
    return "Generous" if pct >= THRESHOLDS["a_range_pct"] else "Strict"


def _format_path(parts) -> str:
    out = ""
    for part in parts:
        if isinstance(part, int):
            out += f"[{part}]"
        elif _IDENTIFIER.fullmatch(part):
            out += f".{part}" if out else part
        else:
            out += f"[{json.dumps(part)}]"
    return out or "plan"


def _shorten(message: str) -> str:
    """Cut the middle of a long message (e.g. an echoed 501-char string) but
    keep the end, where jsonschema puts its verdict ("... is too long")."""
    if len(message) <= _MAX_MESSAGE_CHARS:
        return message
    return message[:_KEEP_HEAD] + "..." + message[-_KEEP_TAIL:]


def _flag_is_allowed(flag: str) -> bool:
    return flag in FIXED_FLAGS or any(p.fullmatch(flag) for p in _FLAG_PATTERNS)


def _row_errors(path: str, section: str, row: dict) -> list:
    errors = []
    kept = row["reviews_kept"]
    score = row["review_score"]
    flags = row["flags"]

    if kept >= 1 and score is None:
        errors.append(
            f"{path}.review_score: required when reviews_kept is {kept} (at least 1)"
        )
    if kept == 0 and score is not None:
        errors.append(f"{path}.review_score: must be null when reviews_kept is 0")
    if row["reviews_this_course"] > kept:
        errors.append(
            f"{path}.reviews_this_course: {row['reviews_this_course']} is more "
            f"than reviews_kept ({kept})"
        )
    if "Reviews not checked" in flags and kept != 0:
        errors.append(
            f'{path}.reviews_kept: must be 0 when flags include "Reviews not checked"'
        )

    for j, flag in enumerate(flags):
        if not _flag_is_allowed(flag):
            errors.append(
                f"{path}.flags[{j}]: {_shorten(repr(flag))} is not an allowed flag"
            )

    if section == "decal":
        if row["label"] != "Interest match":
            errors.append(f'{path}.label: DeCal rows must be "Interest match"')
        if row["grading"] != "P/NP":
            errors.append(f'{path}.grading: DeCal rows must be "P/NP"')
        return errors

    # With enough reviews but no score the label is undefined; the
    # review_score error above already reports the cause.
    if not (kept >= THRESHOLDS["min_reviews"] and score is None):
        label = expected_label(row)
        if row["label"] != label:
            errors.append(
                f'{path}.label: "{row["label"]}" contradicts the numbers '
                f'(reviews_kept={kept}, review_score={score}, '
                f'a_range_pct={row["a_range_pct"]}); expected "{label}"'
            )

    grading = _expected_grading(row["a_range_pct"])
    if row["grading"] != grading:
        errors.append(
            f'{path}.grading: "{row["grading"]}" does not match '
            f'a_range_pct {row["a_range_pct"]}; expected "{grading}"'
        )
    return errors


def _control_character_message(text: str) -> str:
    """'' if text is clean; otherwise which character and where, escaped so the
    raw character never reaches stderr."""
    match = _CONTROL_CHARACTER.search(text)
    if not match:
        return ""
    return (
        f"contains control character \\x{ord(match.group()):02x} at position "
        f"{match.start()}; remove it"
    )


def _value_errors(node, parts=()) -> list:
    """Strings with a control character and numbers that are NaN or infinite,
    anywhere in the plan. Both can pass the schema, but openpyxl cannot write
    the first and the workbook cannot show the second."""
    errors = []
    if isinstance(node, dict):
        for key, value in node.items():
            problem = _control_character_message(key)
            if problem:
                errors.append(f"{_format_path(parts + (key,))}: the key {problem}")
            errors.extend(_value_errors(value, parts + (key,)))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            errors.extend(_value_errors(value, parts + (i,)))
    elif isinstance(node, str):
        problem = _control_character_message(node)
        if problem:
            errors.append(f"{_format_path(parts)}: {problem}")
    elif isinstance(node, float) and not math.isfinite(node):
        errors.append(f"{_format_path(parts)}: {json.dumps(node)} is not a finite number")
    return errors


def _normalized(text: str) -> str:
    """Case and spacing never make two rows different."""
    return " ".join(text.split()).casefold()


def _duplicate_errors(path: str, section: str, row: dict, seen_rows: dict, seen_decals: dict) -> list:
    """One row per course and instructor; for DeCals, per course, instructor
    and title, because two DeCals of one department can share the other two."""
    number, instructor = row["course_number"], row["instructor"]
    key = (_normalized(number), _normalized(instructor))
    if section != "decal":
        if key in seen_rows:
            return [
                f"{path}: duplicate course_number and instructor "
                f"({number}, {instructor}), already in {seen_rows[key]}; keep one row "
                f"and list the other requirement in also_satisfies"
            ]
        seen_rows[key] = path
        return []

    if key in seen_rows:
        return [
            f"{path}: course_number and instructor ({number}, {instructor}) are "
            f"already in {seen_rows[key]}; a DeCal row goes in sections.decal only "
            f"(rubric.md section E)"
        ]
    decal_key = key + (_normalized(row["title"]),)
    if decal_key in seen_decals:
        return [
            f"{path}: same DeCal as {seen_decals[decal_key]} (course_number, "
            f"instructor and title all match: {number}, {instructor}, {row['title']}). "
            f"If both rows are the same DeCal, keep one row. If they are different "
            f"DeCals, write course_number and instructor as rubric.md section E says"
        ]
    seen_decals[decal_key] = path
    return []


def validate_plan(plan: dict) -> list:
    """Return a list of error messages; an empty list means the plan is valid."""
    schema_errors = sorted(
        (
            (_format_path(e.absolute_path), _shorten(e.message))
            for e in _VALIDATOR.iter_errors(plan)
        )
    )
    errors = [f"{path}: {message}" for path, message in schema_errors]
    errors.extend(_value_errors(plan))
    if errors:
        return errors

    seen_rows, seen_decals = {}, {}
    for section in _SECTIONS:
        for i, row in enumerate(plan["sections"][section]):
            path = f"sections.{section}[{i}]"
            errors.extend(_row_errors(path, section, row))
            errors.extend(_duplicate_errors(path, section, row, seen_rows, seen_decals))
    return errors
