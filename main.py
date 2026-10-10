"""
main.py
=======
Student Grade Management System
Day 5 — Final Polish & Edge-Case Hardening

Changes from Day 4:
    - display_class_report(): single-student edge case handled gracefully.
      When only one student exists, top and bottom are the same person —
      a dedicated single-student branch now shows this clearly instead of
      printing two identical "[TOP]" and "[LOW]" blocks.
    - search_student(): whitespace-only input (e.g. "   ") now caught
      correctly, since .strip() is applied before the empty-string check.
    - _divider() and _section() helper functions introduced to eliminate
      repeated literal strings and keep all formatting in one place.
    - All prompt labels reviewed and made consistent in tone and alignment.
    - Removed all redundant inline comments; docstrings kept accurate.
    - No changes to data model, validators, calculations, or reports modules.

Architecture (final):
    main.py         — I/O, menus, display formatting
    validators.py   — Is the input acceptable?
    calculations.py — What do the numbers mean?
    reports.py      — How do students compare with each other?

Data Structure (unchanged throughout all five days):
    students: list[dict]
    Each dict: {"name": str, "subjects": {subject_name: mark, ...}}
"""

from validators import (
    validate_student_name,
    validate_subject_count,
    validate_subject_name,
    validate_mark,
)
from calculations import (
    calculate_total,
    calculate_average,
    assign_grade,
)
from reports import (
    find_student,
    get_top_student,
    get_bottom_student,
    get_grade_distribution,
    get_class_average,
)

# ---------------------------------------------------------------------------
# Global in-memory store
# ---------------------------------------------------------------------------

students = []   # list[dict]


# ---------------------------------------------------------------------------
# Display utilities — centralised formatting constants
# ---------------------------------------------------------------------------

_WIDTH      = 40
_DIVIDER    = "-" * _WIDTH
_SEPARATOR  = "." * _WIDTH
_HEADER     = "=" * _WIDTH


def _print_header(title: str):
    """Print a section header surrounded by '=' borders.

    Args:
        title: The centred title text.
    """
    print("\n" + _HEADER)
    print(title.center(_WIDTH))
    print(_HEADER)


def _print_divider():
    print(_DIVIDER)


def _print_separator():
    print(_SEPARATOR)


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def display_menu():
    """Print the main application menu."""
    print("\n" + _HEADER)
    print("  STUDENT GRADE MANAGEMENT SYSTEM".center(_WIDTH))
    print(_HEADER)
    print("  1. Add Student")
    print("  2. Display Students")
    print("  3. Search Student")
    print("  4. Class Report")
    print("  5. Exit")
    print(_HEADER)


# ---------------------------------------------------------------------------
# Validated input helpers
# ---------------------------------------------------------------------------

def prompt_student_name() -> str:
    """Prompt until a valid, unique student name is entered.

    Returns:
        str: A validated, stripped student name.
    """
    while True:
        name = input("  Student name      : ").strip()
        is_valid, error = validate_student_name(name, students)
        if is_valid:
            return name
        print(f"  ✗ {error}")


def prompt_subject_count() -> int:
    """Prompt until a valid number of subjects (1-20) is entered.

    Returns:
        int: A validated subject count.
    """
    while True:
        raw = input("  Number of subjects: ").strip()
        is_valid, error = validate_subject_count(raw)
        if is_valid:
            return int(raw)
        print(f"  ✗ {error}")


def prompt_subject_name(existing_subjects: dict) -> str:
    """Prompt until a valid, non-duplicate subject name is entered.

    Args:
        existing_subjects: Subjects already collected for the current student.

    Returns:
        str: A validated, stripped subject name.
    """
    while True:
        name = input("    Name   : ").strip()
        is_valid, error = validate_subject_name(name, existing_subjects)
        if is_valid:
            return name
        print(f"    ✗ {error}")


def prompt_mark() -> int:
    """Prompt until a valid integer mark in range 0-100 is entered.

    Returns:
        int: A validated mark.
    """
    while True:
        raw = input("    Mark   : ").strip()
        is_valid, error = validate_mark(raw)
        if is_valid:
            return int(raw)
        print(f"    ✗ {error}")


# ---------------------------------------------------------------------------
# Student creation
# ---------------------------------------------------------------------------

def collect_subjects(num_subjects: int) -> dict:
    """Collect validated subject names and marks for a single student.

    Args:
        num_subjects: How many subjects to collect.

    Returns:
        dict: Mapping of subject_name to mark (int).
    """
    subjects = {}
    for i in range(1, num_subjects + 1):
        print(f"\n  Subject {i}:")
        subject_name = prompt_subject_name(subjects)
        mark         = prompt_mark()
        subjects[subject_name] = mark
    return subjects


