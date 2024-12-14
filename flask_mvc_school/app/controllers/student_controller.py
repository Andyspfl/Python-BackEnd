from flask import Blueprint, jsonify, request
from models.student_model import Student  # Asegúrate de que el modelo Student esté correctamente importado
from utils.decorators import jwt_required, roles_required
from views.student_view import render_student_detail, render_student_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de estudiantes
student_bp = Blueprint("student", __name__)

# Ruta para obtener la lista de estudiantes
@student_bp.route("/students", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
def get_students():
    students = Student.get_all()
    return jsonify(render_student_list(students))

# Ruta para obtener un estudiante específico por su ID
@student_bp.route("/students/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "teacher"])
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
    user_id = data.get("user_id")
    gender = data.get("gender")
    birth_date = data.get("birth_date")
    address = data.get("address")
    enrollment_date = data.get("enrollment_date")
    

    # Validación simple de datos de entrada
    if not user_id or not birth_date or not address or not enrollment_date or not gender:
        return jsonify({"error": "Datos de estudiante incompletos"}), 400
    
    # Crear un nuevo estudiante y guardarlo en la base de datos
    student = Student(
        user_id = user_id,
        birth_date = birth_date,
        gender = gender,
        address = address,    
    )

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
    user_id = data.get("user_id")
    birth_date = data.get("birth_date")
    gender = data.get("gender")
    address = data.get("address")

    # Actualizar los datos del estudiante
    student.update(
        user_id = user_id,
        birth_date = birth_date,
        gender = gender,
        address = address
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
