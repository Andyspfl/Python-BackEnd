import pytest
import requests_mock
from app.main import create_app # Asumiendo que tu aplicación tiene una función de creación

# Simulación de respuestas del microservicio de usuarios
@pytest.fixture
def mock_user_service():
    with requests_mock.Mocker() as m:
        yield m

# Test de la ruta de registro en el API Gateway
def test_register_user_api(mock_user_service):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "password123",
        "phone": "123456789",
        "role": "user"
    }

    mock_user_service.post('http://localhost:5000/api/register', json={
        "message": "Usuario creado exitosamente", "id": 1
    }, status_code=201)

    app = create_app()
    client = app.test_client()

    response = client.post('/register', json=user_data)
    assert response.status_code == 201
    assert response.json["message"] == "Usuario creado exitosamente"

# Test de la ruta de login en el API Gateway
def test_login_user_api(mock_user_service):
    credentials = {
        "email": "johndoe@example.com",
        "password": "password123"
    }

    mock_user_service.post('http://localhost:5000/api/login', json={
        "access_token": "fake-jwt-token"
    }, status_code=200)

    app = create_app()
    client = app.test_client()

    response = client.post('/login', json=credentials)
    assert response.status_code == 200
    assert "access_token" in response.json

# Test de la ruta /me (perfil de usuario) en el API Gateway
def test_get_user_profile_api(mock_user_service):
    mock_user_service.get('http://localhost:5000/api/me', json={
        "email": "johndoe@example.com", "role": "user"
    }, status_code=200)

    app = create_app()
    client = app.test_client()

    token = "fake-jwt-token"
    response = client.get('/me', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json["email"] == "johndoe@example.com"

# Test de la ruta /users en el API Gateway (solo para admin)
def test_get_all_users_api(mock_user_service):
    mock_user_service.get('http://localhost:5000/api/users', json=[
        {"name": "John", "email": "john@example.com", "role": "user"},
        {"name": "Admin", "email": "admin@example.com", "role": "admin"}
    ], status_code=200)

    app = create_app()
    client = app.test_client()

    token = "admin-jwt-token"
    response = client.get('/users', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json) > 0

# Test de la ruta /users/<id> en el API Gateway
def test_get_user_by_id_api(mock_user_service):
    mock_user_service.get('http://localhost:5000/api/users/1', json={
        "id": 1, "name": "John", "email": "john@example.com", "role": "user"
    }, status_code=200)

    app = create_app()
    client = app.test_client()

    token = "admin-jwt-token"
    response = client.get('/users/1', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json['id'] == 1
