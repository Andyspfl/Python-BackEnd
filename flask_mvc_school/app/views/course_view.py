# app/views/course_view.py

def render_course_list(courses):
    # Representa una lista de cursos como una lista de diccionarios
    return [
        {
            "id": course.id,
            "codigo": course.codigo,
            "nombre": course.nombre,
            "descripcion": course.descripcion,
            "creditos": course.creditos,
            "profesor_id": course.profesor_id,
            "periodo": course.periodo,
            "nivel": course.nivel,
        }
        for course in courses
    ]

def render_course_detail(course):
    # Representa los detalles de un curso como un diccionario
    return {
        "id": course.id,
        "codigo": course.codigo,
        "nombre": course.nombre,
        "descripcion": course.descripcion,
        "creditos": course.creditos,
        "profesor_id": course.profesor_id,
        "periodo": course.periodo,
        "nivel": course.nivel,
    }
