from app.database import db
from sqlalchemy.orm import Session

class Teacher(db.Model):
    __tablename__ = "profesores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=True)
    fecha_contratacion = db.Column(db.Date, nullable=True)
    titulo_academico = db.Column(db.String(100), nullable=True)

    # Relación con la tabla 'usuarios'
    usuario = db.relationship('User', backref=db.backref('teachers', lazy=True))

    def __init__(self, usuario_id, nombre, apellido, especialidad=None, fecha_contratacion=None, titulo_academico=None):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.fecha_contratacion = fecha_contratacion
        self.titulo_academico = titulo_academico

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Teacher.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Teacher, id)

    def update(self, usuario_id=None, nombre=None, apellido=None, especialidad=None, fecha_contratacion=None, titulo_academico=None):
        if usuario_id is not None:
            self.usuario_id = usuario_id
        if nombre is not None:
            self.nombre = nombre
        if apellido is not None:
            self.apellido = apellido
        if especialidad is not None:
            self.especialidad = especialidad
        if fecha_contratacion is not None:
            self.fecha_contratacion = fecha_contratacion
        if titulo_academico is not None:
            self.titulo_academico = titulo_academico
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
