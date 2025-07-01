from fastapi import APIRouter, HTTPException
from services.recommender import generar_recomendaciones

recomendacion = APIRouter()

@recomendacion.get("/recomendaciones/{user_id}", tags=["Recomendaciones"])
def obtener_recomendaciones(user_id: int):
    recomendaciones = generar_recomendaciones(user_id)
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No hay recomendaciones para este usuario.")
    
    return {"user_id": user_id, "recomendaciones": recomendaciones}
