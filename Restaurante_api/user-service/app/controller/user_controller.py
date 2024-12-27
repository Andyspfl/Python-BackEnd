from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash

from model.user_model import User
from utils.decorators import jwt_required, roles_required

# Crear el blueprint de usuario
user_bp = Blueprint("user", __name__)

# Ruta para registrar un nuevo usuario
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role")

    if not name or not email or not password or not phone or not role:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Verificar si el correo electrónico ya está registrado
    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 400

    # Crear y guardar el nuevo usuario
    new_user = User(name, email, password, phone, role)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente",
                    "id": new_user.id}), 201, 


# Ruta para el login y generar el token JWT
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Verificar si el usuario existe y si la contraseña es correcta
    user = User.find_by_email(email)
    if user and user.check_password(password):
        # Generar el token JWT si las credenciales son válidas
        access_token = create_access_token(
            identity=user.email,
            additional_claims={"role": user.role}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


# Ruta para obtener el usuario actual (solo si el JWT es válido)
@user_bp.route("/me", methods=["GET"])
@jwt_required
def get_current_user():
    current_user = get_jwt_identity()  # Obtener el email del usuario actual
    current_user_role = get_jwt().get("role")  # Obtener el rol del usuario actual
    return jsonify({"email": current_user, "role": current_user_role}), 200


# Ruta para obtener todos los usuarios (solo accesible para administradores)
@user_bp.route("/users", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_users():
    users = User.query.all()
    return jsonify([{"name": user.name, "email": user.email, "role": user.role} for user in users]), 200


# Ruta para obtener un usuario específico por su ID (solo accesible para administradores)
@user_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_user(id):
    user = User.find_by_id(id)  # Buscar al usuario por su ID

    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
