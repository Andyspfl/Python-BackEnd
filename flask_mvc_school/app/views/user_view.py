# app/views/user_view.py

def render_user_list(users):
    # Representa una lista de usuarios como una lista de diccionarios
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "tipo_usuario": user.tipo_usuario,
            "activo": user.activo,
            "fecha_creacion": user.fecha_creacion.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        for user in users
    ]

def render_user_detail(user):
    # Representa los detalles de un usuario como un diccionario
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario,
        "activo": user.activo,
        "fecha_creacion": user.fecha_creacion.strftime('%Y-%m-%dT%H:%M:%S'),
    }
