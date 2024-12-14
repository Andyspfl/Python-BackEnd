from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash

from models.user_model import User
from utils.decorators import jwt_required, roles_required

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods = ["POST"])
def register():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role")
    email = data.get("email")
    
    if not name or not password or not phone or not role or not email:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({"error": "El email ya esta registrado"}), 400
    
    new_user = User(name, password, phone, role, email)
    new_user.save()
    
    return jsonify({"message": "Usuario registrado exitosamente"}), 201


@user_bp.route('/login', methods = ["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    user = User.find_by_email(email)
    if user and user.check_password(password):
        
        access_token = create_access_token(
            identity = {"email": user.email, "role": user.role}
        )
        return jsonify(access_token = access_token), 200
    else:
        return jsonify({"error": "Credenciales invalidas"}), 401
    
@user_bp.route("/me", methods = ["GET"])
@jwt_required
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

@user_bp.route("users", methods = ["GET"])
@jwt_required
@roles_required(roles = ["admin"])
def get_users():
    users = User.query.all()
    return jsonify([{"name": user.name, "email": user.email, "phone": user.phone, "role": user.role} for user in users]), 200
    
