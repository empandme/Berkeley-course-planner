"""The text of a Candidates row, shared by the workbook and the CSV fallback.

Standard library only: the CSV fallback runs exactly when openpyxl is missing,
so it cannot import anything that imports openpyxl (workbook.py does).
"""

import math

# plan.json section key -> section title, in the order the sections appear.
SECTION_ORDER = [
    ("breadth", "Breadth Courses"),
    ("major", "Major Requirements"),
    ("personal", "Personally Intended Courses"),
    ("decal", "Recommended DeCal Courses"),
]

COLUMNS = [
    "Pick?",
    "Requirement slot",
    "Course number",
    "Title",
    "Units",
    "Instructor",
    "Lecture days/time",
    "Label",
    "Review score",
    "Review notes",
    "Grading",
    "Grade data scope",
    "Also satisfies",
    "Flags",
]


def _review_score_text(row: dict) -> str:
    if "Reviews not checked" in row["flags"]:
        return "Not confirmed"
    if row["review_score"] is None:
        return "—"
    kept = row["reviews_kept"]
    noun = "review" if kept == 1 else "reviews"
    return (
        f"{row['review_score']:.1f}/5 · {kept} {noun} "
        f"({row['reviews_this_course']} this course)"
    )


def _grading_text(row: dict) -> str:
    if row["grading"] in ("Generous", "Strict"):
        # Floor, never round: 39.6 must not read "40%" beside a Strict label
        # when 40 is the Generous threshold.
        return f"{row['grading']} · {math.floor(row['a_range_pct'])}% A-range"
    return row["grading"]


def _review_notes_text(row: dict) -> str:
    lines = []
    if row["review_notes"]:
        lines.append(row["review_notes"])
    if row["reddit_urls"]:
        lines.append("Reddit: " + " ".join(row["reddit_urls"]))
    return "\n".join(lines)


def _instructor_text(row: dict) -> str:
    if "Instructor unconfirmed" in row["flags"]:
        return f"{row['instructor']} (unconfirmed)"
    return row["instructor"]


def row_cells(row: dict) -> list:
    """The 14 (text, hyperlink-or-None) pairs of a candidate row, in COLUMNS order."""
    return [
        (None, None),  # Pick?: the student's to fill
        (row["slot"], None),
        (row["course_number"], row["course_url"]),
        (row["title"], None),
        (row["units"], None),
        (_instructor_text(row), None),
        (row["lecture_time"], None),
        (row["label"], None),
        (_review_score_text(row), row["rmp_url"]),
        (_review_notes_text(row), None),
        (_grading_text(row), row["berkeleytime_url"]),
        (row["grade_scope"], None),
        (", ".join(row["also_satisfies"]), None),
        ("; ".join(row["flags"]), None),
    ]


def row_values(row: dict) -> list:
    """The 14 display values of a candidate row, in COLUMNS order (Pick? is None)."""
    return [text for text, _url in row_cells(row)]
