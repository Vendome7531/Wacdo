from fastapi import FastAPI, Depends
from app.database.database import engine, Base
from app.routers import auth, user, product, menu, order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

# 1. Création des tables
Base.metadata.create_all(bind=engine)

# 2. Configuration du cadenas Swagger
# Cette instance sert à extraire le token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="Wacdo API",
    description="Système de gestion interne Wacdo",
    version="1.0.0"
    # On a supprimé la ligne 'security=' ici pour nettoyer Swagger
)

# 3. Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Inclusion des routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(menu.router)
app.include_router(order.router)

@app.get("/")
def read_root():
    return {"message": "Serveur opérationnel - Bienvenue chez Wacdo !"}

# Route de test
@app.get("/auth-check", tags=["Security"])
def check_connection(token: str = Depends(oauth2_scheme)):
    return {"status": "Connecté", "token": token}