from app.database import db
from sqlalchemy.orm import Session

class User(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.Enum('admin', 'profesor', 'estudiante', name='tipo_usuario'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __init__(self, username, email, password, tipo_usuario, activo=True, fecha_creacion=None):
        self.username = username
        self.email = email
        self.password = password
        self.tipo_usuario = tipo_usuario
        self.activo = activo
        self.fecha_creacion = fecha_creacion or db.func.current_timestamp()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(User, id)

    def update(self, username=None, email=None, password=None, tipo_usuario=None, activo=None):
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if tipo_usuario is not None:
            self.tipo_usuario = tipo_usuario
        if activo is not None:
            self.activo = activo
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
