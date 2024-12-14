from flask import Blueprint, jsonify, request
from datetime import datetime
from models.qualification_model import Qualification
from utils.decorators import jwt_required, roles_required
from views.qualification_view import render_qualification_detail, render_qualification_list

# Create a blueprint for the qualifications controller
qualification_bp = Blueprint("qualification", __name__)

# Route to get the list of qualifications
@qualification_bp.route("/qualifications", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "student", "teacher"])
def get_qualifications():
    qualifications = Qualification.get_all()
    return jsonify(render_qualification_list(qualifications))

# Route to get a specific qualification by its ID
@qualification_bp.route("/qualifications/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "student", "teacher"])
def get_qualification(id):
    qualification = Qualification.get_by_id(id)
    if qualification:
        return jsonify(render_qualification_detail(qualification))
    return jsonify({"error": "Calificación no encontrada"}), 404

# Route to create a new qualification
@qualification_bp.route("/qualifications", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def create_qualification():
    data = request.json
    tuition_id = data.get("tuition_id")
    grade = data.get("grade")
    evaluation_type = data.get("evaluation_type")
    evaluation_date = data.get("evaluation_date")

    # Simple validation of required input
    if not tuition_id or not grade or not evaluation_type or not evaluation_date:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        # Handle optional microseconds in the date format
        evaluation_date = datetime.fromisoformat(evaluation_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Create a new qualification and save it to the database
    qualification = Qualification(
        tuition_id=tuition_id,
        grade=grade,
        evaluation_type=evaluation_type,
        evaluation_date=evaluation_date
    )
    qualification.save()

    return jsonify(render_qualification_detail(qualification)), 201

# Route to update an existing qualification
@qualification_bp.route("/qualifications/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def update_qualification(id):
    qualification = Qualification.get_by_id(id)

    if not qualification:
        return jsonify({"error": "Calificación no encontrada"}), 404

    data = request.json
    tuition_id = data.get("tuition_id")
    grade = data.get("grade")
    evaluation_type = data.get("evaluation_type")
    evaluation_date = data.get("evaluation_date")

    try:
        if evaluation_date:
            # Handle optional microseconds in the date format
            evaluation_date = datetime.fromisoformat(evaluation_date.rstrip("Z")).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Update qualification data
    qualification.update(
        tuition_id=tuition_id,
        grade=grade,
        evaluation_type=evaluation_type,
        evaluation_date=evaluation_date
    )

    return jsonify(render_qualification_detail(qualification))

# Route to delete an existing qualification
@qualification_bp.route("/qualifications/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def delete_qualification(id):
    qualification = Qualification.get_by_id(id)

    if not qualification:
        return jsonify({"error": "Calificación no encontrada"}), 404

    # Delete the qualification from the database
    qualification.delete()

    # Empty response with status code 204 (No Content)
    return "", 204
