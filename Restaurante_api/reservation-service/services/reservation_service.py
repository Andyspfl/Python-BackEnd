import requests
from model.reservation_model import Reservation
from datetime import datetime

def create_reservation_service(data, jwt_token):
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')
    reservation_date = data.get('reservation_date')
    num_guests = data.get('num_guests')
    special_requests = data.get('special_requests')
    status = data.get('status')

    # Verificar que el usuario y el restaurante existan
    user_response = requests.get(f"http://localhost:5000/api/users/{user_id}", headers={"Authorization": f"Bearer {jwt_token}"})
    restaurant_response = requests.get(f"http://localhost:5001/api/restaurants/{restaurant_id}", headers={"Authorization": f"Bearer {jwt_token}"})

    if user_response.status_code != 200 or restaurant_response.status_code != 200:
        raise ValueError("Usuario o Restaurante no válido")

    print("llegue hasta aqui :D")
    # Crear la reserva
    reservation = Reservation(
        user_id=user_id,
        restaurant_id=restaurant_id,
        reservation_date=datetime.fromisoformat(reservation_date.rstrip("Z")),
        num_guests=num_guests,
        special_requests=special_requests,
        status=status
    )

    print(reservation)
    return reservation

def get_reservation_service(id=None):
    if id:
        return Reservation.get_by_id(id)
    return Reservation.get_all()

def update_reservation_service(id, data, jwt_token):
    reservation = Reservation.get_by_id(id)
    if not reservation:
        raise ValueError("Reserva no encontrada")

    # Validar la existencia de usuario y restaurante
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')

    user_response = requests.get(f"http://localhost:5000/users/{user_id}", headers={"Authorization": f"Bearer {jwt_token}"})
    restaurant_response = requests.get(f"http://localhost:5001/api/restaurants/{restaurant_id}", headers={"Authorization": f"Bearer {jwt_token}"})

    if user_response.status_code != 200 or restaurant_response.status_code != 200:
        raise ValueError("Usuario o Restaurante no válido")

    # Actualizar la reserva
    reservation.user_id = user_id
    reservation.restaurant_id = restaurant_id
    reservation.reservation_date = datetime.fromisoformat(data.get("reservation_date").rstrip("Z"))
    reservation.num_guests = data.get("num_guests")
    reservation.special_requests = data.get("special_requests")
    reservation.status = data.get("status")
    
    return reservation

def delete_reservation_service(id, jwt_token):
    reservation = Reservation.get_by_id(id)
    if reservation:
        reservation.delete()
        return True
    return False
