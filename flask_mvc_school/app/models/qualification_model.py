from app.database import db
from sqlalchemy.orm import Session

class Qualification(db.Model):
    __tablename__ = "calificaciones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    nota = db.Column(db.Numeric(4, 2), nullable=True)
    tipo_evaluacion = db.Column(db.Enum('PARCIAL', 'FINAL', 'PROYECTO', name='tipo_evaluacion'), nullable=True)
    fecha_evaluacion = db.Column(db.Date, nullable=True)

    # Relación con la tabla 'matriculas'
    matricula = db.relationship('Tuition', backref=db.backref('qualifications', lazy=True))

    def __init__(self, matricula_id, nota=None, tipo_evaluacion=None, fecha_evaluacion=None):
        self.matricula_id = matricula_id
        self.nota = nota
        self.tipo_evaluacion = tipo_evaluacion
        self.fecha_evaluacion = fecha_evaluacion

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Qualification.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Qualification, id)

    def update(self, matricula_id=None, nota=None, tipo_evaluacion=None, fecha_evaluacion=None):
        if matricula_id is not None:
            self.matricula_id = matricula_id
        if nota is not None:
            self.nota = nota
        if tipo_evaluacion is not None:
            self.tipo_evaluacion = tipo_evaluacion
        if fecha_evaluacion is not None:
            self.fecha_evaluacion = fecha_evaluacion
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
