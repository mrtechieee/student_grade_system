# Student Grade Management System

A command-line Python application for managing academic records for multiple students.
Built over a structured 5-day development cycle using clean, modular, function-based architecture.

---

## Development Cycle — Complete

| Day | Focus | Status |
|---|---|---|
| Day 1 | Project foundation, data model, student creation, basic display | ✅ |
| Day 2 | Input validation, error handling | ✅ |
| Day 3 | Totals, averages, grade calculation | ✅ |
| Day 4 | Search and reporting | ✅ |
| Day 5 | Final polish, edge-case hardening, full review | ✅ |

---

## Features

| Feature | Description |
|---|---|
| Add Student | Add a student with any number of subjects (1–20) and marks (0–100) |
| Display Students | View all students with totals, averages, and grade letters |
| Search Student | Find a student by name (case-insensitive) |
| Class Report | Class average, top & bottom performer, grade distribution |
| Input Validation | All inputs validated with clear re-prompts on errors |

---

## Running the Application

```bash
python main.py
```

**Requirements:** Python 3.7 or higher · No third-party libraries required.

---

## Running the Unit Tests

```bash
python -m unittest test_suite -v
```

| Module | Test Cases |
|---|---|
| `validators.py` | 26 |
| `calculations.py` | 16 |
| `reports.py` | 17 |
| **Total** | **59** |

All 59 tests pass in under 0.01 seconds — no external libraries required.

---

## Project Structure

```
student-grade-management/
│
├── main.py            # Application logic — menus, I/O helpers, display
├── validators.py      # Pure input validation functions        (Day 2)
├── calculations.py    # Pure calculation functions             (Day 3)
├── reports.py         # Pure search & reporting functions      (Day 4)
├── test_suite.py      # 59-case automated unit test suite
└── README.md
```

### Module Responsibilities

| Module | Question it answers |
|---|---|
| `main.py` | What should the user see and what should they be asked? |
| `validators.py` | Is this input acceptable? |
| `calculations.py` | What do these marks mean? |
| `reports.py` | How do students compare with each other? |

Every module outside `main.py` is pure: no I/O, no global state, no side effects — independently testable.

---

## Data Model

Each student is stored as a dictionary inside a list:

```python
students = [
    {
        "name": "Rahul",
        "subjects": {
            "Mathematics": 85,
            "Python":      92,
            "Physics":     78
        }
    }
]
```

This structure was chosen on Day 1 and remained unchanged through all five days — validation, calculation, and reporting were added purely as layers on top.

---

## Grade Scale

| Average Range | Grade | Label |
|---|---|---|
| 90 – 100 | A+ | Excellent |
| 80 – 89 | A | Very Good |
| 70 – 79 | B | Good |
| 60 – 69 | C | Average |
| 50 – 59 | D | Below Average |
| 0 – 49 | F | Fail |

---

## Validation Rules

| Input | Rules enforced |
|---|---|
| Student name | Not empty · Not duplicate (case-insensitive) |
| Number of subjects | Integer · 1 to 20 inclusive |
| Subject name | Not empty · Not duplicate within student (case-insensitive) |
| Mark | Integer · 0 to 100 inclusive |
| Search query | Not empty · Not whitespace-only |
| Menu choice | Must be 1 to 5 |

All invalid inputs are rejected with a clear message and the prompt is repeated — the application never crashes on bad user input.

---

## Menu

```
========================================
     STUDENT GRADE MANAGEMENT SYSTEM
========================================
  1. Add Student
  2. Display Students
  3. Search Student
  4. Class Report
  5. Exit
========================================
```

---

## Sample Output

### Student Record

```
----------------------------------------
  Student : Rahul
----------------------------------------
  Mathematics           : 85
  Python                : 92
  Physics               : 78
........................................
  Total                 : 255
  Average               : 85.00
  Grade                 : A  (Very Good)
----------------------------------------
```

### Class Report

```
========================================
              CLASS REPORT
========================================

  Total Students  : 7
  Class Average   : 70.79
  Class Grade     : B  (Good)

----------------------------------------
  PERFORMANCE HIGHLIGHTS
----------------------------------------
  [TOP]   Aman
          Avg: 96.50  |  Grade: A+

  [LOW]   Rohit
          Avg: 42.50  |  Grade: F

----------------------------------------
  GRADE DISTRIBUTION
----------------------------------------
  Grade  Label            Count  Bar
  ----------------------------------
  A+     Excellent        1      #
  A      Very Good        2      ##
  B      Good             1      #
  C      Average          1      #
  D      Below Average    1      #
  F      Fail             1      #

========================================
```

---

## Edge Cases Handled

| Scenario | Behaviour |
|---|---|
| Display / Search / Report with no students | Clear "no records" message |
| Search with empty or whitespace-only input | Rejected with error message |
| Class Report with only 1 student | Shows `[ONLY]` block — no misleading top/low split |
| Duplicate student name (case-insensitive) | Rejected during add |
| Duplicate subject within same student | Rejected during add |
| Mark entered as letters (e.g. `abc`) | Rejected with type error message |
| Mark out of range (e.g. `-5` or `101`) | Rejected with range error message |

---

## Known Limitations

| Limitation | Notes |
|---|---|
| No data persistence | All records are stored in memory and lost when the program exits |
| No file import/export | CSV or JSON support is outside this project's scope |
| No GUI or web interface | This is a command-line application by design |

---

## Author

Invexon Project — Student Grade Management System
