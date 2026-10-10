"""
calculations.py
===============
Day 5 — Final reviewed version (no logic changes from Day 3).

Review notes:
    - GRADE_SCALE table confirmed complete and correctly ordered high-to-low.
    - calculate_average() ZeroDivisionError guard confirmed.
    - assign_grade() fallback return confirmed unreachable for valid marks.
    - All docstrings verified accurate.

Grade Scale:
    A+  →  90 – 100   Excellent
    A   →  80 –  89   Very Good
    B   →  70 –  79   Good
    C   →  60 –  69   Average
    D   →  50 –  59   Below Average
    F   →   0 –  49   Fail
"""


GRADE_SCALE = [
    (90, "A+", "Excellent"),
    (80, "A",  "Very Good"),
    (70, "B",  "Good"),
    (60, "C",  "Average"),
    (50, "D",  "Below Average"),
    (0,  "F",  "Fail"),
]


def calculate_total(subjects: dict) -> int:
    """Return the sum of all marks for a student.

    Args:
        subjects: A subject-to-mark dictionary, e.g. {"Math": 85, "English": 90}.

    Returns:
        int: Sum of all mark values.
    """
    return sum(subjects.values())


def calculate_average(subjects: dict) -> float:
    """Return the average mark rounded to two decimal places.

    Args:
        subjects: A subject-to-mark dictionary.

    Returns:
        float: Average mark rounded to 2 dp.
               Returns 0.0 if subjects is empty (guards against ZeroDivisionError).
    """
    if not subjects:
        return 0.0
    return round(sum(subjects.values()) / len(subjects), 2)


def assign_grade(average: float) -> tuple:
    """Return the grade letter and descriptive label for a given average.

    Walks GRADE_SCALE from highest threshold to lowest; first match wins.

    Args:
        average: The student's average mark (expected range: 0.0 – 100.0).

    Returns:
        tuple: (grade_letter: str, grade_label: str)
               e.g. ("A+", "Excellent") or ("F", "Fail").
    """
    for minimum, letter, label in GRADE_SCALE:
        if average >= minimum:
            return letter, label

    return "F", "Fail"     # unreachable for valid marks; defensive fallback
