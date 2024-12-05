from app.database import db
from sqlalchemy.orm import Session

class Student(db.Model):
    __tablename__ = "estudiantes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.Enum('M', 'F', 'OTRO', name='genero'), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email_personal = db.Column(db.String(100), nullable=True)
    fecha_ingreso = db.Column(db.Date, nullable=True)

    # Relación con la tabla 'usuarios'
    usuario = db.relationship('User', backref=db.backref('students', lazy=True))

    def __init__(self, usuario_id, nombre, apellido, fecha_nacimiento=None, genero=None, direccion=None,
                 telefono=None, email_personal=None, fecha_ingreso=None):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.direccion = direccion
        self.telefono = telefono
        self.email_personal = email_personal
        self.fecha_ingreso = fecha_ingreso

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Student.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Student, id)

    def update(self, usuario_id=None, nombre=None, apellido=None, fecha_nacimiento=None, genero=None,
               direccion=None, telefono=None, email_personal=None, fecha_ingreso=None):
        if usuario_id is not None:
            self.usuario_id = usuario_id
        if nombre is not None:
            self.nombre = nombre
        if apellido is not None:
            self.apellido = apellido
        if fecha_nacimiento is not None:
            self.fecha_nacimiento = fecha_nacimiento
        if genero is not None:
            self.genero = genero
        if direccion is not None:
            self.direccion = direccion
        if telefono is not None:
            self.telefono = telefono
        if email_personal is not None:
            self.email_personal = email_personal
        if fecha_ingreso is not None:
            self.fecha_ingreso = fecha_ingreso
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
