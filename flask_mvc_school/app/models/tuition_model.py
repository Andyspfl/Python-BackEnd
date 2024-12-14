from database import db
from sqlalchemy.orm import Session

class Tuition(db.Model):
    __tablename__ = "tuitions"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable = False)
    enrollment_date = db.Column(db.Date, nullable = False)
    status = db.Column(db.Enum('ACTIVO', 'COMPLETADO', 'ABANDONADO', name = 'status'), nullable = False)
    
    user = db.relationship("Student", backref = db.backref('tuitions', lazy = True))
    
    
    def __init__(self, student_id, course_id, enrollment_date, status):
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.status = status
        
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
    
    def update(self, student_id = None, course_id = None, enrollment_date = None, status = None):
        if student_id is not None:
            self.student_id = student_id
        if course_id is not None:
            self.course_id = course_id
        if enrollment_date is not None:
            self.enrollment_date = enrollment_date
        if status is not None:
            self.status = status
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
