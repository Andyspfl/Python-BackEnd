from flask import Blueprint, jsonify, request
from app.models.tuition_model import Tuition  # Asegúrate de que el modelo Tuition esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.tuition_view import render_tuition_detail, render_tuition_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de matrículas
tuition_bp = Blueprint("tuition", __name__)

# Ruta para obtener la lista de matrículas
@tuition_bp.route("/tuitions", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "estudiante", "profesor"])
def get_tuitions():
    tuitions = Tuition.get_all()
    return jsonify(render_tuition_list(tuitions))

# Ruta para obtener una matrícula específica por su ID
@tuition_bp.route("/tuitions/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "estudiante", "profesor"])
def get_tuition(id):
    tuition = Tuition.get_by_id(id)
    if tuition:
        return jsonify(render_tuition_detail(tuition))
    return jsonify({"error": "Matrícula no encontrada"}), 404

# Ruta para crear una nueva matrícula
@tuition_bp.route("/tuitions", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "estudiante"])
def create_tuition():
    data = request.json
    estudiante_id = data.get("estudiante_id")
    curso_id = data.get("curso_id")
    estado = data.get("estado")

    # Validación simple de datos de entrada
    if not estudiante_id or not curso_id:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear una nueva matrícula y guardarla en la base de datos
    tuition = Tuition(
        estudiante_id=estudiante_id,
        curso_id=curso_id,
        estado=estado
    )
    tuition.save()

    return jsonify(render_tuition_detail(tuition)), 201

# Ruta para actualizar una matrícula existente
@tuition_bp.route("/tuitions/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "estudiante"])
def update_tuition(id):
    tuition = Tuition.get_by_id(id)

    if not tuition:
        return jsonify({"error": "Matrícula no encontrada"}), 404

    data = request.json
    estado = data.get("estado")

    # Actualizar el estado de la matrícula
    tuition.update(estado=estado)

    return jsonify(render_tuition_detail(tuition))

# Ruta para eliminar una matrícula existente
@tuition_bp.route("/tuitions/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "estudiante"])
def delete_tuition(id):
    tuition = Tuition.get_by_id(id)

    if not tuition:
        return jsonify({"error": "Matrícula no encontrada"}), 404

    # Eliminar la matrícula de la base de datos
    tuition.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
