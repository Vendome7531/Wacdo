from fastapi import FastAPI, Depends
from app.database.database import engine, Base
from app.routers import auth, user, product, menu, order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import os

# 1. Création des tables
Base.metadata.create_all(bind=engine)

# 2. Initialisation de l'application
app = FastAPI(
    title="WacDo API - Système de Gestion de Restaurant",
    description="Système de gestion des commandes, des produits, des menus et du personnel.",
    version="1.1.0"
)

# 3. Gestion des fichiers statiques (POUR LES IMAGES)
if not os.path.exists("static"):
    os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Configuration CORS (Le "Portier" de ton API)
# On définit ici quels domaines ont le droit de contacter ton API
origins = [
    "http://localhost:3000",      # Port classique pour React/Next.js
    "http://localhost:5173",      # Port classique pour Vite/Vue.js
    "http://127.0.0.1:5500",      # Port classique pour Live Server (VS Code)
    "*",                          # Permet d'accepter TOUT pendant la phase de dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Liste des sites autorisés
    allow_credentials=True,       # Autorise l'envoi des cookies et headers d'auth
    allow_methods=["*"],          # Autorise toutes les méthodes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # Autorise tous les headers (Content-Type, Authorization, etc.)
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