from database import db
from sqlalchemy.orm import Session

class Qualification(db.Model):
    __tablename__ = "qualifications"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    tuition_id = db.Column(db.Integer, db.ForeignKey("tuitions.id"), nullable = False)
    grade = db.Column(db.Numeric(4, 2), nullable = False)
    evaluation_type = db.Column(db.Enum('PARCIAL', 'FINAL', 'PROYECTO', name = 'tipo_evaluacion'), nullable = False)
    evaluation_date = db.Column(db.Date, nullable = False)
    
    tuition = db.relationship("Tuition", backref = db.backref('qualifications', lazy = True))
    
    
    def __init__(self, tuition_id, grade, evaluation_type, evaluation_date):
        self.tuition_id = tuition_id
        self.grade = grade
        self.evaluation_type = evaluation_type
        self.evaluation_date = evaluation_date
        
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
    
    def update(self, tuition_id = None, grade = None, evaluation_type = None, evaluation_date = None):
        if tuition_id is not None:
            self.tuition_id = tuition_id
        if grade is not None:
            self.grade = grade
        if evaluation_type is not None:
            self.evaluation_type = evaluation_type
        if evaluation_date is not None:
            self.evaluation_date = evaluation_date
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
