from flask import Blueprint, jsonify, request

from app.controllers import course_controller

course_bp = Blueprint("course", __name__)


@course_bp.route("/api/courses", methods=["POST"])
def create_course():
    try:
        data = request.get_json()
        result, status = course_controller.create_course(data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@course_bp.route("/api/courses", methods=["GET"])
def get_courses():
    try:
        result, status = course_controller.get_courses()
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@course_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):
    try:
        result, status = course_controller.get_course(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500


@course_bp.route("/api/courses/<int:id>", methods=["PUT"])
def update_course(id):
    try:
        data = request.get_json()
        result, status = course_controller.update_course(id, data)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500


@course_bp.route("/api/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    try:
        result, status = course_controller.delete_course(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500
