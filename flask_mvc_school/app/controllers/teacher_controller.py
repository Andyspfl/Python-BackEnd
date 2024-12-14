from flask import Blueprint, jsonify, request
from datetime import datetime
from models.teacher_model import Teacher
from utils.decorators import jwt_required, roles_required
from views.teacher_view import render_teacher_detail, render_teacher_list

# Create a blueprint for the teachers controller
teacher_bp = Blueprint("teacher", __name__)

# Route to get the list of teachers
@teacher_bp.route("/teachers", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def get_teachers():
    teachers = Teacher.get_all()
    return jsonify(render_teacher_list(teachers))

# Route to get a specific teacher by its ID
@teacher_bp.route("/teachers/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def get_teacher(id):
    teacher = Teacher.get_by_id(id)
    if teacher:
        return jsonify(render_teacher_detail(teacher))
    return jsonify({"error": "Profesor no encontrado"}), 404

# Route to create a new teacher
@teacher_bp.route("/teachers", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_teacher():
    data = request.json
    user_id = data.get("user_id")
    speciality = data.get("speciality")
    hiring_date = data.get("hiring_date")
    academic_title = data.get("academic_title")

    # Simple validation of required input
    if not user_id or not speciality or not hiring_date or not academic_title:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        # Handle optional microseconds in the date format
        hiring_date = datetime.fromisoformat(hiring_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Create a new teacher and save it to the database
    teacher = Teacher(
        user_id=user_id,
        speciality=speciality,
        hiring_date=hiring_date,
        academic_title=academic_title
    )
    teacher.save()

    return jsonify(render_teacher_detail(teacher)), 201

# Route to update an existing teacher
@teacher_bp.route("/teachers/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_teacher(id):
    teacher = Teacher.get_by_id(id)

    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    data = request.json
    user_id = data.get("user_id")
    speciality = data.get("speciality")
    hiring_date = data.get("hiring_date")
    academic_title = data.get("academic_title")

    try:
        if hiring_date:
            # Handle optional microseconds in the date format
            hiring_date = datetime.fromisoformat(hiring_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Update teacher data
    teacher.update(
        user_id=user_id,
        speciality=speciality,
        hiring_date=hiring_date,
        academic_title=academic_title
    )

    return jsonify(render_teacher_detail(teacher))

# Route to delete an existing teacher
@teacher_bp.route("/teachers/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_teacher(id):
    teacher = Teacher.get_by_id(id)

    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    # Delete the teacher from the database
    teacher.delete()

    # Empty response with status code 204 (No Content)
    return "", 204
