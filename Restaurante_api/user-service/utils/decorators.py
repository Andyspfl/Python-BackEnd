import json
from functools import wraps
from model.user_model import User

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt

def jwt_required(fn):
    @wraps(fn)
    
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            print('aqui el error')
            return jsonify({"error": str(e)}), 401

    return wrapper


def roles_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verifica que el token JWT esté presente y válido
                verify_jwt_in_request()

                # Obtén el correo electrónico (identity) del token JWT
                current_user_email = get_jwt_identity()

                # Obtén el 'role' directamente desde el token JWT
                jwt_claims = get_jwt()
                current_user_role = jwt_claims.get("role")

                # Si el 'role' no está en los claims, podemos devolver un error
                if current_user_role is None:
                    return jsonify({"error": "No se encontró el rol en el token"}), 401

                # Verifica si el rol del usuario está permitido
                if current_user_role not in roles:
                    return jsonify({"error": "No tiene permiso para realizar esta acción"}), 403
                
                # Si pasa todas las comprobaciones, ejecuta la función original
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator