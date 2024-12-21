from flask import Flask
from api import user_api, reservation_api, restaurant_api

app = Flask(__name__)

# Registrar las rutas
app.register_blueprint(user_api.bp)
app.register_blueprint(reservation_api.bp)
app.register_blueprint(restaurant_api.bp)

if __name__ == "__main__":
    app.run(debug=True, port=5005)
