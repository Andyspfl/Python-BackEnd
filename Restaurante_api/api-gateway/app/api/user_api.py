from flask import Blueprint, request, jsonify
import requests
from app.services.auth_service import get_token

bp = Blueprint('user_api', __name__)

USER_SERVICE_URL = "http://localhost:5000/api"  # URL del microservicio de usuarios

@bp.route('/register', methods=['POST'])
def register_user():
    user = request.json
    response = requests.post(f"{USER_SERVICE_URL}/register", json=user)
    return jsonify(response.json()), response.status_code

@bp.route('/login', methods=['POST'])
def login_user():
    credentials = request.json
    response = requests.post(f"{USER_SERVICE_URL}/login", json=credentials)
    return jsonify(response.json()), response.status_code

@bp.route('/me', methods=['GET'])
def get_user_profile():
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{USER_SERVICE_URL}/me", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/users', methods=['GET'])
def get_users():
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{USER_SERVICE_URL}/users", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{USER_SERVICE_URL}/users/{id}", headers=headers)
    return jsonify(response.json()), response.status_code
