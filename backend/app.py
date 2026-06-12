from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this


def error_response(message):
    return jsonify({"error": message}), 404


def parse_student_payload(payload, require_name=False, require_course=False):
    if not isinstance(payload, dict):
        return None, "Request body must be valid JSON"

    name = payload.get("name")
    course = payload.get("course")
    mark = payload.get("mark")

    if require_name and (not isinstance(name, str) or not name.strip()):
        return None, "Name is required"

    if require_course and (not isinstance(course, str) or not course.strip()):
        return None, "Course is required"

    if name is not None:
        if not isinstance(name, str) or not name.strip():
            return None, "Name must be a non-empty string"
        name = name.strip()

    if course is not None:
        if not isinstance(course, str) or not course.strip():
            return None, "Course must be a non-empty string"
        course = course.strip()

    if mark is not None:
        if not isinstance(mark, int) or isinstance(mark, bool):
            return None, "Mark must be an integer"
        if mark < 0 or mark > 100:
            return None, "Mark must be between 0 and 100"

    return {"name": name, "course": course, "mark": mark}, None

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    student_data, error = parse_student_payload(
        request.get_json(silent=True),
        require_name=True,
        require_course=True,
    )
    if error:
        return error_response(error)

    created = db.insert_student(
        student_data["name"],
        student_data["course"],
        student_data["mark"],
    )
    return jsonify(created), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    if db.get_student_by_id(student_id) is None:
        return error_response("Student not found")

    student_data, error = parse_student_payload(request.get_json(silent=True))
    if error:
        return error_response(error)

    updated = db.update_student(
        student_id,
        student_data["name"],
        student_data["course"],
        student_data["mark"],
    )
    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)
    if deleted is None:
        return error_response("Student not found")
    return jsonify(deleted), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [student["mark"] for student in students if student.get("mark") is not None]

    if not marks:
        return jsonify({
            "count": 0,
            "average": None,
            "min": None,
            "max": None,
        }), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
