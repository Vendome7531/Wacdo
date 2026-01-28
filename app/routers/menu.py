from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.menu import MenuCreate, MenuSchema
from app.controllers import menu_controller

router = APIRouter(prefix="/menus", tags=["Menus"])

@router.post("/", response_model=MenuSchema)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    return menu_controller.create_new_menu(db, menu)

@router.get("/", response_model=List[MenuSchema])
def read_all_menus(db: Session = Depends(get_db)):
    return menu_controller.get_all_menus(db)

@router.get("/{menu_id}", response_model=MenuSchema)
def read_one_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = menu_controller.get_menu_by_id(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return db_menu

@router.put("/{menu_id}", response_model=MenuSchema)
def update_menu(menu_id: int, menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = menu_controller.update_menu_info(db, menu_id, menu)
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return db_menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    success = menu_controller.delete_menu_by_id(db, menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return {"message": f"Le menu {menu_id} a été supprimé"}