# app/views/course_view.py

def render_course_list(courses):
    # Representa una lista de cursos como una lista de diccionarios
    return [
        {
            "id": course.id,
            "code": course.code,
            "name": course.name,
            "description": course.description,
            "credits": course.credits,
            "teacher_id": course.teacher_id,
            "period": course.period,
            "level": course.level
        }
        for course in courses
    ]

def render_course_detail(course):
    # Representa los detalles de un curso como un diccionario
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "description": course.description,
        "credits": course.credits,
        "teacher_id": course.teacher_id,
        "period": course.period,
        "level": course.level
    }
