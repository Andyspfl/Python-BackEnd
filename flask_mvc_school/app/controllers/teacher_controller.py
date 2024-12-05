from flask import Blueprint, jsonify, request
from app.models.teacher_model import Teacher  # Asegúrate de que el modelo Teacher esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.teacher_view import render_teacher_detail, render_teacher_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de profesores
teacher_bp = Blueprint("teacher", __name__)

# Ruta para obtener la lista de profesores
@teacher_bp.route("/teachers", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_teachers():
    teachers = Teacher.get_all()
    return jsonify(render_teacher_list(teachers))

# Ruta para obtener un profesor específico por su ID
@teacher_bp.route("/teachers/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def get_teacher(id):
    teacher = Teacher.get_by_id(id)
    if teacher:
        return jsonify(render_teacher_detail(teacher))
    return jsonify({"error": "Profesor no encontrado"}), 404

# Ruta para crear un nuevo profesor
@teacher_bp.route("/teachers", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_teacher():
    data = request.json
    usuario_id = data.get("usuario_id")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    especialidad = data.get("especialidad")
    fecha_contratacion = data.get("fecha_contratacion")
    titulo_academico = data.get("titulo_academico")

    # Validación simple de datos de entrada
    if not usuario_id or not nombre or not apellido or not especialidad or not fecha_contratacion:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo profesor y guardarlo en la base de datos
    teacher = Teacher(
        usuario_id=usuario_id,
        nombre=nombre,
        apellido=apellido,
        especialidad=especialidad,
        fecha_contratacion=fecha_contratacion,
        titulo_academico=titulo_academico
    )
    teacher.save()

    return jsonify(render_teacher_detail(teacher)), 201

# Ruta para actualizar un profesor existente
@teacher_bp.route("/teachers/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_teacher(id):
    teacher = Teacher.get_by_id(id)

    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    data = request.json
    usuario_id = data.get("usuario_id")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    especialidad = data.get("especialidad")
    fecha_contratacion = data.get("fecha_contratacion")
    titulo_academico = data.get("titulo_academico")

    # Actualizar los datos del profesor
    teacher.update(
        usuario_id=usuario_id,
        nombre=nombre,
        apellido=apellido,
        especialidad=especialidad,
        fecha_contratacion=fecha_contratacion,
        titulo_academico=titulo_academico
    )

    return jsonify(render_teacher_detail(teacher))

# Ruta para eliminar un profesor existente
@teacher_bp.route("/teachers/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_teacher(id):
    teacher = Teacher.get_by_id(id)

    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    # Eliminar el profesor de la base de datos
    teacher.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
