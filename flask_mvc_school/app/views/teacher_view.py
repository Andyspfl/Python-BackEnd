# app/views/teacher_view.py

def render_teacher_list(teachers):
    # Representa una lista de profesores como una lista de diccionarios
    return [
        {
            "id": teacher.id,
            "usuario_id": teacher.usuario_id,
            "nombre": teacher.nombre,
            "apellido": teacher.apellido,
            "especialidad": teacher.especialidad,
            "fecha_contratacion": teacher.fecha_contratacion.strftime('%Y-%m-%d') if teacher.fecha_contratacion else None,
            "titulo_academico": teacher.titulo_academico,
        }
        for teacher in teachers
    ]

def render_teacher_detail(teacher):
    # Representa los detalles de un profesor como un diccionario
    return {
        "id": teacher.id,
        "usuario_id": teacher.usuario_id,
        "nombre": teacher.nombre,
        "apellido": teacher.apellido,
        "especialidad": teacher.especialidad,
        "fecha_contratacion": teacher.fecha_contratacion.strftime('%Y-%m-%d') if teacher.fecha_contratacion else None,
        "titulo_academico": teacher.titulo_academico,
    }
