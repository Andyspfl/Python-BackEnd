from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de usuarios simulada
users = [
    {"id": 1, "username": "juan", "email": "juan@correo.com"},
    {"id": 2, "username": "maria", "email": "maria@correo.com"}
]

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Ruta para obtener un usuario por ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

# Ruta para crear un nuevo usuario
@app.route('/user', methods=['POST'])
def create_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(port=5000)
