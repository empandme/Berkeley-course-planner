"""Build the student's workbook from a plan.json.

    python3 build_sheet.py PLAN_JSON --out-dir DIR

Exit codes:
    0  the workbook was written; its path is printed on stdout
    2  the plan could not be used (file missing, not JSON, or failed
       validation); one error per line on stderr, nothing written
    3  openpyxl is not installed; one CSV per section was written instead and
       the paths are printed on stdout, one per line

A file that already exists is never overwritten: the new file gets "_2", "_3",
... before its suffix, so a workbook the student has already marked up survives
a re-run.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from cell_text import COLUMNS, SECTION_ORDER, row_values
from plan_validation import validate_plan

EXIT_OK = 0
EXIT_BAD_PLAN = 2
EXIT_CSV_FALLBACK = 3


def _alphanumeric(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", text)


def _file_stem(semester: str, major: str) -> str:
    return f"Course_Plan_{_alphanumeric(semester)}_{_alphanumeric(major)}"


def output_filename(semester: str, major: str) -> str:
    """Course_Plan_<Semester>_<Major>.xlsx, keeping only ASCII letters and digits of each part."""
    return _file_stem(semester, major) + ".xlsx"


def next_free_path(directory: Path, filename: str) -> Path:
    """directory/filename, or the first of name_2.ext, name_3.ext, ... that does not exist."""
    path = directory / filename
    if not path.exists():
        return path
    stem, suffix = Path(filename).stem, Path(filename).suffix
    n = 2
    while True:
        candidate = directory / f"{stem}_{n}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def xlsx_available() -> bool:
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        return False
    return True


def write_csv_fallback(plan: dict, directory: Path) -> list:
    """Write one CSV per section, in section order; return the paths written.

    Same text as the Candidates sheet, minus the student's Pick? column. UTF-8
    with a BOM so Excel reads "·", "—" and "→" correctly. An empty section
    still gets its file, with just the header row.
    """
    stem = _file_stem(plan["run"]["semester"], plan["run"]["major"])
    paths = []
    for key, _title in SECTION_ORDER:
        path = next_free_path(directory, f"{stem}_{key}.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS[1:])
            for row in plan["sections"][key]:
                writer.writerow(row_values(row)[1:])
        paths.append(path)
    return paths


def _read_plan(plan_path: Path):
    """Return (plan, None), or (None, error message) when the file is unusable."""
    try:
        text = plan_path.read_text(encoding="utf-8-sig")
        return json.loads(text), None
    except OSError as e:
        return None, f"{plan_path}: cannot read plan file ({e.strerror})"
    except ValueError as e:  # JSONDecodeError and UnicodeDecodeError
        return None, f"{plan_path}: not valid JSON ({e})"


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        prog="build_sheet.py",
        description="Build the course-plan workbook from a plan.json.",
    )
    parser.add_argument("plan_json", metavar="PLAN_JSON", help="path to plan.json")
    parser.add_argument("--out-dir", required=True, help="folder for the workbook (created if missing)")
    args = parser.parse_args(argv)

    plan, problem = _read_plan(Path(args.plan_json))
    errors = [problem] if problem else validate_plan(plan)
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return EXIT_BAD_PLAN

    out_dir = Path(args.out_dir).absolute()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not xlsx_available():
        for path in write_csv_fallback(plan, out_dir):
            print(path)
        return EXIT_CSV_FALLBACK

    from workbook import build_workbook  # needs openpyxl, so imported only now

    run = plan["run"]
    path = next_free_path(out_dir, output_filename(run["semester"], run["major"]))
    build_workbook(plan).save(path)
    print(path)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
