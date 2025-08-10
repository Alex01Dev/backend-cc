from sqlalchemy.orm import Session
from services.training import entrenar_recomendaciones

def get_best_recommendation(db: Session, user_id: int):
    recomendaciones = entrenar_recomendaciones(db, user_id)
    if recomendaciones:
        return recomendaciones[0]  # Mejor recomendación
    return None
