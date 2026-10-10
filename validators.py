"""
validators.py
=============
Day 5 — Final reviewed version (no logic changes from Day 2).

Review notes:
    - All four validators confirmed correct and complete.
    - Docstrings verified accurate.
    - No redundant logic found.
    - Whitespace-only names: .strip() is called by callers before passing
      here, so an empty stripped string correctly triggers the empty-name rule.
"""


def validate_student_name(name: str, existing_students: list) -> tuple:
    """Validate a student name against content and uniqueness rules.

    Rules:
        1. Must not be empty (caller must strip before passing).
        2. Must not duplicate an existing student name (case-insensitive).

    Args:
        name:              Stripped name string entered by the user.
        existing_students: The global students list for duplicate detection.

    Returns:
        (True, "")            on success.
        (False, error_reason) on failure.
    """
    if not name:
        return False, "Student name cannot be empty."

    existing_names = [s["name"].lower() for s in existing_students]
    if name.lower() in existing_names:
        return False, f"A student named '{name}' already exists."

    return True, ""


def validate_subject_count(raw: str) -> tuple:
    """Validate the number of subjects entered by the user.

    Rules:
        1. Must be a whole number (no decimals, no letters).
        2. Must be between 1 and 20 inclusive.

    Args:
        raw: Stripped string entered by the user.

    Returns:
        (True, "")            on success.
        (False, error_reason) on failure.
    """
    if not raw.isdigit():
        return False, "Please enter a valid positive whole number."

    count = int(raw)

    if count < 1:
        return False, "Number of subjects must be at least 1."

    if count > 20:
        return False, "Maximum 20 subjects allowed per student."

    return True, ""


def validate_subject_name(name: str, existing_subjects: dict) -> tuple:
    """Validate a subject name against content and uniqueness rules.

    Rules:
        1. Must not be empty (caller must strip before passing).
        2. Must not duplicate a subject already added for this student
           (case-insensitive).

    Args:
        name:              Stripped subject name entered by the user.
        existing_subjects: Subjects already collected for the current student.

    Returns:
        (True, "")            on success.
        (False, error_reason) on failure.
    """
    if not name:
        return False, "Subject name cannot be empty."

    existing = [s.lower() for s in existing_subjects]
    if name.lower() in existing:
        return False, f"'{name}' has already been added for this student."

    return True, ""


def validate_mark(raw: str) -> tuple:
    """Validate a mark string.

    Rules:
        1. Must be convertible to an integer (no decimals, no letters).
        2. Must be in the range 0 to 100 inclusive.

    Args:
        raw: Stripped string entered by the user.

    Returns:
        (True, "")            on success.
        (False, error_reason) on failure.
    """
    try:
        mark = int(raw)
    except ValueError:
        return False, f"'{raw}' is not a valid integer. Enter a whole number."

    if not (0 <= mark <= 100):
        return False, f"Mark must be between 0 and 100. You entered: {mark}."

    return True, ""
