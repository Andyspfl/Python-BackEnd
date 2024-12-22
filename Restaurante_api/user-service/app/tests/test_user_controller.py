import pytest

@pytest.fixture
def new_user():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "role": "user",
    }


def test_register_user(test_client, new_user):
    response = test_client.post("/api/register", json=new_user)
    assert response.status_code == 201
    assert response.json["message"] == "Usuario creado exitosamente"


def test_register_duplicate_user(test_client, new_user):

    # Intentar registrar el mismo usuario de nuevo
    response = test_client.post("/api/register", json=new_user)
    assert response.status_code == 400
    assert response.json["error"] == "El correo electrónico ya está en uso"


def test_login_user(test_client, new_user):
    # Ahora intentar iniciar sesión
    login_credentials = {
        "email": new_user["email"],
        "password": new_user["password"],
    }
    response = test_client.post("/api/login", json=login_credentials)
    assert response.status_code == 200
    assert response.json["access_token"]


def test_login_invalid_user(test_client, new_user):
    # Intentar iniciar sesión sin registrar al usuario
    login_credentials = {
        "email": "nouser@example.com",
        "password": new_user["password"],
    }
    response = test_client.post("/api/login", json=login_credentials)
    assert response.status_code == 401
    assert response.json["error"] == "Credenciales inválidas"


def test_login_wrong_password(test_client, new_user):
    # Intentar iniciar sesión con una contraseña incorrecta
    login_credentials = {"email": new_user["email"], "password": "wrongpassword"}
    response = test_client.post("/api/login", json=login_credentials)
    assert response.status_code == 401
    assert response.json["error"] == "Credenciales inválidas"

def test_register_admin_user(test_client):
    new_admin = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpassword",
        "phone": "9876543210",
        "role": "admin",
    }
    response = test_client.post("/api/register", json=new_admin)
    assert response.status_code == 201
    assert response.json["message"] == "Usuario creado exitosamente"


def test_admin_login_user(test_client):
    # Ahora intentar iniciar sesión como administrador
    admin_credentials = {
        "email": "admin@example.com",
        "password": "adminpassword",
    }
    response = test_client.post("/api/login", json=admin_credentials)
    assert response.status_code == 200
    assert response.json["access_token"]
    
def test_admin_get_users(test_client, admin_auth_header):
    response = test_client.get("/api/users", headers=admin_auth_header)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    

def test_admin_get_user(test_client, admin_auth_header):
    data = {
        "name": "Test User",
        "email": "test2@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "role": "admin",
    }
    response = test_client.post("/api/register",json=data, headers=admin_auth_header)
    assert response.status_code == 201
    user_id = response.json["id"]
    
    response = test_client.get(f"/api/users/{user_id}", headers = admin_auth_header)   
    assert response.status_code == 200
    assert response.json["id"] == user_id
    assert response.json["name"] == data["name"]
    assert response.json["email"] == data["email"]
    assert response.json["role"] == data["role"]
    assert response.json["phone"] == data["phone"]
    