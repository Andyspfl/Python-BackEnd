from flask import Blueprint, jsonify, request
from app.models.user_model import User  # Asegúrate de que el modelo User esté correctamente importado
from app.utils.decorators import jwt_required, roles_required
from app.views.user_view import render_user_detail, render_user_list  # Asegúrate de que estas funciones de vista existan y estén correctamente importadas

# Crear un blueprint para el controlador de usuarios
user_bp = Blueprint("user", __name__)

# Ruta para obtener la lista de usuarios
@user_bp.route("/users", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_users():
    users = User.get_all()
    return jsonify(render_user_list(users))

# Ruta para obtener un usuario específico por su ID
@user_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "profesor", "estudiante"])
def get_user(id):
    user = User.get_by_id(id)
    if user:
        return jsonify(render_user_detail(user))
    return jsonify({"error": "Usuario no encontrado"}), 404

# Ruta para crear un nuevo usuario
@user_bp.route("/users", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    tipo_usuario = data.get("tipo_usuario")
    activo = data.get("activo", True)

    # Validación simple de datos de entrada
    if not username or not email or not password or not tipo_usuario:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo usuario y guardarlo en la base de datos
    user = User(
        username=username,
        email=email,
        password=password,
        tipo_usuario=tipo_usuario,
        activo=activo
    )
    user.save()

    return jsonify(render_user_detail(user)), 201

# Ruta para actualizar un usuario existente
@user_bp.route("/users/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_user(id):
    user = User.get_by_id(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    tipo_usuario = data.get("tipo_usuario")
    activo = data.get("activo")

    # Actualizar los datos del usuario
    user.update(
        username=username,
        email=email,
        password=password,
        tipo_usuario=tipo_usuario,
        activo=activo
    )

    return jsonify(render_user_detail(user))

# Ruta para eliminar un usuario existente
@user_bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_user(id):
    user = User.get_by_id(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Eliminar el usuario de la base de datos
    user.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
