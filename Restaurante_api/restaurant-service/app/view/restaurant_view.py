def render_restaurant_list(restaurants):
    return [
        {
            "name": restaurant.name,
            "address": restaurant.address,
            "city": restaurant.city,
            "phone": restaurant.phone,
            "description": restaurant.description,
            "rating": float(restaurant.rating),
        }
        for restaurant in restaurants
    ]

def render_restaurant_detail(restaurant):
    return {
        "name": restaurant.name,
        "address": restaurant.address,
        "city": restaurant.city,
        "phone": restaurant.phone,
        "description": restaurant.description,
        "rating": float(restaurant.rating),
    }