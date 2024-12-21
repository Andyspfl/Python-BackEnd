from flask import Blueprint, request, jsonify
import requests
from services.auth_service import get_token

bp = Blueprint('reservation_api', __name__)

RESERVATION_SERVICE_URL = "http://localhost:5002/api"  # URL del microservicio de reservas

@bp.route('/reservations', methods=['GET'])
def get_reservations():
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{RESERVATION_SERVICE_URL}/reservations", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/reservations/<int:id>', methods=['GET'])
def get_reservation(id):
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{RESERVATION_SERVICE_URL}/reservations/{id}", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/reservations', methods=['POST'])
def create_reservation():
    reservation = request.json
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{RESERVATION_SERVICE_URL}/reservations", json=reservation, headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/reservations/<int:id>', methods=['PUT'])
def update_reservation(id):
    reservation = request.json
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{RESERVATION_SERVICE_URL}/reservations/{id}", json=reservation, headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{RESERVATION_SERVICE_URL}/reservations/{id}", headers=headers)
    return jsonify({"message": "Reserva eliminada"}), response.status_code
