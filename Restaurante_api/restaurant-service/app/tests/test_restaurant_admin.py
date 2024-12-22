def test_get_restaurants(test_client, admin_auth_headers):
    response = test_client.get("/api/restaurants", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json == []

def test_create_restaurant(test_client, admin_auth_headers):
    data = {
        "name": "Gourmet Plaza",
        "address": "123 Main Street",
        "city": "Springfield",
        "phone": "555-1234",
        "description": "A fine dining experience.",
        "rating": 4.5
    }
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    assert response.json["name"] == "Gourmet Plaza"
    assert response.json["address"] == "123 Main Street"
    assert response.json["city"] == "Springfield"
    assert response.json["phone"] == "555-1234"
    assert response.json["description"] == "A fine dining experience."
    assert response.json["rating"] == 4.5

def test_create_restaurant_with_zero_rating(test_client, admin_auth_headers):
    data = {
        "name": "Budget Bites",
        "address": "404 Error Street",
        "city": "Lost City",
        "phone": "555-4040",
        "description": "Affordable meals for everyone.",
        "rating": 0.0
    }
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    assert response.json["name"] == "Budget Bites"
    assert response.json["address"] == "404 Error Street"
    assert response.json["city"] == "Lost City"
    assert response.json["phone"] == "555-4040"
    assert response.json["description"] == "Affordable meals for everyone."
    assert response.json["rating"] == 0.0

def test_get_restaurant(test_client, admin_auth_headers):
    # Primero crea un restaurante
    data = {
        "name": "Burger Palace",
        "address": "456 Elm Street",
        "city": "Shelbyville",
        "phone": "555-5678",
        "description": "The best burgers in town.",
        "rating": 4.2
    }
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    restaurant_id = response.json["id"]

    # Ahora obtén el restaurante
    response = test_client.get(f"/api/restaurants/{restaurant_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json["name"] == "Burger Palace"
    assert response.json["address"] == "456 Elm Street"
    assert response.json["city"] == "Shelbyville"
    assert response.json["phone"] == "555-5678"
    assert response.json["description"] == "The best burgers in town."
    assert response.json["rating"] == 4.2

def test_get_nonexistent_restaurant(test_client, admin_auth_headers):
    response = test_client.get("/api/restaurants/999", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Restaurante no encontrado"

def test_create_restaurant_invalid_data(test_client, admin_auth_headers):
    data = {"name": "Sushi Place"}  # Faltan address, city, phone, description y rating
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 400
    assert response.json["error"] == "Faltan datos requeridos"

def test_update_restaurant(test_client, admin_auth_headers):
    # Primero crea un restaurante
    data = {
        "name": "Pizza Haven",
        "address": "789 Oak Street",
        "city": "Evergreen",
        "phone": "555-6789",
        "description": "Delicious pizza for everyone.",
        "rating": 4.0
    }
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    restaurant_id = response.json["id"]

    # Ahora actualiza el restaurante
    update_data = {
        "name": "Pizza Haven",
        "address": "789 Oak Street",
        "city": "Evergreen",
        "phone": "555-6789",
        "description": "The best pizza in town.",
        "rating": 4.5
    }
    response = test_client.put(
        f"/api/restaurants/{restaurant_id}", json=update_data, headers=admin_auth_headers
    )
    assert response.status_code == 200
    assert response.json["name"] == "Pizza Haven"
    assert response.json["address"] == "789 Oak Street"
    assert response.json["city"] == "Evergreen"
    assert response.json["phone"] == "555-6789"
    assert response.json["description"] == "The best pizza in town."
    assert response.json["rating"] == 4.5

def test_update_nonexistent_restaurant(test_client, admin_auth_headers):
    update_data = {
        "name": "Steakhouse",
        "address": "1010 Maple Street",
        "city": "Riverdale",
        "phone": "555-1010",
        "description": "Premium steaks and more.",
        "rating": 4.8
    }
    response = test_client.put(
        "/api/restaurants/999", json=update_data, headers=admin_auth_headers
    )
    assert response.status_code == 404
    assert response.json["error"] == "Restaurante no encontrado"

def test_delete_restaurant(test_client, admin_auth_headers):
    # Primero crea un restaurante
    data = {
        "name": "Taco Town",
        "address": "2020 Birch Street",
        "city": "Hillside",
        "phone": "555-2020",
        "description": "Authentic Mexican tacos.",
        "rating": 4.3
    }
    response = test_client.post("/api/restaurants", json=data, headers=admin_auth_headers)
    assert response.status_code == 201
    restaurant_id = response.json["id"]

    # Ahora elimina el restaurante
    response = test_client.delete(
        f"/api/restaurants/{restaurant_id}", headers=admin_auth_headers
    )
    assert response.status_code == 204

    # Verifica que el restaurante ha sido eliminado
    response = test_client.get(f"/api/restaurants/{restaurant_id}", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Restaurante no encontrado"

def test_delete_nonexistent_restaurant(test_client, admin_auth_headers):
    response = test_client.delete("/api/restaurants/999", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Restaurante no encontrado"