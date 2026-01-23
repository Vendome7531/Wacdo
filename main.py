from fastapi import FastAPI
from app.database.database import engine, Base
# Imports explicites pour éviter tout conflit de dossier
from app.routers.product import router as product_router
from app.routers.order import router as order_router

# Création physique des tables dans la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wacdo API")

# On branche les routes sur l'application
app.include_router(product_router)
app.include_router(order_router)

@app.get("/")
def root():
    return {"status": "success", "message": "Wacdo est prêt"}