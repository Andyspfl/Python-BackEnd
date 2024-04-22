from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
from app.controllers import clothes_controllers  # Importa los controladores aquí
