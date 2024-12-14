from database import db
from sqlalchemy.orm import Session

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    speciality = db.Column(db.String(100), nullable = False)
    hiring_date = db.Column(db.Date, nullable = False)
    academic_title = db.Column(db.String(100), nullable = False)
    
    user = db.relationship("User", backref = db.backref('teachers', lazy=True))
    
    def __init__(self, user_id, speciality, hiring_date, academic_title):
        
        self.user_id = user_id
        self.speciality = speciality
        self.hiring_date = hiring_date
        self.academic_title = academic_title
        
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
    
    def update(self, user_id = None, speciality = None, hiring_date = None, academic_title = None):
        if user_id is not None:
            self.user_id = user_id
        if speciality is not None:
            self.speciality = speciality
        if hiring_date is not None:
            self.hiring_date = hiring_date
        if academic_title is not None:
            self.academic_title = academic_title
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

