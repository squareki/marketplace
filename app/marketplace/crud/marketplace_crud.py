from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError

from app.marketplace.models.models import *
from app.marketplace.schemas.schemas import *
import app.marketplace.schemas.schemas as sc

import os
import uuid

from app.exceptions import ObjectNotFoundError
from app.exceptions import BaseError, DuplicateObjectError, InvalidDataError

def create_unit(unit: ShopUnitImport, date: DateTime, db: Session):
    try:
        db_unit = unit.orm_create()
        db_unit.date = date
        db.add(db_unit)

        categoryId = unit.parentId
        while categoryId != None:
            parent = db.query(models.ShopUnit).filter(models.ShopUnit.id == categoryId).first()
            parent.date = date
            db.merge(parent)
            categoryId = parent.parentId
    except IntegrityError:
        raise DuplicateObjectError
    except:
        raise InvalidDataError

def import_units(request: ShopUnitImportRequest, db: Session):
    try:
        for unit in request.items:
            create_unit(unit, request.updateDate, db)
        db.commit()
    except DuplicateObjectError:
        db.rollback()
        raise DuplicateObjectError
    except InvalidDataError:
        db.rollback()
        raise InvalidDataError
        

def delete_unit(id: str, db: Session):
    try:
        unit = db.query(models.ShopUnit).filter(models.ShopUnit.id == id).first()
        if unit is None:
            db.rollback()
            raise ObjectNotFoundError
    except DataError:
        db.rollback()
        raise InvalidDataError
    
    db.delete(unit)
    db.commit()

def get_unit_recursive(id: str, db: Session) -> sc.ShopUnit:
    def find_children(id, rows):
        children = []
        for r in rows:
            f = sc.ShopUnit.from_orm(r)
            print(f"{f.parentId} == {id} ? {f.parentId == id}")
            if f.parentId == id:
                if f.type == ShopUnitType.CATEGORY:
                    f.children = find_children(f.id, rows)
                else:
                    f.children = None
                children.append(f)
        return children
    
    filename = os.path.join(os.path.dirname(__file__), "marketplace_cte.sql")
    with open(filename, "r") as (file, err):
        if err:
            raise BaseError(message="Internal load failed")

        contents = file.read()
        formated = contents.replace("{id}", f"{id}")
        query = text(formated)

        result = db.execute(query).all()
        for u in result:
            form_id = uuid.UUID(id)
            if u[0] == form_id:
                parent = sc.ShopUnit.from_orm(u)
                parent.children = find_children(form_id, result)
                return parent
    
    raise ObjectNotFoundError


# An attempt to make the CTE with SQLAlchemy
# from sqlalchemy.dialects.postgresql import ARRAY, array
# def get_unit_recursive2(id: str, db: Session) -> sc.ShopUnit:
#     path = array(id)
#     topquery = db.query(models.ShopUnit).filter(models.ShopUnit.id == id)
#     topquery.add_columns(path.label("path")).all()
#     # if topquery.first() is None:
#     #     raise ValueError(f"Unit with id {id} does not exist in database")
    
#     topquery = topquery.cte("unitnested", recursive=True)

#     bottomquery = db.query(models.ShopUnit).filter(models.ShopUnit.parentId == id)
#     t = text(f"array_append(path, {bottomquery})")
#     bottomquery = bottomquery.join(topquery, ShopUnit.parentId == topquery.id)