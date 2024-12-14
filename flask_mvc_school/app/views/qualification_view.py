# app/views/qualification_view.py

def render_qualification_list(qualifications):
    # Representa una lista de calificaciones como una lista de diccionarios
    return [
        {
            "id": qualification.id,
            "tuition_id": qualification.tuition_id,
            "grade": qualification.grade,
            "evaluation_type": qualification.evaluation_type,
            "evaluation_date": qualification.evaluation_date.strftime('%Y-%m-%d')
        }
        for qualification in qualifications
    ]

def render_qualification_detail(qualification):
    # Representa los detalles de una calificación como un diccionario
    return {
        "id": qualification.id,
        "tuition_id": qualification.tuition_id,
        "grade": qualification.grade,
        "evaluation_type": qualification.evaluation_type,
        "evaluation_date": qualification.evaluation_date.strftime('%Y-%m-%d')
    }
