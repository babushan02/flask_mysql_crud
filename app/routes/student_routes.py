from flask import Blueprint, jsonify, request

from app.controllers import student_controller

student_bp = Blueprint("student", __name__)


@student_bp.route("/api/students", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        result, status = student_controller.create_student(data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@student_bp.route("/api/students", methods=["GET"])
def get_students():
    try:
        result, status = student_controller.get_students()
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@student_bp.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    try:
        result, status = student_controller.get_student(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    try:
        data = request.get_json()
        result, status = student_controller.update_student(id, data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        result, status = student_controller.delete_student(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500
