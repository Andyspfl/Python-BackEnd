# app/views/user_view.py

def render_user_list(users):
    # Representa una lista de usuarios como una lista de diccionarios
    return [
        render_user_detail(user)
        for user in users
    ]

def render_user_detail(user):
    # Representa los detalles de un usuario como un diccionario
    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "role": user.role,
        "email": user.email
    }
