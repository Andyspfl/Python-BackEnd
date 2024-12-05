# app/views/tuition_view.py

def render_tuition_list(tuitions):
    # Representa una lista de matrículas como una lista de diccionarios
    return [
        {
            "id": tuition.id,
            "estudiante_id": tuition.estudiante_id,
            "curso_id": tuition.curso_id,
            "fecha_matricula": tuition.fecha_matricula.strftime('%Y-%m-%dT%H:%M:%S'),
            "estado": tuition.estado,
        }
        for tuition in tuitions
    ]

def render_tuition_detail(tuition):
    # Representa los detalles de una matrícula como un diccionario
    return {
        "id": tuition.id,
        "estudiante_id": tuition.estudiante_id,
        "curso_id": tuition.curso_id,
        "fecha_matricula": tuition.fecha_matricula.strftime('%Y-%m-%dT%H:%M:%S'),
        "estado": tuition.estado,
    }
