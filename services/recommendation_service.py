# controller/notification_controller.py
from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from services.recoserv import get_best_recommendation
from config.db import get_db  # Asumiendo tienes función para obtener sesión DB
import asyncio
import json

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
