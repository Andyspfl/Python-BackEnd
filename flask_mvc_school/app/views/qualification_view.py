# app/views/qualification_view.py

def render_qualification_list(qualifications):
    # Representa una lista de calificaciones como una lista de diccionarios
    return [
        {
            "id": qualification.id,
            "matricula_id": qualification.matricula_id,
            "nota": qualification.nota,
            "tipo_evaluacion": qualification.tipo_evaluacion,
            "fecha_evaluacion": qualification.fecha_evaluacion.strftime('%Y-%m-%d'),
        }
        for qualification in qualifications
    ]

def render_qualification_detail(qualification):
    # Representa los detalles de una calificación como un diccionario
    return {
        "id": qualification.id,
        "matricula_id": qualification.matricula_id,
        "nota": qualification.nota,
        "tipo_evaluacion": qualification.tipo_evaluacion,
        "fecha_evaluacion": qualification.fecha_evaluacion.strftime('%Y-%m-%d'),
    }
