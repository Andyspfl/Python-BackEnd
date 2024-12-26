from flask import Blueprint, jsonify, request
from app.services.reservation_service import create_reservation_service, get_reservation_service, update_reservation_service, delete_reservation_service
from app.utils.decorators import jwt_required, roles_required
from app.view.reservation_view import render_reservation_detail, render_reservation_list
import requests
# Crear un blueprint para el controlador de reservas
reservation_bp = Blueprint('reservation', __name__)

# Creacion de las rutas para validar la creacion y actualizacion de reservas
USER_SERVICE_URL = "http://localhost:5000/api/users"
RESTAURANT_SERVICE_URL = "http://localhost:5001/api/restaurants"

# Ruta para obtener la lista de reservas
@reservation_bp.route('/reservations', methods=['GET'])
@jwt_required
@roles_required(roles=['admin', 'user'])
def get_reservations():
    # Obtener todas las reservas
    reservations = get_reservation_service()
    return jsonify(render_reservation_list(reservations))

# Ruta para obtener una reserva específica por su ID
@reservation_bp.route('/reservations/<int:id>', methods=['GET'])
@jwt_required
@roles_required(roles=['admin', 'user'])
def get_reservation(id):
    reservation = get_reservation_service(id)
    if reservation:
        return jsonify(render_reservation_detail(reservation))
    return jsonify({"error": "Reserva no encontrada"}), 404

# Ruta para crear una nueva reserva
@reservation_bp.route('/reservations', methods=['POST'])
@jwt_required
@roles_required(roles=['admin', 'user'])
def create_reservation():
    data = request.json
    jwt_token = request.headers.get("Authorization").split(" ")[1]  # Extraer el token JWT
    
    # Validar la existencia del usuario
    user_response = requests.get(f"{USER_SERVICE_URL}/{data.get("user_id")}", headers={"Authorization": f"Bearer {jwt_token}"})
    
    if user_response.status_code != 200:
        return jsonify({"error": "Ususario no encontrado"}), 400
    
    restaurant_response = requests.get(f"{RESTAURANT_SERVICE_URL}/{data.get("restaurant_id")}", headers = {"Authorization": f"Bearer {jwt_token}"})
    
    if restaurant_response.status_code != 200:
        return jsonify({"error": "Restaurante no encontrado"}), 400
    
    try:
        reservation = create_reservation_service(data)
        return jsonify(render_reservation_detail(reservation)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Ruta para actualizar una reserva
@reservation_bp.route('/reservations/<int:id>', methods=['PUT'])
@jwt_required
@roles_required(roles=['admin', 'user'])
def update_reservation(id):
    data = request.json
    jwt_token = request.headers.get("Authorization").split(" ")[1]  # Extraer el token JWT
    
    # Validar la existencia del usuario
    user_response = requests.get(f"{USER_SERVICE_URL}/{data.get("user_id")}", headers={"Authorization": f"Bearer {jwt_token}"})
    
    if user_response.status_code != 200:
        return jsonify({"error": "Ususario no encontrado"}), 400
    
    restaurant_response = requests.get(f"{RESTAURANT_SERVICE_URL}/{data.get("restaurant_id")}", headers = {"Authorization": f"Bearer {jwt_token}"})
    
    if restaurant_response.status_code != 200:
        return jsonify({"error": "Restaurante no encontrado"}), 400
    print("aqui llegue :c")
    try:
        reservation = update_reservation_service(id, data)
        return jsonify(render_reservation_detail(reservation))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Ruta para eliminar una reserva existente
@reservation_bp.route('/reservations/<int:id>', methods=['DELETE'])
@jwt_required
@roles_required(roles=['admin', 'user'])
def delete_reservation(id):
    jwt_token = request.headers.get("Authorization").split(" ")[1]  # Extraer el token JWT
    result = delete_reservation_service(id, jwt_token)
    if result:
        return '', 204
    return jsonify({"error": "No se pudo eliminar la reserva"}), 404
