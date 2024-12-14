# app/views/student_view.py

def render_student_list(students):
    # Representa una lista de estudiantes como una lista de diccionarios
    return [
        render_student_detail(student)
        for student in students
    ]

def render_student_detail(student):
    # Representa los detalles de un estudiante como un diccionario
    return {
        "id": student.id,
        "user_id": student.user_id,
        "birth_date": student.birth,
        "gender": student.gender,
        "address": student.address,
        "enrollment_date": student.enrollment_date
        
        
    }
