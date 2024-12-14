import json
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verifica que el JWT esté presente y sea válido en la solicitud
            verify_jwt_in_request()
            return fn(*args, **kwargs)  # Si el token es válido, ejecuta la función
        except Exception as e:
            # Si hay un error (por ejemplo, si el token es inválido o no está presente)
            return jsonify({"error": str(e)}), 401
    return wrapper

def roles_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                user_role = current_user.get("role")
                if user_role not in roles:
                    return jsonify({"error": "No tiene permiso para realizar esta acción"}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator
