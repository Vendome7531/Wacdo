from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
import shutil
import os

from app.database.database import get_db
from app.models.user import UserModel
from app.models.product import ProductModel  # <--- Ajouté pour le GET unique
from app.schemas.product import ProductSchema, ProductCreate, ProductUpdate, ProductDeleteResponse
from app.controllers import product_controller
from app.dependencies import admin_only

router = APIRouter(prefix="/products", tags=["Produits"])

# --- LECTURE : Accessible à tous ---
@router.get("/", response_model=list[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    """Récupère la liste de tous les produits."""
    return product_controller.get_all_products(db)  

# --- LECTURE D'UN PRODUIT UNIQUE ---
@router.get("/{product_id}", response_model=ProductSchema)
def get_one_product(product_id: int, db: Session = Depends(get_db)):
    """Récupère un produit spécifique par son ID."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

# --- CRÉATION : Admin seulement (Version avec IMAGE) ---
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def add_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None), # <--- Champ pour l'image
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Ajoute un nouveau produit avec une image (Admin uniquement)."""
    
    image_url = None
    if image:
        # Création du dossier si inexistant
        os.makedirs("static/images", exist_ok=True)
        file_path = f"static/images/{image.filename}"
        
        # Sauvegarde physique du fichier
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/{file_path}"

    # On passe les données au contrôleur
    return product_controller.create_new_product(
        db, 
        name=name, 
        description=description, 
        price=price, 
        category=category,
        image_url=image_url
    )

# --- MODIFICATION ---
@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_data: ProductUpdate, 
    product_id: int = Path(..., description="L'identifiant unique du produit à modifier dans le catalogue"),
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    """
    **Mettre à jour un produit** : Permet de modifier les détails d'un article existant (nom, prix, description, etc.).
    
    *Cette action est réservée aux administrateurs.*
    """
    return product_controller.update_product(db, product_id, product_data)

# --- SUPPRESSION ---
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int = Path(..., description="L'identifiant unique du produit à supprimer définitivement"),
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    """
    **Supprimer un produit** : Retire un article du catalogue. 
    *Attention : Cette opération est irréversible.*
    """
    return product_controller.delete_product(db, product_id)