import jwt
from flask import jsonify

SECRET_KEY = "tu_clave_secreta_aqui"

def decode_jwt_token(token: str):
    try:
        # Decodificar el token usando la misma clave secreta
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f" este es el decode{decoded_token}")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise Exception("El token ha expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")
