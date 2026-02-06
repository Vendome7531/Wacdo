from fastapi import FastAPI, Depends
from app.database.database import engine, Base
from app.routers import auth, user, product, menu, order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import os

# 1. Création des tables
Base.metadata.create_all(bind=engine)

# 2. Initialisation de l'application (UNE SEULE FOIS)
app = FastAPI(
    title="WacDo API - Système de Gestion de Restaurant",
    description="""
    Système de gestion des commandes, des produits, des menus et du personnel.
    """,
    version="1.1.0"
)

# 3. Gestion des fichiers statiques (POUR LES IMAGES)
# On vérifie que le dossier existe pour éviter le plantage au démarrage
if not os.path.exists("static"):
    os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Schéma de sécurité pour Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 6. Inclusion des routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(menu.router)
app.include_router(order.router)

@app.get("/")
def read_root():
    return {"message": "Serveur opérationnel - Bienvenue chez Wacdo !"}

@app.get("/auth-check", tags=["Security"])
def check_connection(token: str = Depends(oauth2_scheme)):
    return {"status": "Connecté", "token": token}