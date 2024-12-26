from app.database import db
from sqlalchemy.orm import Session

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)  # Ya no es una clave foránea
    restaurant_id = db.Column(db.Integer, nullable=False)  # Tampoco es clave foránea
    reservation_date = db.Column(db.DateTime, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pendiente")

    def __init__(self, user_id, restaurant_id, reservation_date, num_guests, special_requests=None, status="pendiente"):
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.reservation_date = reservation_date
        self.num_guests = num_guests
        self.special_requests = special_requests
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Reservation.query.all()

    @staticmethod
    def get_by_id(id):
        session: Session = db.session
        return session.get(Reservation, id)

    def update(self, user_id=None, restaurant_id=None, reservation_date=None, num_guests=None, special_requests=None, status=None):
        if user_id is not None:
            self.user_id = user_id
        if restaurant_id is not None:
            self.restaurant_id = restaurant_id
        if reservation_date is not None:
            self.reservation_date = reservation_date
        if num_guests is not None:
            self.num_guests = num_guests
        if special_requests is not None:
            self.special_requests = special_requests
        if status is not None:
            self.status = status
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
