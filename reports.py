"""
reports.py
==========
Day 5 — Final reviewed version.

Changes from Day 4:
    - get_class_average() return type annotation corrected to float.
    - All docstrings verified accurate.
    - No logic changes required.

Design principle:
    Pure functions only — no I/O, no global state, no side effects.
    main.py handles all printing; this module handles all data logic.
"""

from calculations import calculate_average, assign_grade


def find_student(name: str, students: list) -> dict | None:
    """Search for a student by name using case-insensitive matching.

    Args:
        name:     Stripped name string to search for.
        students: The global students list.

    Returns:
        The matching student dict, or None if not found.
    """
    name_lower = name.lower()
    for student in students:
        if student["name"].lower() == name_lower:
            return student
    return None


def get_top_student(students: list) -> dict | None:
    """Return the student with the highest average mark.

    When two students share the same average, the one added first wins
    (stable sort — preserves insertion order).

    Args:
        students: The global students list.

    Returns:
        The student dict with the highest average, or None if list is empty.
    """
    if not students:
        return None
    return max(students, key=lambda s: calculate_average(s["subjects"]))


def get_bottom_student(students: list) -> dict | None:
    """Return the student with the lowest average mark.

    When two students share the same average, the one added first wins.

    Args:
        students: The global students list.

    Returns:
        The student dict with the lowest average, or None if list is empty.
    """
    if not students:
        return None
    return min(students, key=lambda s: calculate_average(s["subjects"]))


def get_grade_distribution(students: list) -> dict:
    """Count how many students achieved each grade letter.

    All six grade letters are always present in the result (defaulting to 0),
    so the report layout is consistent regardless of how many students exist.

    Args:
        students: The global students list.

    Returns:
        dict: Mapping of grade_letter -> count, e.g. {"A+": 2, "A": 3, ...}.
    """
    distribution = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for student in students:
        average = calculate_average(student["subjects"])
        letter, _ = assign_grade(average)
        distribution[letter] += 1
    return distribution


def get_class_average(students: list) -> float:
    """Return the mean of all students' individual averages.

    Args:
        students: The global students list.

    Returns:
        float: Class-wide average rounded to 2 dp, or 0.0 if no students.
    """
    if not students:
        return 0.0
    total = sum(calculate_average(s["subjects"]) for s in students)
    return round(total / len(students), 2)
