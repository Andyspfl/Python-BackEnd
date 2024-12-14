from database import db
from sqlalchemy.orm import Session


class Course(db.Model):
    __tablename__ = "courses"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    code = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    desciption = db.Column(db.Text, nullable = False)
    credits = db.Column(db.Integer, nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable = False)
    period = db.Column(db.String(50), nullable = False)
    level = db.Column(db.Enum('INICIAL', 'INTERMEDIO', 'AVANZADO', name = 'nivel'), nullable = False)
    
    teacher = db.relationship("Teacher", backref = db.backref("courses", lazy = True))
    
    def __init__(self, code = None, name = None, description = None, credits = None, teacher_id = None, period = None, level = None):
        self.code = code
        self.name = name
        self. description = description
        self.credits = credits
        self.teacher_id = teacher_id
        self. period = period
        self.level = level
        
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
    
    def update(self, code = None, name = None, description = None, credits = None, teacher_id = None, period = None, level = None):
        if code is not None:
            self.code = code
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if credits is not None:
            self.credits = credits
        if teacher_id is not None:
            self.teacher_id = teacher_id
        if period is not None:
            self.period = period
        if level is not None:
            self.level = level
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()