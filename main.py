from fastapi import FastAPI
from routes.productsRoutes import product_router
from routes.usersRoutes import user
from fastapi.middleware.cors import CORSMiddleware
from config.db import Base, engine
from routes.interactionRoutes import interaction
from routes.training import training_router
from routes.commentsRoutes import comment_router
from seed.seed import Seeder

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consumo Consciente API",
    description="API para monitorear y recomendar productos sustentables",
    version="1.0"
)

# Registrar rutas
app.include_router(product_router)
app.include_router(user)
app.include_router(interaction)
app.include_router(training_router)
app.include_router(comment_router)

@app.on_event ("startup")
def startup_event():
    seed=Seeder()
    seed.run()
