
```python
-----product_model.py-----
from app.database import db


# Define la clase `Product` que hereda de `db.Model`
# `Product` representa la tabla `products` en la base de datos
class Product(db.Model):
    __tablename__ = "products"

    # Define las columnas de la tabla `products`
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    # Inicializa la clase `Product`
    def __init__(self, name, description, price, stock):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    # Guarda un producto en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtiene todos los productos de la base de datos
    @staticmethod
    def get_all():
        return Product.query.all()

    # Obtiene un producto por su ID
    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)

    # Actualiza un producto en la base de datos
    def update(self, name=None, description=None, price=None, stock=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if stock is not None:
            self.stock = stock
        db.session.commit()

    # Elimina un producto de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()
----user_model.py----
import json

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, roles=["user"]):
        self.username = username
        self.roles = json.dumps(roles)
        self.password_hash = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    # Esta funcion encuentra un usuario por su nombre de usuario
    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

----product_controller.py----
from flask import Blueprint, jsonify, request
from app.models.product_model import Product
from app.utils.decorators import jwt_required, roles_required
from app.views.product_view import render_product_detail, render_product_list

# Crear un blueprint para el controlador de productos
product_bp = Blueprint("product", __name__)


# Ruta para obtener la lista de productos
@product_bp.route("products", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_products():
    products = Product.get_all()
    return jsonify(render_product_list(products))


# Ruta para obtener un producto específico por su ID
@product_bp.route("products/<int:id>", methods=["GET"])
@jwt_required
def get_product(id):
    product = Product.get_by_id(id)
    if product:
        return jsonify(render_product_detail(product))
    return jsonify({"error": "Producto no encontrado"}), 404


# Ruta para crear un nuevo producto
@product_bp.route("products", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")

    # Validación simple de datos de entrada
    if not name or not description or price is None or stock is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo producto y guardarlo en la base de datos
    product = Product(name=name, description=description, price=price, stock=stock)
    product.save()

    return jsonify(render_product_detail(product)), 201


# Ruta para actualizar un producto existente
@product_bp.route("products/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_product(id):
    data = request.json
    product = Product.get_by_id(id)

    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")

    # Actualizar los datos del producto
    product.update(name=name, description=description, price=price, stock=stock)

    return jsonify(render_product_detail(product))


# Ruta para eliminar un producto existente
@product_bp.route("products/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_product(id):
    product = Product.get_by_id(id)

    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Eliminar el producto de la base de datos
    product.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204


-----user_controller.py-----
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user_model import User

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    roles = data.get("roles")

    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contraseña"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_user = User(username, password, roles)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        # Si las credenciales son válidas, genera un token JWT
        access_token = create_access_token(
            identity={"username": username, "roles": user.roles}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

---product_view.py---

def render_product_list(products):
    # Representa una lista de productos como una lista de diccionarios
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
        }
        for product in products
    ]


def render_product_detail(product):
    # Representa los detalles de un producto como un diccionario
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
    }

---user_view.py---
def render_user_list(users):
    # Representa una lista de dulces como una lista de diccionarios
    return [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password_hash,
            "roles": user.roles,
        }
        for user in users
    ]

def render_user_detail(user):
    # Representa los detalles de un dulce como un diccionario
    return {
            "id": user.id,
            "username": user.username,
            "password": user.password_hash,
            "roles": user.roles,
        }

---decorators.py---
import json
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return wrapper


def roles_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                user_roles = json.loads(current_user.get("roles", []))
                if not set(roles).intersection(user_roles):
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator

---swagger.py---
{
    "openapi": "3.0.1",
    "info": {
        "title": "Tienda Online API",
        "version": "1.0.0"
    },
    "paths": {
        "/api/products": {
            "get": {
                "summary": "Obtiene la lista de todos los productos",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de productos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Product"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Crea un nuevo producto",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Product"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Producto creado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Product"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/products/{id}": {
            "get": {
                "summary": "Obtiene un producto específico por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Detalles del producto",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Product"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Producto no encontrado"
                    }
                }
            },
            "put": {
                "summary": "Actualiza un producto existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Product"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Producto actualizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Product"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Producto no encontrado"
                    }
                }
            },
            "delete": {
                "summary": "Elimina un producto existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Producto eliminado"
                    },
                    "404": {
                        "description": "Producto no encontrado"
                    }
                }
            }
        },
        "/api/register": {
            "post": {
                "summary": "Registra un nuevo usuario",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Usuario creado"
                    },
                    "400": {
                        "description": "Solicitud incorrecta"
                    }
                }
            }
        },
        "/api/login": {
            "post": {
                "summary": "Inicia sesión con un usuario existente",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Login"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Inicio de sesión exitoso",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Token"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Credenciales inválidas"
                    }
                }
            }
        }
    },
    "components": {
        "securitySchemes": {
            "JWTAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        },
        "schemas": {
            "Product": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "readOnly": true
                    },
                    "name": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "price": {
                        "type": "number",
                        "format": "float"
                    },
                    "stock": {
                        "type": "integer"
                    }
                },
                "required": [
                    "name",
                    "description",
                    "price",
                    "stock"
                ]
            },
            "User": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                    "roles": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "admin",
                                "user"
                            ]
                        }
                    }
                },
                "required": [
                    "username",
                    "password",
                    "roles"
                ]
            },
            "Login": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    }
                },
                "required": [
                    "username",
                    "password"
                ]
            }
        }
    }
}
---run.py---
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from app.controllers.product_controller import product_bp
from app.controllers.user_controller import user_bp
from app.database import db

app = Flask(__name__)

# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
# Configuración de la URL de la documentación OpenAPI
# Ruta para servir Swagger UI
SWAGGER_URL = "/api/docs"
# Ruta de tu archivo OpenAPI/Swagger
API_URL = "/static/swagger.json"


# Inicializa el Blueprint de Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Tienda Online  API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la base de datos
