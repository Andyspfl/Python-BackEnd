from flask import Blueprint, jsonify, request
from app.models.course_model import Course  # Asegúrate de que el modelo Course esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.course_view import render_course_detail, render_course_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de cursos
course_bp = Blueprint("course", __name__)

# Ruta para obtener la lista de cursos
@course_bp.route("/courses", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_courses():
    courses = Course.get_all()
    return jsonify(render_course_list(courses))

# Ruta para obtener un curso específico por su ID
@course_bp.route("/courses/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_course(id):
    course = Course.get_by_id(id)
    if course:
        return jsonify(render_course_detail(course))
    return jsonify({"error": "Curso no encontrado"}), 404

# Ruta para crear un nuevo curso
@course_bp.route("/courses", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def create_course():
    data = request.json
    codigo = data.get("codigo")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    creditos = data.get("creditos")
    profesor_id = data.get("profesor_id")
    periodo = data.get("periodo")
    nivel = data.get("nivel")

    # Validación simple de datos de entrada
    if not codigo or not nombre or not creditos or not profesor_id or not nivel:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo curso y guardarlo en la base de datos
    course = Course(
        codigo=codigo,
        nombre=nombre,
        descripcion=descripcion,
        creditos=creditos,
        profesor_id=profesor_id,
        periodo=periodo,
        nivel=nivel
    )
    course.save()

    return jsonify(render_course_detail(course)), 201

# Ruta para actualizar un curso existente
@course_bp.route("/courses/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def update_course(id):
    course = Course.get_by_id(id)

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404

    data = request.json
    codigo = data.get("codigo")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    creditos = data.get("creditos")
    profesor_id = data.get("profesor_id")
    periodo = data.get("periodo")
    nivel = data.get("nivel")

    # Actualizar los datos del curso
    course.update(
        codigo=codigo,
        nombre=nombre,
        descripcion=descripcion,
        creditos=creditos,
        profesor_id=profesor_id,
        periodo=periodo,
        nivel=nivel
    )

    return jsonify(render_course_detail(course))

# Ruta para eliminar un curso existente
@course_bp.route("/courses/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def delete_course(id):
    course = Course.get_by_id(id)

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404

    # Eliminar el curso de la base de datos
    course.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
