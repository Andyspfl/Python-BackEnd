from flask import Flask
from api import user_api, reservation_api, restaurant_api

def create_app():
    app = Flask(__name__)

    # Registrar las rutas (Blueprints)
    app.register_blueprint(user_api.bp, url_prefix="/api")
    app.register_blueprint(reservation_api.bp, url_prefix="/api")
    app.register_blueprint(restaurant_api.bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()  # Asegúrate de crear la app desde esta función
    app.run(debug=True,host='0.0.0.0', port=5005)

