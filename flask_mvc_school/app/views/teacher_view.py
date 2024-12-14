# app/views/teacher_view.py

def render_teacher_list(teachers):
    # Representa una lista de profesores como una lista de diccionarios
    return [
        render_teacher_detail(teacher)
        for teacher in teachers
    ]

def render_teacher_detail(teacher):
    # Representa los detalles de un profesor como un diccionario
    return{
        "id": teacher.id,
        "user_id": teacher.user_id,
        "name": teacher.name,
        "last_name": teacher.last_name,
        "speciality": teacher.speciality,
        "hiring_date": teacher.hiring_date.strftime('%Y-%m-%d') if teacher.hiring_date else None,
        "academic_title": teacher.academic_title
    }