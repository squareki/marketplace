from fastapi import APIRouter, Depends

from app.db import get_db

from sqlalchemy.orm import Session

from app.marketplace.crud import marketplace_crud
from app.marketplace.schemas.schemas import *

router = APIRouter(
    tags=["marketplace"],
)

@router.post("/imports")
def process_import_request(request: ShopUnitImportRequest, db: Session = Depends(get_db)):
    return marketplace_crud.import_units(request, db)

@router.delete("/delete/{id}")
def delete_node(id: str, db: Session = Depends(get_db)):
    return marketplace_crud.delete_unit(id, db)

@router.get("/nodes/{id}", response_model=ShopUnit)
def get_node(id: str, db: Session = Depends(get_db)):
    return marketplace_crud.get_unit_recursive(id, db)
