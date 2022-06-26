from datetime import datetime, timezone
from enum import Enum

from typing import List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field, PrivateAttr, validator

from app.marketplace.models import models

from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_pydantic_orm import ORMBaseSchema

class ShopUnitType(str, Enum):
    OFFER: str = "OFFER"
    CATEGORY: str = "CATEGORY"

class ShopUnitImport(ORMBaseSchema):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None

    _orm_model = PrivateAttr(models.ShopUnit)

    class Config:
        use_enum_values = True

class ShopUnit(ShopUnitImport):
    date: datetime
    children: Optional[List["ShopUnit"]] = None

    #_orm_model: DeclarativeMeta = PrivateAttr(models.ShopUnit)
    _orm_model = PrivateAttr(models.ShopUnit)


    # class Config:
    #     orm_mode = True
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', #.isoformat(timespec="milliseconds")
        }

    # @validator("date", pre=True)
    # def date_validate(cls, v):
    #     return datetime.fromisoformat(v)

class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime

    # class Config:
    #     json_encoders = {
    #         datetime: lambda v: v.isoformat(),
    #     }

    # @validator("updateDate", pre=True)
    # def date_validate(cls, v):
    #     return datetime.fromisoformat(v)

class ShopUnitStatisticUnit(ShopUnit):
    pass

class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]

ShopUnit.update_forward_refs()