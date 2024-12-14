import json

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from database import db

class User(UserMixin, db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    password_hash = db.Column(db.String(129), nullable = False)
    phone = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    
    
    
    def __init__(self, name = None, password = None, phone = None, role = None, email = None):
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.phone = phone
        self.role = role
        self.email = email
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email = email).first()
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)