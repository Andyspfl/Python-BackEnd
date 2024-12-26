from flask import Blueprint, request, jsonify
import requests
from app.services.auth_service import get_token

bp = Blueprint('restaurant_api', __name__)

RESTAURANT_SERVICE_URL = "http://localhost:5001/api"  # URL del microservicio de restaurantes

@bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{RESTAURANT_SERVICE_URL}/restaurants", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{RESTAURANT_SERVICE_URL}/restaurants/{id}", headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/restaurants', methods=['POST'])
def create_restaurant():
    restaurant = request.json
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{RESTAURANT_SERVICE_URL}/restaurants", json=restaurant, headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id):
    restaurant = request.json
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{RESTAURANT_SERVICE_URL}/restaurants/{id}", json=restaurant, headers=headers)
    return jsonify(response.json()), response.status_code

@bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    token = get_token(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{RESTAURANT_SERVICE_URL}/restaurants/{id}", headers=headers)
    return jsonify({"message": "Restaurante eliminado"}), response.status_code
