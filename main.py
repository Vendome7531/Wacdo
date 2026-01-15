from fastapi import FastAPI
import models # On importe ton fichier models.py
from database import engine # On importe le moteur de database.py

# CETTE LIGNE EST LA CLÉ :
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wacdo API")


print('Bienvenue chez Wacdo !')

from fastapi import FastAPI
from models import ProductSchema # On importe le schéma qu'on a préparé tout à l'heure

app = FastAPI(title="Wacdo API")

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de commande Wacdo !"}

@app.get("/status")
def get_status():
    return {"status": "Le back-end fonctionne parfaitement"}