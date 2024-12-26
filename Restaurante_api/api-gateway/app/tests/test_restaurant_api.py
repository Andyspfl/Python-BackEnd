import pytest
import requests_mock
from app.main import create_app  # Asegúrate de que esta es la ruta correcta

# URL base para el servicio de restaurantes
RESTAURANT_SERVICE_URL = "http://localhost:5001/api"

# Fixture para simular el microservicio de restaurantes
@pytest.fixture
def mock_restaurant_service():
    with requests_mock.Mocker() as m:
        yield m

# Test para obtener todos los restaurantes
def test_get_restaurants(mock_restaurant_service):
    # Simulamos la respuesta del microservicio
    mock_restaurant_service.get(f"{RESTAURANT_SERVICE_URL}/restaurants", json=[
        {"id": 1, "name": "Restaurant 1"},
        {"id": 2, "name": "Restaurant 2"}
    ], status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud GET al API Gateway
    token = "fake-jwt-token"
    response = client.get('/restaurants', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Restaurant 1"

# Test para obtener un restaurante por su ID
def test_get_restaurant(mock_restaurant_service):
    # Simulamos la respuesta del microservicio
    mock_restaurant_service.get(f"{RESTAURANT_SERVICE_URL}/restaurants/1", json={
        "id": 1, "name": "Restaurant 1"
    }, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud GET al API Gateway
    token = "fake-jwt-token"
    response = client.get('/restaurants/1', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert response.json["name"] == "Restaurant 1"

# Test para crear un restaurante
def test_create_restaurant(mock_restaurant_service):
    # Datos del nuevo restaurante
    new_restaurant = {"name": "New Restaurant", "location": "Location 1"}

    # Simulamos la respuesta del microservicio
    mock_restaurant_service.post(f"{RESTAURANT_SERVICE_URL}/restaurants", json={
        "id": 3, "name": "New Restaurant", "location": "Location 1"
    }, status_code=201)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud POST al API Gateway
    token = "fake-jwt-token"
    response = client.post('/restaurants', json=new_restaurant, headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 201
    assert response.json["name"] == "New Restaurant"

# Test para actualizar un restaurante
def test_update_restaurant(mock_restaurant_service):
    # Datos del restaurante actualizado
    updated_restaurant = {"name": "Updated Restaurant", "location": "Updated Location"}

    # Simulamos la respuesta del microservicio
    mock_restaurant_service.put(f"{RESTAURANT_SERVICE_URL}/restaurants/1", json={
        "id": 1, "name": "Updated Restaurant", "location": "Updated Location"
    }, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud PUT al API Gateway
    token = "fake-jwt-token"
    response = client.put('/restaurants/1', json=updated_restaurant, headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta y los datos
    assert response.status_code == 200
    assert response.json["name"] == "Updated Restaurant"

# Test para eliminar un restaurante
def test_delete_restaurant(mock_restaurant_service):
    # Simulamos la respuesta del microservicio
    mock_restaurant_service.delete(f"{RESTAURANT_SERVICE_URL}/restaurants/1", json={}, status_code=200)

    # Creamos la aplicación Flask
    app = create_app()
    client = app.test_client()

    # Hacemos la solicitud DELETE al API Gateway
    token = "fake-jwt-token"
    response = client.delete('/restaurants/1', headers={"Authorization": f"Bearer {token}"})
    
    # Comprobamos el estado de la respuesta
    assert response.status_code == 200
    assert response.json["message"] == "Restaurante eliminado"
