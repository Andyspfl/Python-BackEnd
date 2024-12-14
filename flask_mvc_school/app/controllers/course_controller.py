from flask import Blueprint, jsonify, request
from models.course_model import Course
from utils.decorators import jwt_required, roles_required
from views.course_view import render_course_detail, render_course_list

# Crear un blueprint para el controlador de cursos
course_bp = Blueprint("course", __name__)

# Ruta para obtener la lista de cursos
@course_bp.route("/courses", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher", "student"])
def get_courses():
    courses = Course.get_all()
    return jsonify(render_course_list(courses))

# Ruta para obtener un curso específico por su ID
@course_bp.route("/courses/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher", "student"])
def get_course(id):
    course = Course.get_by_id(id)
    if course:
        return jsonify(render_course_detail(course))
    return jsonify({"error": "Curso no encontrado"}), 404

# Ruta para crear un nuevo curso
@course_bp.route("/courses", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_course():
    data = request.json
    code = data.get("code")
    name = data.get("name")
    description = data.get("description")
    credits = data.get("credits")
    teacher_id = data.get("teacher_id")
    period = data.get("period")
    level = data.get("level")

    # Validación simple de datos de entrada
    if not code or not name or not description or not credits or not teacher_id or not period or not level:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo curso y guardarlo en la base de datos
    course = Course(
        code=code,
        name=name,
        description=description,
        credits=credits,
        teacher_id=teacher_id,
        period=period,
        level=level
    )
    course.save()

    return jsonify(render_course_detail(course)), 201

# Ruta para actualizar un curso existente
@course_bp.route("/courses/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_course(id):
    course = Course.get_by_id(id)

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404

    data = request.json
    code = data.get("code")
    name = data.get("name")
    description = data.get("description")
    credits = data.get("credits")
    teacher_id = data.get("teacher_id")
    period = data.get("period")
    level = data.get("level")

    # Actualizar los datos del curso
    course.update(
        code=code,
        name=name,
        description=description,
        credits=credits,
        teacher_id=teacher_id,
        period=period,
        level=level
    )

    return jsonify(render_course_detail(course))

# Ruta para eliminar un curso existente
@course_bp.route("/courses/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_course(id):
    course = Course.get_by_id(id)

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404

    # Eliminar el curso de la base de datos
    course.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
