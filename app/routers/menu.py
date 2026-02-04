from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.menu import MenuSchema, MenuCreate 
from app.controllers import menu_controller
from app.dependencies import admin_only
from app.models.user import UserModel
from app.schemas.menu import MenuCreate, MenuSchema, MenuDeleteResponse  

router = APIRouter(prefix="/menus", tags=["Menus"])

# --- LECTURE : Public ---
@router.get("/", response_model=list[MenuSchema])
def list_menus(db: Session = Depends(get_db)):
    """Liste tous les menus disponibles."""
    return menu_controller.get_all_menus(db)

# --- LECTURE D'UN MENU (ID): Accessible à tous (Agent, Préparateur, Admin) ---

@router.get("/{menu_id}", response_model=MenuSchema) # Ou MenuResponse selon ton fichier
def read_menu(
    menu_id: int = Path(..., description="L'identifiant unique du menu (ex: 1 pour le Menu Best Of)"),
    db: Session = Depends(get_db)
):
    """
    **Consulter un menu** : Affiche la composition d'un menu spécifique et son prix remisé.
    """
    return menu_controller.get_menu_by_id(db, menu_id=menu_id)

# --- CRÉATION : Admin uniquement ---
@router.post("/", response_model=MenuSchema, status_code=status.HTTP_201_CREATED)
def create_menu(
    menu: MenuCreate, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Crée un nouveau menu (Admin seulement)."""
    return menu_controller.create_new_menu(db, menu)

# --- SUPPRESSION : Admin uniquement ---
@router.delete("/{menu_id}", response_model=MenuDeleteResponse)
def delete_menu(
    menu_id: int, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Supprime un menu (Admin seulement)."""
    if not menu_controller.delete_menu_by_id(db, menu_id):
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return {"message": "Menu supprimé avec succès"}

@router.put("/{menu_id}", response_model=MenuSchema)
def update_menu(
    menu_id: int, 
    menu_data: MenuCreate, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Met à jour un menu existant (Admin uniquement)."""
    updated_menu = menu_controller.update_menu_info(db, menu_id, menu_data)
    if not updated_menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return updated_menu
