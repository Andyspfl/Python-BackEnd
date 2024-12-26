def test_user_get_restaurants(test_client, user_auth_headers):
    response = test_client.get("/api/restaurants", headers = user_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
def test_user_get_restaurants(test_client, user_auth_headers, admin_auth_headers):
    admin_data = {
        "name": "Gourmet Plaza",
        "address": "123 Main Street",
        "city": "Springfield",
        "phone": "555-1234",
        "description": "A fine dining experience.",
        "rating": 4.5
    }
    admin_response = test_client.post("/api/restaurants", json = admin_data, headers = admin_auth_headers)
    
    assert admin_response.status_code == 201
    restaurant_id = admin_response.json["id"]
    
    response = test_client.get(f"/api/restaurants/{restaurant_id}", headers = user_auth_headers)
    assert response.status_code == 200
    assert response.json["name"] == "Gourmet Plaza"
    assert response.json["address"] == "123 Main Street"
    assert response.json["city"] == "Springfield"
    assert response.json["phone"] == "555-1234"
    assert response.json["description"] == "A fine dining experience."
    assert response.json["rating"] == 4.5
    
def test_user_get_noexistent_restaurant(test_client, user_auth_headers):
    response = test_client.get("/api/restuarants/999", headers = user_auth_headers)
    
def test_user_create_restaurant(test_client, user_auth_headers):
    data  = {
        "name": "Gourmet Plaza",
        "address": "123 Main Street",
        "city": "Springfield",
        "phone": "555-1234",
        "description": "A fine dining experience.",
        "rating": 4.5
    }
    response = test_client.post("/api/restaurants", json = data, headers = user_auth_headers)
    
    assert response.status_code == 403
    assert response.json["error"] == "No tiene permiso para realizar esta acción"
    
def test_user_update_restaurant(test_client, user_auth_headers, admin_auth_headers):
    update_data = {
        "name": "Gourmet Plaza",
        "address": "123 Main Street",
        "city": "Springfield",
        "phone": "555-1234",
        "description": "A fine dining experience.",
        "rating": 4.5
    }
    response = test_client.post("/api/restaurants", json = update_data, headers = admin_auth_headers)
    assert response.status_code == 201
    
    response_user = test_client.put(f"/api/restaurants/{response.json["id"]}", headers = user_auth_headers)
    
    assert response_user.status_code == 403
    assert response_user.json["error"] == "No tiene permiso para realizar esta acción"
    
        
def test_customer_delete_restaurant(test_client, user_auth_headers):
    response = test_client.delete("/api/restaurants/1", headers = user_auth_headers)
    assert response.status_code == 403
    assert response.json["error"] == "No tiene permiso para realizar esta acción"