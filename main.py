from fastapi import FastAPI
from routes.productsRoutes import product_router
from config.db import Base, engine

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consumo Consciente API",
    description="API para monitorear y recomendar productos sustentables",
    version="1.0"
)

# Registrar rutas
app.include_router(product_router)
