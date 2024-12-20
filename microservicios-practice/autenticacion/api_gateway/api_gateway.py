from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt_claims
import requests

app = Flask(__name__)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambiar en producción
jwt = JWTManager(app)

# Dirección de los microservicios
AUTH_SERVICE_URL = "http://localhost:5000"
RESOURCE_SERVICE_URL = "http://localhost:5001"

# Rutas protegidas por JWT
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    # Verificar que el rol es admin usando el JWT
    claims = get_jwt_claims()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "No tienes permiso para acceder a este recurso"}), 403

    # Redirigir la solicitud al microservicio de recursos
    response = requests.get(f"{RESOURCE_SERVICE_URL}/admin", headers={"Authorization": f"Bearer {request.headers['Authorization'].split()[1]}"})
    return jsonify(response.json()), response.status_code

@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    # Verificar que el rol es user usando el JWT
    claims = get_jwt_claims()
    if claims.get('role') != 'user':
        return jsonify({"msg": "No tienes permiso para acceder a este recurso"}), 403

    # Redirigir la solicitud al microservicio de recursos
    response = requests.get(f"{RESOURCE_SERVICE_URL}/user", headers={"Authorization": f"Bearer {request.headers['Authorization'].split()[1]}"})
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5002, debug=True)
