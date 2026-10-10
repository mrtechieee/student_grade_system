"""
app.py
======
Student Grade Management System — Web Interface
Flask backend that reuses all existing logic modules unchanged.
"""

from flask import Flask, request, jsonify, render_template
from validators   import validate_student_name, validate_subject_count, validate_subject_name, validate_mark
from calculations import calculate_total, calculate_average, assign_grade
from reports      import find_student, get_top_student, get_bottom_student, get_grade_distribution, get_class_average

app = Flask(__name__)

# In-memory store (same model as CLI)
students = []


# ── API routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def api_get_students():
    result = []
    for s in students:
        total   = calculate_total(s["subjects"])
        average = calculate_average(s["subjects"])
        letter, label = assign_grade(average)
        result.append({
            "name":     s["name"],
            "subjects": [{"name": k, "mark": v} for k, v in s["subjects"].items()],
            "total":    total,
            "average":  average,
            "grade":    letter,
            "label":    label,
        })
    return jsonify(result)


@app.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.get_json()
    name     = data.get("name", "").strip()
    subjects = data.get("subjects", [])   # [{"name": str, "mark": str}, ...]

    # Validate student name
    valid, error = validate_student_name(name, students)
    if not valid:
        return jsonify({"ok": False, "error": error}), 400

    # Validate every subject
    seen = {}
    for item in subjects:
        sname = item.get("name", "").strip()
        mark  = str(item.get("mark", "")).strip()

        v, e = validate_subject_name(sname, seen)
        if not v:
            return jsonify({"ok": False, "error": f"Subject '{sname}': {e}"}), 400

        v, e = validate_mark(mark)
        if not v:
            return jsonify({"ok": False, "error": f"Mark for '{sname}': {e}"}), 400

        seen[sname] = int(mark)

    if not seen:
        return jsonify({"ok": False, "error": "At least one subject is required."}), 400

    students.append({"name": name, "subjects": seen})
    return jsonify({"ok": True, "message": f"Student '{name}' added successfully."})


@app.route("/api/search")
def api_search():
    name   = request.args.get("name", "").strip()
    result = find_student(name, students)
    if result is None:
        return jsonify({"ok": False, "error": f"No student found matching '{name}'."}), 404

    s = result
    total   = calculate_total(s["subjects"])
    average = calculate_average(s["subjects"])
    letter, label = assign_grade(average)
    return jsonify({
        "ok":      True,
        "name":    s["name"],
        "subjects":[{"name": k, "mark": v} for k, v in s["subjects"].items()],
        "total":   total,
        "average": average,
        "grade":   letter,
        "label":   label,
    })


@app.route("/api/report")
def api_report():
    if not students:
        return jsonify({"ok": False, "error": "No students found."}), 404

    class_avg     = get_class_average(students)
    cls_letter, cls_label = assign_grade(class_avg)
    top    = get_top_student(students)
    bottom = get_bottom_student(students)

    top_avg      = calculate_average(top["subjects"])
    top_grade, _ = assign_grade(top_avg)

    bot_avg      = calculate_average(bottom["subjects"])
    bot_grade, _ = assign_grade(bot_avg)

    dist = get_grade_distribution(students)

    return jsonify({
        "ok":            True,
        "total_students": len(students),
        "class_average": class_avg,
        "class_grade":   cls_letter,
        "class_label":   cls_label,
        "top": {
            "name":    top["name"],
            "average": top_avg,
            "grade":   top_grade,
            "same_as_bottom": top["name"] == bottom["name"],
        },
        "bottom": {
            "name":    bottom["name"],
            "average": bot_avg,
            "grade":   bot_grade,
        },
        "distribution": dist,
    })


if __name__ == "__main__":
    print("\n  Student Grade Management System — Web Interface")
    print("  ------------------------------------------------")
    print("  Open your browser and visit:")
    print("  http://127.0.0.1:5000\n")
    app.run(debug=False)
