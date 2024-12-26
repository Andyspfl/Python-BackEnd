from flask import request, jsonify
from app.utils.token_utils import decode_jwt_token

def get_token(request):
    auth_header = request.headers.get('Authorization')
    
    # Imprimir el encabezado para ver qué está llegando
    
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token no proporcionado o formato incorrecto. Debe ser 'Bearer <JWT>'"}), 401
    
    token = auth_header.split(" ")[1]
    
    try:
        
        return token # Regresar el payload decodificado del token
    except Exception as e:
        return jsonify({"error": "Token inválido o expirado", "message": str(e)}), 401
