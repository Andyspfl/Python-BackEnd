from database import db
from sqlalchemy.orm import Session

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    
    birth_date = db.Column(db.Date, nullable = False)
    gender = db.Column(db.Enum('M', 'F', 'OTRO', name='genero'), nullable=True)
    address = db.Column(db.Text, nullable = False)
    enrollment_date = db.Column(db.Date, nullable = False)
    
    user = db.relationship("User", backref = db.backref('students', lazy = True))
    
    
    def __init__(self, user_id, birth_date, gender, address, enrollment_date):
        
        self.user_id = user_id
        self.birth_date = birth_date
        self.gender = gender
        self.address = address
        self.enrollment_date = enrollment_date
    
    
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
    
    
    def update(self, user_id = None, birth_date = None, gender = None, address = None, enrollment_date = None):
        if user_id is not None:
            self.user_id = user_id
            self.birth_date = birth_date
        if gender is not None:
            self.gender = gender
        if address is not None:
            self.address = address
        if enrollment_date is not None:
            self. enrollment_date = enrollment_date
            
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
            
            
