from app.database import db
from sqlalchemy.orm import Session

class Tuition(db.Model):
    __tablename__ = "matriculas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_matricula = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    estado = db.Column(db.Enum('ACTIVO', 'COMPLETADO', 'ABANDONADO', name='estado'), default='ACTIVO', nullable=False)

    # Relación con las tablas 'estudiantes' y 'cursos'
    estudiante = db.relationship('Students', backref=db.backref('tuitions', lazy=True))
    curso = db.relationship('Course', backref=db.backref('tuitions', lazy=True))

    def __init__(self, estudiante_id, curso_id, estado='ACTIVO'):
        self.estudiante_id = estudiante_id
        self.curso_id = curso_id
        self.estado = estado

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Tuition.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Tuition, id)

    def update(self, estudiante_id=None, curso_id=None, estado=None):
        if estudiante_id is not None:
            self.estudiante_id = estudiante_id
        if curso_id is not None:
            self.curso_id = curso_id
        if estado is not None:
            self.estado = estado
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
