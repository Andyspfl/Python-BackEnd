import pytest
import requests_mock
from app.main import create_app  # Asegúrate de que esta es la ruta correcta

# URL base para el servicio de reservas
RESERVATION_SERVICE_URL = "http://localhost:5002/api"

# Fixture para simular el microservicio de reservas
@pytest.fixture
def mock_reservation_service():
    with requests_mock.Mocker() as m:
        yield m

# Test para obtener todas las reservas
def test_get_reservations(mock_reservation_service):
    # Simulamos la respuesta del microservicio
    mock_reservation_service.get(f"{RESERVATION_SERVICE_URL}/reservations", json=[
        {"id": 1, "customer_name": "John Doe", "restaurant_id": 1, "date": "2024-12-24"},
        {"id": 2, "customer_name": "Jane Smith", "restaurant_id": 2, "date": "2024-12-25"}
    ], status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud GET al API Gateway
    token = "fake-jwt-token"
    response = client.get('/reservations', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["customer_name"] == "John Doe"

# Test para obtener una reserva por su ID
def test_get_reservation(mock_reservation_service):
    # Simulamos la respuesta del microservicio
    mock_reservation_service.get(f"{RESERVATION_SERVICE_URL}/reservations/1", json={
        "id": 1, "customer_name": "John Doe", "restaurant_id": 1, "date": "2024-12-24"
    }, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud GET al API Gateway
    token = "fake-jwt-token"
    response = client.get('/reservations/1', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert response.json["customer_name"] == "John Doe"

# Test para crear una nueva reserva
def test_create_reservation(mock_reservation_service):
    # Datos de la nueva reserva
    new_reservation = {"customer_name": "Mark Johnson", "restaurant_id": 1, "date": "2024-12-31"}

    # Simulamos la respuesta del microservicio
    mock_reservation_service.post(f"{RESERVATION_SERVICE_URL}/reservations", json={
        "id": 3, "customer_name": "Mark Johnson", "restaurant_id": 1, "date": "2024-12-31"
    }, status_code=201)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud POST al API Gateway
    token = "fake-jwt-token"
    response = client.post('/reservations', json=new_reservation, headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 201
    assert response.json["customer_name"] == "Mark Johnson"

# Test para actualizar una reserva existente
def test_update_reservation(mock_reservation_service):
    # Datos de la reserva actualizada
    updated_reservation = {"customer_name": "Mark Johnson", "restaurant_id": 1, "date": "2024-12-30"}

    # Simulamos la respuesta del microservicio
    mock_reservation_service.put(f"{RESERVATION_SERVICE_URL}/reservations/1", json={
        "id": 1, "customer_name": "Mark Johnson", "restaurant_id": 1, "date": "2024-12-30"
    }, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud PUT al API Gateway
    token = "fake-jwt-token"
    response = client.put('/reservations/1', json=updated_reservation, headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert response.json["customer_name"] == "Mark Johnson"

# Test para eliminar una reserva
def test_delete_reservation(mock_reservation_service):
    # Simulamos la respuesta del microservicio
    mock_reservation_service.delete(f"{RESERVATION_SERVICE_URL}/reservations/1", json={}, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud DELETE al API Gateway
    token = "fake-jwt-token"
    response = client.delete('/reservations/1', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta
    assert response.status_code == 200
    assert response.json["message"] == "Reserva eliminada"
