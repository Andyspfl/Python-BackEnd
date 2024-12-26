import requests
from app.model.reservation_model import Reservation
from datetime import datetime


def create_reservation_service(data):
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    reservation = Reservation(
        user_id=user_id,
        restaurant_id=restaurant_id,
        reservation_date=datetime.fromisoformat(reservation_date.rstrip("Z")),
        num_guests=num_guests,
        special_requests=special_requests,
        status=status,
    )
    
    reservation.save()
    
    return reservation


def get_reservation_service(id=None):
    if id:
        return Reservation.get_by_id(id)
    return Reservation.get_all()


def update_reservation_service(id, data):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        raise ValueError("Reserva no encontrada")

    # Actualizar la reserva
    reservation.user_id = data.get("user_id")
    reservation.restaurant_id = data.get("restaurant_id")
    reservation.reservation_date = datetime.fromisoformat(
        data.get("reservation_date").rstrip("Z")
    )
    reservation.num_guests = data.get("num_guests")
    reservation.special_requests = data.get("special_requests")
    reservation.status = data.get("status")

    reservation.save()
    
    return reservation


def delete_reservation_service(id, jwt_token):
    reservation = Reservation.get_by_id(id)
    if reservation:
        reservation.delete()
        return True
    return False
