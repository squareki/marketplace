import logging
from typing import List

from sqlalchemy import null, text
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, NoResultFound
from sqlalchemy.dialects.postgresql import ARRAY, array

from app.marketplace.models.models import *
from app.marketplace.schemas.schemas import *
import app.marketplace.schemas.schemas as sc

import os
import uuid

from app.exceptions import ObjectNotFoundError
from app.exceptions import InvalidDataError

def create_unit(unit: ShopUnitImport, date: DateTime, db: Session):
    try:
        db_unit = unit.orm_create()
        db_unit.date = date
        print(db_unit)
        db.add(db_unit)
        categoryId = unit.parentId
        while categoryId != None:
            parent = db.query(models.ShopUnit).filter(models.ShopUnit.id == categoryId).first()
            parent.date = date
            db.merge(parent)
            categoryId = parent.parentId
    except ValueError as e:
        raise InvalidDataError

def import_units(request: ShopUnitImportRequest, db: Session):
    try:
        for unit in request.items:
            create_unit(unit, request.updateDate, db)
        db.commit()
    except InvalidDataError:
        raise InvalidDataError
        

def delete_unit(id: str, db: Session):
    try:
        unit = db.query(models.ShopUnit).filter(models.ShopUnit.id == id).first()
        if unit is None:
            raise ObjectNotFoundError
    except DataError:
        raise InvalidDataError
    
    db.delete(unit)
    db.commit()

def get_unit_recursive2(id: str, db: Session) -> sc.ShopUnit:
    path = array(id)
    topquery = db.query(models.ShopUnit).filter(models.ShopUnit.id == id)
    topquery.add_columns(path.label("path")).all()
    # if topquery.first() is None:
    #     print("sshit")
    #     raise ValueError(f"Unit with id {id} does not exist in database")
    
    topquery = topquery.cte("unitnested", recursive=True)

    bottomquery = db.query(models.ShopUnit).filter(models.ShopUnit.parentId == id)
    t = text(f"array_append(path, {bottomquery})")
    bottomquery = bottomquery.join(topquery, ShopUnit.parentId == topquery.id)

def get_unit_recursive(id: str, db: Session) -> sc.ShopUnit:
    #topquery = db.query(models.ShopUnit).filter(models.ShopUnit.id == id)
    # if topquery.first() is None:
    #     print("sshit")
    #     raise ValueError(f"Unit with id {id} does not exist in database")
    def find_children(id, rows):
        # ids = []
        # for r in rows:
        #     f = sc.ShopUnit.from_orm(r)
        #     print(f"{f.parentId} == {id} ? {f.parentId == id}")
        #     if f.parentId == id:
        #         ids.append(f.parentId)
        # if len(ids) == 0:
        #     return []
        # print(ids)

        # children = []
        # num = len(ids)
        # for r in rows:
        #     f = sc.ShopUnit.from_orm(r)
        #     print(f"{f.parentId} == {id} ? {f.parentId == id}")
        #     if f.parentId == id:
        #         f.children = find_children(f.id, rows)
        #         children.append(f)
        #         num -= 1
        #         if num == 0:
        #             print(children)
        #             return children

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
    with open(filename, "r") as file:
        contents = file.read()
        formated = contents.replace("{id}", f"{id}")
        print(formated)
        query = text(formated)
        result = db.execute(query).all()
        for u in result:
            form_id = uuid.UUID(id)
            #print(f"{u[0]} == {form_id} ? {u[0] == form_id}")
            #print(u.dict())
            if u[0] == form_id:
                parent = sc.ShopUnit.from_orm(u)
                parent.children = find_children(form_id, result)
                return parent
        #return sc.ShopUnit.from_orm(result)


def get_unit(id: str, db: Session) -> sc.ShopUnit:
    unit = db.query(models.ShopUnit).filter(models.ShopUnit.id == id).first()
    if unit is None:
        print("sshit")
        raise ValueError(f"Unit with id {id} does not exist in database")
    
    print(unit)
    print(sc.ShopUnit.from_orm(unit))
    print(sc.ShopUnit.from_orm(unit).dict())
    return sc.ShopUnit.from_orm(unit)
