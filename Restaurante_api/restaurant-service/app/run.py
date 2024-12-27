from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


from controller.restaurant_controller import restaurant_bp
from database import db


app = Flask(__name__)

# Configuracion de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
# Configuracion de la URL de la documentacion OpenAPI


# Ruta para servir OPENAPI/Swagger
SWAGGER_URL = "/api/docs"


# Ruta de tu archivo OpenAPI/Swagger
API_URL = "/static/swagger.json"

# Inicializa el Blueprint de Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Restaurant Service"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la base de datos
db.init_app(app)

# Inicializa la extensión JWTManager
jwt = JWTManager(app)

# Registra los blueprints de animales y usuarios en la aplicación
app.register_blueprint(restaurant_bp, url_prefix="/api")



# Crea las tablas si no existen
with app.app_context():
    db.create_all()

# Ejecuta la aplicación
if __name__ == "__main__":
    app.run(port=5001,host='0.0.0.0', debug=True)
