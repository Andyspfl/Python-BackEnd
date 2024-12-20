# app/views/reservation_view.py

def render_reservation_list(reservations):
    # Representa una lista de reservas como una lista de diccionarios
    return [
        {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "restaurant_id": reservation.restaurant_id,
            "reservation_date": reservation.reservation_date.strftime('%Y-%m-%dT%H:%M:%S'),
            "num_guests": reservation.num_guests,
            "special_requests": reservation.special_requests,
            "status": reservation.status,
        }
        for reservation in reservations
    ]

def render_reservation_detail(reservation):
    # Representa los detalles de una reserva como un diccionario
    return {
        "id": reservation.id,
        "user_id": reservation.user_id,
        "restaurant_id": reservation.restaurant_id,
        "reservation_date": reservation.reservation_date.strftime('%Y-%m-%dT%H:%M:%S'),
        "num_guests": reservation.num_guests,
        "special_requests": reservation.special_requests,
        "status": reservation.status,
    }