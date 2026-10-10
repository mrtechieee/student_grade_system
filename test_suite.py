"""
test_suite.py
=============
Student Grade Management System — Unit Test Suite

Tests every pure function in:
    validators.py      — 18 test cases
    calculations.py    — 13 test cases
    reports.py         — 12 test cases

Total: 43 test cases

Run with:
    python test_suite.py
    python -m unittest test_suite -v        (verbose output)

Design notes:
    - Only pure functions are unit-tested here; main.py's I/O functions
      require integration testing (manual or with mock inputs).
    - Each test class maps 1-to-1 with a source module.
    - Test method names follow the pattern:
          test_<function>_<scenario>
      so failures immediately identify both the function and the case.
"""

import unittest

from validators    import (validate_student_name, validate_subject_count,
                           validate_subject_name,  validate_mark)
from calculations  import (calculate_total, calculate_average, assign_grade)
from reports       import (find_student, get_top_student, get_bottom_student,
                           get_grade_distribution, get_class_average)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_student(name: str, **subjects) -> dict:
    """Build a student dict matching the application's data model."""
    return {"name": name, "subjects": dict(subjects)}


# ─────────────────────────────────────────────────────────────────────────────
# validators.py
# ─────────────────────────────────────────────────────────────────────────────

class TestValidateStudentName(unittest.TestCase):

    def setUp(self):
        self.students = [
            _make_student("Rahul", Mathematics=85),
            _make_student("Priya", English=90),
        ]

    def test_valid_name_accepted(self):
        valid, msg = validate_student_name("Aman", self.students)
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_empty_name_rejected(self):
        valid, msg = validate_student_name("", self.students)
        self.assertFalse(valid)
        self.assertIn("empty", msg.lower())

    def test_duplicate_exact_case_rejected(self):
        valid, msg = validate_student_name("Rahul", self.students)
        self.assertFalse(valid)
        self.assertIn("already exists", msg)

    def test_duplicate_lower_case_rejected(self):
        valid, msg = validate_student_name("rahul", self.students)
        self.assertFalse(valid)

    def test_duplicate_upper_case_rejected(self):
        valid, msg = validate_student_name("PRIYA", self.students)
        self.assertFalse(valid)

    def test_no_existing_students(self):
        valid, msg = validate_student_name("NewStudent", [])
        self.assertTrue(valid)


class TestValidateSubjectCount(unittest.TestCase):

    def test_valid_count_accepted(self):
        valid, msg = validate_subject_count("3")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_count_one_accepted(self):
        valid, msg = validate_subject_count("1")
        self.assertTrue(valid)

    def test_count_twenty_accepted(self):
        valid, msg = validate_subject_count("20")
        self.assertTrue(valid)

    def test_count_zero_rejected(self):
        valid, msg = validate_subject_count("0")
        self.assertFalse(valid)

    def test_count_above_twenty_rejected(self):
        valid, msg = validate_subject_count("21")
        self.assertFalse(valid)
        self.assertIn("20", msg)

    def test_letters_rejected(self):
        valid, msg = validate_subject_count("abc")
        self.assertFalse(valid)

    def test_decimal_rejected(self):
        valid, msg = validate_subject_count("2.5")
        self.assertFalse(valid)

    def test_negative_rejected(self):
        valid, msg = validate_subject_count("-1")
        self.assertFalse(valid)


class TestValidateSubjectName(unittest.TestCase):

    def setUp(self):
        self.existing = {"Mathematics": 85, "English": 90}

    def test_valid_subject_accepted(self):
        valid, msg = validate_subject_name("Physics", self.existing)
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_empty_subject_rejected(self):
        valid, msg = validate_subject_name("", self.existing)
        self.assertFalse(valid)
        self.assertIn("empty", msg.lower())

    def test_duplicate_exact_case_rejected(self):
        valid, msg = validate_subject_name("Mathematics", self.existing)
        self.assertFalse(valid)

    def test_duplicate_different_case_rejected(self):
        valid, msg = validate_subject_name("mathematics", self.existing)
        self.assertFalse(valid)

    def test_no_existing_subjects(self):
        valid, msg = validate_subject_name("History", {})
        self.assertTrue(valid)


class TestValidateMark(unittest.TestCase):

    def test_valid_mark_accepted(self):
        valid, msg = validate_mark("75")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_boundary_zero_accepted(self):
        valid, msg = validate_mark("0")
        self.assertTrue(valid)

    def test_boundary_hundred_accepted(self):
        valid, msg = validate_mark("100")
        self.assertTrue(valid)

    def test_negative_mark_rejected(self):
        valid, msg = validate_mark("-1")
        self.assertFalse(valid)
        self.assertIn("0 and 100", msg)

    def test_above_hundred_rejected(self):
        valid, msg = validate_mark("101")
        self.assertFalse(valid)

    def test_letters_rejected(self):
        valid, msg = validate_mark("abc")
        self.assertFalse(valid)
        self.assertIn("not a valid integer", msg)

    def test_decimal_rejected(self):
        valid, msg = validate_mark("85.5")
        self.assertFalse(valid)

    def test_empty_string_rejected(self):
        valid, msg = validate_mark("")
        self.assertFalse(valid)


# ─────────────────────────────────────────────────────────────────────────────
# calculations.py
# ─────────────────────────────────────────────────────────────────────────────

class TestCalculateTotal(unittest.TestCase):

    def test_single_subject(self):
        self.assertEqual(calculate_total({"Maths": 80}), 80)

    def test_multiple_subjects(self):
        subjects = {"Maths": 80, "English": 90, "Physics": 70}
        self.assertEqual(calculate_total(subjects), 240)

    def test_boundary_marks(self):
        subjects = {"Min": 0, "Max": 100}
        self.assertEqual(calculate_total(subjects), 100)


