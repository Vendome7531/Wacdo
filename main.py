from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers.product import router as product_router
from app.routers.order import router as order_router
from app.routers.user import router as user_router # Nouveau import

# Création des tables (SQLAlchemy va créer la table 'users' automatiquement)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wacdo API")

app.include_router(product_router)
app.include_router(order_router)
app.include_router(user_router) # Nouvelle route activée

@app.get("/")
def root():
    return {"message": "Wacdo est prêt avec les utilisateurs !"}