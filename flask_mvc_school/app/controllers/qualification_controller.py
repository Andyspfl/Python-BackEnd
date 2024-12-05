from flask import Blueprint, jsonify, request
from app.models.qualification_model import Qualification  # Asegúrate de que el modelo Qualification esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.qualification_view import render_qualification_detail, render_qualification_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de calificaciones
qualification_bp = Blueprint("qualification", __name__)

# Ruta para obtener la lista de calificaciones
@qualification_bp.route("/qualifications", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_qualifications():
    qualifications = Qualification.get_all()
    return jsonify(render_qualification_list(qualifications))

# Ruta para obtener una calificación específica por su ID
@qualification_bp.route("/qualifications/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_qualification(id):
    qualification = Qualification.get_by_id(id)
    if qualification:
        return jsonify(render_qualification_detail(qualification))
    return jsonify({"error": "Calificación no encontrada"}), 404

# Ruta para crear una nueva calificación
@qualification_bp.route("/qualifications", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def create_qualification():
    data = request.json
    matricula_id = data.get("matricula_id")
    nota = data.get("nota")
    tipo_evaluacion = data.get("tipo_evaluacion")
    fecha_evaluacion = data.get("fecha_evaluacion")

    # Validación simple de datos de entrada
    if not matricula_id or nota is None or not tipo_evaluacion or not fecha_evaluacion:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear una nueva calificación y guardarla en la base de datos
    qualification = Qualification(
        matricula_id=matricula_id,
        nota=nota,
        tipo_evaluacion=tipo_evaluacion,
        fecha_evaluacion=fecha_evaluacion
    )
    qualification.save()

    return jsonify(render_qualification_detail(qualification)), 201

# Ruta para actualizar una calificación existente
@qualification_bp.route("/qualifications/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def update_qualification(id):
    qualification = Qualification.get_by_id(id)

    if not qualification:
        return jsonify({"error": "Calificación no encontrada"}), 404

    data = request.json
    nota = data.get("nota")
    tipo_evaluacion = data.get("tipo_evaluacion")
    fecha_evaluacion = data.get("fecha_evaluacion")

    # Actualizar los datos de la calificación
    qualification.update(
        nota=nota,
        tipo_evaluacion=tipo_evaluacion,
        fecha_evaluacion=fecha_evaluacion
    )

    return jsonify(render_qualification_detail(qualification))

# Ruta para eliminar una calificación existente
@qualification_bp.route("/qualifications/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def delete_qualification(id):
    qualification = Qualification.get_by_id(id)

    if not qualification:
        return jsonify({"error": "Calificación no encontrada"}), 404

    # Eliminar la calificación de la base de datos
    qualification.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
