from fastapi import FastAPI
from routes.productsRoutes import product_router
from routes.usersRoutes import user
from fastapi.middleware.cors import CORSMiddleware
from config.db import Base, engine
from routes.interactionRoutes import interaction
from routes.training import training_router
from routes.commentsRoutes import comment_router
from seed.seed import Seeder
from seed.reset_db import DatabaseResetter

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

@app.on_event("startup")
def startup_event():
    run_reset = False   # Cambia a True para limpiar la base de datos
    run_seeder = True   # Cambia a True para ejecutar el seeder

    if run_reset:
        print(" Reiniciando base de datos...")
        resetter = DatabaseResetter()
        resetter.reset()

    if run_seeder:
        print(" Ejecutando seeder...")
        seeder = Seeder()
        seeder.run()

    
    