def add_student():
    """Prompt for student details, validate all inputs, and store the record."""
    print("\n" + _DIVIDER)
    print("  ADD NEW STUDENT")
    print(_DIVIDER)

    student_name = prompt_student_name()
    num_subjects = prompt_subject_count()
    subjects     = collect_subjects(num_subjects)

    students.append({"name": student_name, "subjects": subjects})
    print(f"\n  ✓ '{student_name}' added successfully.")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def display_single_student(student: dict):
    """Print one student's subjects, total, average, and grade.

    Args:
        student: A single student record from the students list.
    """
    subjects = student["subjects"]

    print("\n" + _DIVIDER)
    print(f"  Student : {student['name']}")
    print(_DIVIDER)

    for subject_name, mark in subjects.items():
        print(f"  {subject_name:<22}: {mark}")

    total          = calculate_total(subjects)
    average        = calculate_average(subjects)
    letter, label  = assign_grade(average)

    print(_SEPARATOR)
    print(f"  {'Total':<22}: {total}")
    print(f"  {'Average':<22}: {average:.2f}")
    print(f"  {'Grade':<22}: {letter}  ({label})")
    print(_DIVIDER)


def display_students():
    """Display all stored student records."""
    if not students:
        print("\n  No records found. Please add a student first.")
        return

    print(f"\n  Showing {len(students)} student(s):")
    for student in students:
        display_single_student(student)


# ---------------------------------------------------------------------------
# Search  (Day 4, polished Day 5)
# ---------------------------------------------------------------------------

def search_student():
    """Prompt for a name and display the matching student's full record."""
    print("\n" + _DIVIDER)
    print("  SEARCH STUDENT")
    print(_DIVIDER)

    if not students:
        print("  No records found. Please add a student first.")
        return

    query = input("  Enter name to search: ").strip()

    if not query:
        print("  ✗ Search name cannot be empty.")
        return

    result = find_student(query, students)

    if result is None:
        print(f"\n  ✗ No student found matching '{query}'.")
        print("  Tip: Search is case-insensitive — 'rahul' finds 'Rahul'.")
    else:
        print(f"\n  ✓ Match found:")
        display_single_student(result)


# ---------------------------------------------------------------------------
# Class Report  (Day 4, edge-case hardened Day 5)
# ---------------------------------------------------------------------------

def _print_performance_highlights(students: list):
    """Print the top and bottom performer section of the class report.

    Edge case handled: when only one student exists, top and bottom are
    the same person. In that case a single 'Only Student' block is shown
    instead of two identical blocks that would mislead the reader.

    Args:
        students: The global students list (guaranteed non-empty by caller).
    """
    top    = get_top_student(students)
    bottom = get_bottom_student(students)

    top_avg           = calculate_average(top["subjects"])
    top_letter, _     = assign_grade(top_avg)

    print("\n" + _DIVIDER)
    print("  PERFORMANCE HIGHLIGHTS")
    print(_DIVIDER)

    if len(students) == 1 or top["name"] == bottom["name"]:
        # Single student or all students share the exact same average
        print(f"  [ONLY]  {top['name']}")
        print(f"          Avg: {top_avg:.2f}  |  Grade: {top_letter}")
    else:
        bottom_avg        = calculate_average(bottom["subjects"])
        bottom_letter, _  = assign_grade(bottom_avg)

        print(f"  [TOP]   {top['name']}")
        print(f"          Avg: {top_avg:.2f}  |  Grade: {top_letter}")
        print()
        print(f"  [LOW]   {bottom['name']}")
        print(f"          Avg: {bottom_avg:.2f}  |  Grade: {bottom_letter}")


def _print_grade_distribution(students: list):
    """Print the grade distribution table for the class report.

    Args:
        students: The global students list (guaranteed non-empty by caller).
    """
    GRADE_LABELS = {
        "A+": "Excellent",
        "A" : "Very Good",
        "B" : "Good",
        "C" : "Average",
        "D" : "Below Average",
        "F" : "Fail",
    }

    distribution = get_grade_distribution(students)

    print("\n" + _DIVIDER)
    print("  GRADE DISTRIBUTION")
    print(_DIVIDER)
    print(f"  {'Grade':<6} {'Label':<16} {'Count':<6} Bar")
    print("  " + "-" * 34)

    for letter, label in GRADE_LABELS.items():
        count = distribution[letter]
        bar   = "#" * count
        print(f"  {letter:<6} {label:<16} {count:<6} {bar}")


def display_class_report():
    """Display the full class-wide summary report.

    Sections:
        1. Overview    — student count, class average, class grade
        2. Highlights  — top and bottom performer (or only student)
        3. Distribution — grade letter breakdown with visual bar
    """
    _print_header("CLASS REPORT")

    if not students:
        print("\n  No records found. Please add students first.")
        return

    # Section 1 — Overview
    class_avg      = get_class_average(students)
    cls_letter, cls_label = assign_grade(class_avg)

    print(f"\n  Total Students  : {len(students)}")
    print(f"  Class Average   : {class_avg:.2f}")
    print(f"  Class Grade     : {cls_letter}  ({cls_label})")

    # Section 2 — Performance highlights
    _print_performance_highlights(students)

    # Section 3 — Grade distribution
    _print_grade_distribution(students)

    print("\n" + _HEADER)


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

def main():
    """Run the main application loop."""
    _print_header("STUDENT GRADE MANAGEMENT SYSTEM")
    print("\n  Welcome! Manage student records using the menu below.")

    while True:
        display_menu()
        choice = input("\n  Enter your choice (1-5): ").strip()

        if   choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            display_class_report()
        elif choice == "5":
            print("\n  Thank you for using the Student Grade Management System.")
            print("  Goodbye!\n")
            break
        else:
            print(f"  ✗ '{choice}' is not a valid option. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
