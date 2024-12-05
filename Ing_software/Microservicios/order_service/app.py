from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Lista de pedidos simulada
orders = []

# Ruta para obtener todos los pedidos
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)


# Ruta para crear un nuevo pedido
@app.route('/order', methods=['POST'])
def create_order():
    order_data = request.get_json()

    # Verificar si el usuario existe (llamando al servicio de usuarios)
    user_id = order_data['user_id']
    user_response = requests.get(f'http://localhost:5000/user/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"message": "User not found"}), 404

    # Verificar si el producto existe (llamando al servicio de productos)
    product_id = order_data['product_id']
    product_response = requests.get(f'http://localhost:5001/product/{product_id}')
    if product_response.status_code != 200:
        return jsonify({"message": "Product not found"}), 404

    # Si todo está bien, agregar el pedido
    orders.append(order_data)
    return jsonify(order_data), 201

if __name__ == '__main__':
    app.run(port=5002)
