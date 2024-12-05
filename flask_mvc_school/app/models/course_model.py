from app.database import db
from sqlalchemy.orm import Session

class Course(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    creditos = db.Column(db.Integer, nullable=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'), nullable=True)
    periodo = db.Column(db.String(50), nullable=True)
    nivel = db.Column(db.Enum('INICIAL', 'INTERMEDIO', 'AVANZADO', name='nivel'), nullable=True)

    # Relación con la tabla 'profesores'
    profesor = db.relationship('Teacher', backref=db.backref('courses', lazy=True))

    def __init__(self, codigo, nombre, descripcion=None, creditos=None, profesor_id=None, periodo=None, nivel=None):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.creditos = creditos
        self.profesor_id = profesor_id
        self.periodo = periodo
        self.nivel = nivel

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Course.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Course, id)

    def update(self, codigo=None, nombre=None, descripcion=None, creditos=None, profesor_id=None, periodo=None, nivel=None):
        if codigo is not None:
            self.codigo = codigo
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion
        if creditos is not None:
            self.creditos = creditos
        if profesor_id is not None:
            self.profesor_id = profesor_id
        if periodo is not None:
            self.periodo = periodo
        if nivel is not None:
            self.nivel = nivel
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
