from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de productos simulada
products = [
    {"id": 1, "name": "Laptop", "price": 800},
    {"id": 2, "name": "Smartphone", "price": 500}
]

# Ruta para obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Ruta para obtener un producto por ID
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

# Ruta para crear un nuevo producto
@app.route('/product', methods=['POST'])
def create_product():
    new_product = request.get_json()
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(port=5001)
