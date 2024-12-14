from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from controllers.user_controller import user_bp
from controllers.course_controller import course_bp
from controllers.teacher_controller import teacher_bp
from controllers.student_controller import student_bp
from controllers.tuition_controller import tuition_bp
from controllers.qualification_controller import qualification_bp

from database import db
from flask_cors import CORS  # Importa CORS


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
SWAGGER_URL = "/api/docs"

API_URL = "/static/swagger.json"

# Inicializa el Blueprint de Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "API to manage a school"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///platform.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la base de datos
db.init_app(app)

# Inicializa la extension JWTManager
jwt = JWTManager(app)

# Registra los blueprints de los controladores
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(course_bp, url_prefix="/api")
app.register_blueprint(teacher_bp, url_prefix="/api")
app.register_blueprint(student_bp, url_prefix="/api")
app.register_blueprint(tuition_bp, url_prefix="/api")
app.register_blueprint(qualification_bp, url_prefix="/api")


# Aplica CORS a toda la aplicacion
CORS(app)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()
    
# Ejecuta la aplicacion
if __name__ == "__main__":
    app.run(port = 5000, debug=True)