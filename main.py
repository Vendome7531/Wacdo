from fastapi import FastAPI, Depends
from app.database.database import engine, Base
from app.routers import auth, user, product, menu, order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

# 1. Création des tables (pour que tes burgers s'enregistrent vraiment)
Base.metadata.create_all(bind=engine)

# 2. Configuration du cadenas Swagger
# C'est cette ligne (tokenUrl="login") qui fait réapparaître le bouton Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="Wacdo API",
    # On définit ici que l'API utilise OAuth2 pour que le cadenas apparaisse partout
    security=[{"OAuth2PasswordBearer": []}]
)

# 3. Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Inclusion des routes (bien propres, sans boucle for qui bugue)
app.include_router(auth.router) # Le tag "Auth" est sûrement déjà dans auth.py
app.include_router(user.router)
app.include_router(product.router)
app.include_router(menu.router)
app.include_router(order.router)

@app.get("/")
def read_root():
    return {"message": "Serveur opérationnel - Bienvenue chez Wacdo !"}

# Route de test pour vérifier si tu es connecté
@app.get("/auth-check", tags=["Security"])
def check_connection(token: str = Depends(oauth2_scheme)):
    return {"status": "Connecté", "token": token}