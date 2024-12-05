from flask import Blueprint, jsonify, request
from app.models.student_model import Student  # Asegúrate de que el modelo Student esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.student_view import render_student_detail, render_student_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de estudiantes
student_bp = Blueprint("student", __name__)

# Ruta para obtener la lista de estudiantes
@student_bp.route("/students", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor"])
def get_students():
    students = Student.get_all()
    return jsonify(render_student_list(students))

# Ruta para obtener un estudiante específico por su ID
@student_bp.route("/students/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_student(id):
    student = Student.get_by_id(id)
    if student:
        return jsonify(render_student_detail(student))
    return jsonify({"error": "Estudiante no encontrado"}), 404

# Ruta para crear un nuevo estudiante
@student_bp.route("/students", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_student():
    data = request.json
    usuario_id = data.get("usuario_id")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")
    genero = data.get("genero")
    direccion = data.get("direccion")
    telefono = data.get("telefono")
    email_personal = data.get("email_personal")
    fecha_ingreso = data.get("fecha_ingreso")

    # Validación simple de datos de entrada
    if not usuario_id or not nombre or not apellido or not fecha_nacimiento or not genero or not telefono:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo estudiante y guardarlo en la base de datos
    student = Student(
        usuario_id=usuario_id,
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        direccion=direccion,
        telefono=telefono,
        email_personal=email_personal,
        fecha_ingreso=fecha_ingreso
    )
    student.save()

    return jsonify(render_student_detail(student)), 201

# Ruta para actualizar un estudiante existente
@student_bp.route("/students/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_student(id):
    student = Student.get_by_id(id)

    if not student:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    data = request.json
    usuario_id = data.get("usuario_id")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")
    genero = data.get("genero")
    direccion = data.get("direccion")
    telefono = data.get("telefono")
    email_personal = data.get("email_personal")
    fecha_ingreso = data.get("fecha_ingreso")

    # Actualizar los datos del estudiante
    student.update(
        usuario_id=usuario_id,
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        direccion=direccion,
        telefono=telefono,
        email_personal=email_personal,
        fecha_ingreso=fecha_ingreso
    )

    return jsonify(render_student_detail(student))

# Ruta para eliminar un estudiante existente
@student_bp.route("/students/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_student(id):
    student = Student.get_by_id(id)

    if not student:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    # Eliminar el estudiante de la base de datos
    student.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
