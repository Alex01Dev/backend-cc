from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from services.training import entrenar_recomendaciones
from config.db import get_db
import asyncio
import json

def get_best_recommendation(db: Session, user_id: int):
    recomendaciones = entrenar_recomendaciones(db, user_id)
    if recomendaciones:
        return recomendaciones[0]  # Mejor recomendación
    return None


async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            # Obtener la mejor recomendación (la primera)
            recomendacion = get_best_recommendation(db, user_id)
            if recomendacion:
                mensaje = {
                    "type": "recommendation",
                    "data": recomendacion
                }
                await websocket.send_text(json.dumps(mensaje))
            else:
                await websocket.send_text(json.dumps({"type": "info", "data": "No recommendations available"}))

            await asyncio.sleep(10)  # Esperar 10 segundos antes de la siguiente notificación
    except WebSocketDisconnect:
        print(f"Cliente desconectado: user_id={user_id}")
