"""
Flask REST API — Student Database
Supports: GET (all & by ID), POST, PUT, DELETE
"""

from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "students.json")


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_students():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_students(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def find_student(students, student_id):
    return next((s for s in students if s["student_id"] == student_id), None)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/students", methods=["GET"])
def get_all_students():
    """GET /students — Return all students."""
    students = load_students()
    return jsonify({"status": "success", "count": len(students), "data": students}), 200


@app.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """GET /students/<id> — Return a single student."""
    students = load_students()
    student = find_student(students, student_id)
    if not student:
        return jsonify({"status": "error", "message": f"Student '{student_id}' not found"}), 404
    return jsonify({"status": "success", "data": student}), 200


@app.route("/students", methods=["POST"])
def create_student():
    """POST /students — Create a new student."""
    students = load_students()
    body = request.get_json(silent=True)

    if not body:
        return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

    required = ["student_id", "student_name", "years_of_experience", "company_name"]
    missing = [f for f in required if f not in body]
    if missing:
        return jsonify({"status": "error", "message": f"Missing fields: {missing}"}), 400

    if find_student(students, body["student_id"]):
        return jsonify({"status": "error", "message": f"Student ID '{body['student_id']}' already exists"}), 409

    new_student = {
        "student_id":          body["student_id"],
        "student_name":        body["student_name"],
        "years_of_experience": int(body["years_of_experience"]),
        "company_name":        body["company_name"],
    }
    students.append(new_student)
    save_students(students)
    return jsonify({"status": "success", "message": "Student created", "data": new_student}), 201


@app.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    """PUT /students/<id> — Update an existing student (full replace)."""
    students = load_students()
    student = find_student(students, student_id)
    if not student:
        return jsonify({"status": "error", "message": f"Student '{student_id}' not found"}), 404

    body = request.get_json(silent=True)
    if not body:
        return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

    student["student_name"]        = body.get("student_name",        student["student_name"])
    student["years_of_experience"] = int(body.get("years_of_experience", student["years_of_experience"]))
    student["company_name"]        = body.get("company_name",        student["company_name"])

    save_students(students)
    return jsonify({"status": "success", "message": "Student updated", "data": student}), 200


@app.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    """DELETE /students/<id> — Delete a student."""
    students = load_students()
    student = find_student(students, student_id)
    if not student:
        return jsonify({"status": "error", "message": f"Student '{student_id}' not found"}), 404

    students.remove(student)
    save_students(students)
    return jsonify({"status": "success", "message": f"Student '{student_id}' deleted"}), 200


# ── Health check ─────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Flask API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
