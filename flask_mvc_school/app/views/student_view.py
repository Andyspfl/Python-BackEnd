# app/views/student_view.py

def render_student_list(students):
    # Representa una lista de estudiantes como una lista de diccionarios
    return [
        {
            "id": student.id,
            "usuario_id": student.usuario_id,
            "nombre": student.nombre,
            "apellido": student.apellido,
            "fecha_nacimiento": student.fecha_nacimiento.strftime('%Y-%m-%d') if student.fecha_nacimiento else None,
            "genero": student.genero,
            "direccion": student.direccion,
            "telefono": student.telefono,
            "email_personal": student.email_personal,
            "fecha_ingreso": student.fecha_ingreso.strftime('%Y-%m-%d') if student.fecha_ingreso else None,
        }
        for student in students
    ]

def render_student_detail(student):
    # Representa los detalles de un estudiante como un diccionario
    return {
        "id": student.id,
        "usuario_id": student.usuario_id,
        "nombre": student.nombre,
        "apellido": student.apellido,
        "fecha_nacimiento": student.fecha_nacimiento.strftime('%Y-%m-%d') if student.fecha_nacimiento else None,
        "genero": student.genero,
        "direccion": student.direccion,
        "telefono": student.telefono,
        "email_personal": student.email_personal,
        "fecha_ingreso": student.fecha_ingreso.strftime('%Y-%m-%d') if student.fecha_ingreso else None,
    }
