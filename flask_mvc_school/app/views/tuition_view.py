# app/views/tuition_view.py

def render_tuition_list(tuitions):
    # Representa una lista de matrículas como una lista de diccionarios
    return [
        render_tuition_detail(tuition)
        for tuition in tuitions
    ]

def render_tuition_detail(tuition):
    # Representa los detalles de una matrícula como un diccionario
    return {
        
        "id": tuition.id,
        "student_id": tuition.student_id,
        "course_id": tuition.course_id,
        "enrollment_date": tuition.enrollment_date.strftime('%Y-%m-%dT%H:%M:%S'),
        "status": tuition.status,
    }