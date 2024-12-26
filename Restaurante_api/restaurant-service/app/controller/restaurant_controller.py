from flask import Blueprint, jsonify, request
from app.model.restaurant_model import Restaurant
from app.utils.decorators import roles_required, jwt_required
from app.view.restaurant_view import render_restaurant_detail, render_restaurant_list

# Crear un blueprint para el controlador de restaurantes
restaurant_bp = Blueprint('restaurant_bp', __name__)

# Ruta para obtener la lista de restaurantes
@restaurant_bp.route('/restaurants', methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_restaurants():
    restaurants = Restaurant.get_all()
    return jsonify(render_restaurant_list(restaurants))


# Ruta para obtener un restaurante especifico por su ID
@restaurant_bp.route("/restaurants/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if restaurant:
        return jsonify(render_restaurant_detail(restaurant))
    return jsonify({"error": "Restaurante no encontrado"}), 404

# Ruta para crear un nuevo restaurante
@restaurant_bp.route("/restaurants", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_restaurant():
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    desciption = data.get("description")
    rating = data.get("rating")
    
    if not name or not address or not city or not phone or not desciption or rating is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    restaurant = Restaurant(name=name, address=address, city=city, phone=phone, description=desciption, rating=rating)
    restaurant.save()
    
    return jsonify(render_restaurant_detail(restaurant)), 201

# Ruta para actualizar un restaurante por su ID
@restaurant_bp.route("/restaurants/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    desciption = data.get("description")
    rating = data.get("rating")
    
    # Actualizar los datos del restaurante
    
    restaurant.update(name=name, address=address, city=city, phone=phone, description=desciption, rating=rating)
    return jsonify(render_restaurant_detail(restaurant))

# Ruta para eliminar un restaurante existente por su ID
@restaurant_bp.route("/restaurants/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if not restaurant:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    
    # Eliminar el restaurante de la base de datos
    restaurant.delete()
    
    # Respuesta vacía con código de estado 204
    return "", 204