class TestCalculateAverage(unittest.TestCase):

    def test_single_subject(self):
        self.assertEqual(calculate_average({"Maths": 80}), 80.0)

    def test_multiple_subjects(self):
        subjects = {"A": 90, "B": 80, "C": 70}
        self.assertAlmostEqual(calculate_average(subjects), 80.0, places=2)

    def test_non_round_average(self):
        subjects = {"A": 100, "B": 99, "C": 98}
        self.assertAlmostEqual(calculate_average(subjects), 99.0, places=2)

    def test_two_decimal_precision(self):
        subjects = {"A": 100, "B": 0, "C": 0}
        self.assertAlmostEqual(calculate_average(subjects), 33.33, places=2)

    def test_empty_subjects_returns_zero(self):
        self.assertEqual(calculate_average({}), 0.0)


class TestAssignGrade(unittest.TestCase):

    def test_grade_a_plus(self):
        letter, label = assign_grade(95.0)
        self.assertEqual(letter, "A+")
        self.assertEqual(label, "Excellent")

    def test_grade_a_plus_boundary(self):
        letter, _ = assign_grade(90.0)
        self.assertEqual(letter, "A+")

    def test_grade_a(self):
        letter, label = assign_grade(85.0)
        self.assertEqual(letter, "A")
        self.assertEqual(label, "Very Good")

    def test_grade_b(self):
        letter, label = assign_grade(75.0)
        self.assertEqual(letter, "B")
        self.assertEqual(label, "Good")

    def test_grade_c(self):
        letter, label = assign_grade(65.0)
        self.assertEqual(letter, "C")
        self.assertEqual(label, "Average")

    def test_grade_d(self):
        letter, label = assign_grade(55.0)
        self.assertEqual(letter, "D")
        self.assertEqual(label, "Below Average")

    def test_grade_f(self):
        letter, label = assign_grade(40.0)
        self.assertEqual(letter, "F")
        self.assertEqual(label, "Fail")

    def test_grade_f_boundary_zero(self):
        letter, _ = assign_grade(0.0)
        self.assertEqual(letter, "F")


# ─────────────────────────────────────────────────────────────────────────────
# reports.py
# ─────────────────────────────────────────────────────────────────────────────

class TestFindStudent(unittest.TestCase):

    def setUp(self):
        self.students = [
            _make_student("Rahul",  Mathematics=85, English=90),
            _make_student("Priya",  Biology=72,     Chemistry=68),
            _make_student("Karan",  Science=99,     Maths=98),
        ]

    def test_found_exact_case(self):
        result = find_student("Rahul", self.students)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Rahul")

    def test_found_lower_case(self):
        result = find_student("rahul", self.students)
        self.assertIsNotNone(result)

    def test_found_upper_case(self):
        result = find_student("KARAN", self.students)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Karan")

    def test_not_found_returns_none(self):
        result = find_student("Ghost", self.students)
        self.assertIsNone(result)

    def test_empty_list_returns_none(self):
        result = find_student("Rahul", [])
        self.assertIsNone(result)


class TestGetTopAndBottomStudent(unittest.TestCase):

    def setUp(self):
        self.students = [
            _make_student("Low",    Maths=20),
            _make_student("Mid",    Maths=60),
            _make_student("High",   Maths=95),
        ]

    def test_top_student_correct(self):
        top = get_top_student(self.students)
        self.assertEqual(top["name"], "High")

    def test_bottom_student_correct(self):
        bottom = get_bottom_student(self.students)
        self.assertEqual(bottom["name"], "Low")

    def test_top_empty_returns_none(self):
        self.assertIsNone(get_top_student([]))

    def test_bottom_empty_returns_none(self):
        self.assertIsNone(get_bottom_student([]))

    def test_single_student_same_top_and_bottom(self):
        single = [_make_student("Solo", Maths=75)]
        self.assertEqual(get_top_student(single)["name"], "Solo")
        self.assertEqual(get_bottom_student(single)["name"], "Solo")


class TestGetGradeDistribution(unittest.TestCase):

    def setUp(self):
        self.students = [
            _make_student("S1", Maths=95),   # A+
            _make_student("S2", Maths=85),   # A
            _make_student("S3", Maths=75),   # B
            _make_student("S4", Maths=65),   # C
            _make_student("S5", Maths=55),   # D
            _make_student("S6", Maths=40),   # F
        ]

    def test_all_six_bands_present(self):
        dist = get_grade_distribution(self.students)
        for grade in ("A+", "A", "B", "C", "D", "F"):
            self.assertIn(grade, dist)

    def test_each_band_count_correct(self):
        dist = get_grade_distribution(self.students)
        for grade in ("A+", "A", "B", "C", "D", "F"):
            self.assertEqual(dist[grade], 1)

    def test_empty_list_all_zeros(self):
        dist = get_grade_distribution([])
        self.assertTrue(all(v == 0 for v in dist.values()))


class TestGetClassAverage(unittest.TestCase):

    def test_class_average_correct(self):
        students = [
            _make_student("A", Maths=100),
            _make_student("B", Maths=80),
            _make_student("C", Maths=60),
        ]
        # individual averages: 100, 80, 60 → class average = 80.0
        self.assertAlmostEqual(get_class_average(students), 80.0, places=2)

    def test_empty_list_returns_zero(self):
        self.assertEqual(get_class_average([]), 0.0)

    def test_single_student(self):
        students = [_make_student("Solo", Maths=73, English=77)]
        # average = 75.0
        self.assertAlmostEqual(get_class_average(students), 75.0, places=2)


# ─────────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
