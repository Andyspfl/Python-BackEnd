import json 

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    def __init__(self, name, email, password, phone, role):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.phone = phone
        self.role = role
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return db.session.get(User, user_id)  # Método para obtener un usuario por ID
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
