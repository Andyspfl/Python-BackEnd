from flask import Blueprint, jsonify, request
from datetime import datetime
from models.tuition_model import Tuition
from utils.decorators import jwt_required, roles_required
from views.tuition_view import render_tuition_detail, render_tuition_list

# Create a blueprint for the tuitions controller
tuition_bp = Blueprint("tuition", __name__)

# Route to get the list of tuitions
@tuition_bp.route("/tuitions", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "student", "teacher"])
def get_tuitions():
    tuitions = Tuition.get_all()
    return jsonify(render_tuition_list(tuitions))

# Route to get a specific tuition by its ID
@tuition_bp.route("/tuitions/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "student", "teacher"])
def get_tuition(id):
    tuition = Tuition.get_by_id(id)
    if tuition:
        return jsonify(render_tuition_detail(tuition))
    return jsonify({"error": "Matrícula no encontrada"}), 404

# Route to create a new tuition
@tuition_bp.route("/tuitions", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "student"])
def create_tuition():
    data = request.json
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    enrollment_date = data.get("enrollment_date")
    status = data.get("status")

    # Simple validation of required input
    if not student_id or not course_id or not enrollment_date or not status:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        # Handle optional microseconds in the date format
        enrollment_date = datetime.fromisoformat(enrollment_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Create a new tuition and save it to the database
    tuition = Tuition(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=enrollment_date,
        status=status
    )
    tuition.save()

    return jsonify(render_tuition_detail(tuition)), 201

# Route to update an existing tuition
@tuition_bp.route("/tuitions/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "student"])
def update_tuition(id):
    tuition = Tuition.get_by_id(id)

    if not tuition:
        return jsonify({"error": "Matrícula no encontrada"}), 404

    data = request.json
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    enrollment_date = data.get("enrollment_date")
    status = data.get("status")

    try:
        if enrollment_date:
            # Handle optional microseconds in the date format
            enrollment_date = datetime.fromisoformat(enrollment_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Update tuition data
    tuition.update(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=enrollment_date,
        status=status
    )

    return jsonify(render_tuition_detail(tuition))

# Route to delete an existing tuition
@tuition_bp.route("/tuitions/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "student"])
def delete_tuition(id):
    tuition = Tuition.get_by_id(id)

    if not tuition:
        return jsonify({"error": "Matrícula no encontrada"}), 404

    # Delete the tuition from the database
    tuition.delete()

    # Empty response with status code 204 (No Content)
    return "", 204
