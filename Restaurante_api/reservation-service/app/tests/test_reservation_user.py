import pytest
from unittest.mock import patch, Mock
from flask import jsonify

# Test para crear una reserva
def test_create_reservation_user(test_client, user_auth_header):
    create_data = {
        "user_id": 1,
        "restaurant_id": 1,
        "reservation_date": "2024-12-25T20:00:00",
        "num_guests": 4,
        "special_requests": "Sin cebolla",
        "status": "pending"
    }

    user_response_mock = {
        "id": 1,
        "email": "andy@gmail.com",
        "role": "user"
    }

    restaurant_response_mock = {
        "id": 1,
        "name": "Restaurant A",
        "location": "City Center"
    }

    with patch('requests.get') as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: user_response_mock),
            Mock(status_code=200, json=lambda: restaurant_response_mock)
        ]

        # Realizamos la petición para crear la reserva
        response = test_client.post('/api/reservations', json=create_data, headers=user_auth_header)

    # Verificamos que la respuesta sea la esperada
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['status'] == 'pending'


# Test para obtener una reserva específica
def test_get_reservation_user(test_client, user_auth_header):
    reservation_id = 1  # Suponemos que la reserva con ID 1 existe

    # Realizamos la petición para obtener la reserva
    response = test_client.get(f'/api/reservations/{reservation_id}', headers=user_auth_header)

    # Verificamos que la respuesta sea la esperada
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == reservation_id


# Test para actualizar una reserva
def test_update_reservation_user(test_client, user_auth_header):
    reservation_id = 1  # Suponemos que la reserva con ID 1 existe

    update_data = {
        "user_id": 1,
        "restaurant_id": 1,
        "reservation_date": "2024-12-26T20:00:00",
        "num_guests": 5,
        "special_requests": "Con cebolla",
        "status": "confirmed"
    }

    user_response_mock = {
        "id": 1,
        "email": "andy@gmail.com",
        "role": "user"
    }

    restaurant_response_mock = {
        "id": 1,
        "name": "Restaurant A",
        "location": "City Center"
    }

    with patch('requests.get') as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: user_response_mock),
            Mock(status_code=200, json=lambda: restaurant_response_mock)
        ]

        # Realizamos la petición para actualizar la reserva
        response = test_client.put(f'/api/reservations/{reservation_id}', json=update_data, headers=user_auth_header)

    # Verificamos que la respuesta sea la esperada
    assert response.status_code == 200
    assert response.json['status'] == 'confirmed'
    assert response.json['reservation_date'] == update_data['reservation_date']


# Test para eliminar una reserva
def test_delete_reservation_user(test_client, user_auth_header):
    reservation_id = 1  # Suponemos que la reserva con ID 1 existe

    # Realizamos la petición para eliminar la reserva
    response = test_client.delete(f'/api/reservations/{reservation_id}', headers=user_auth_header)

    # Verificamos que la respuesta sea la esperada
    assert response.status_code == 204  # 204 No Content (Eliminación exitosa)
