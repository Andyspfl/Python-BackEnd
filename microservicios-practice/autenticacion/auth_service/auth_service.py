from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambiar en producción
jwt = JWTManager(app)

# Base de datos ficticia de usuarios
users = {
    "admin": {"password": generate_password_hash("admin123"), "role": "admin"},
    "user": {"password": generate_password_hash("user123"), "role": "user"}
}

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del cuerpo
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Verificar que el usuario existe
    if username not in users:
        return jsonify({"msg": "Usuario no encontrado"}), 401
    
    # Verificar la contraseña
    user = users[username]
    if not check_password_hash(user['password'], password):
        return jsonify({"msg": "Contraseña incorrecta"}), 401
    
    # Crear el token JWT con el rol del usuario
    access_token = create_access_token(identity=username, additional_claims={"role": user['role']})
    
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
