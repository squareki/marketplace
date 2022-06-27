import enum

from app.db import engine

from sqlalchemy import DateTime, Column, Enum, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

# Make the DeclarativeMeta
Base = declarative_base()

@enum.unique
class ShopUnitType(str, enum.Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"

class ShopUnit(Base):
    __tablename__ = "shopunits"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    parentId = Column(UUID(as_uuid=True), ForeignKey("shopunits.id"))
    type = Column(Enum(ShopUnitType), nullable=False)
    price = Column(Integer)
    children = relationship("ShopUnit", cascade="all, delete")

# Create the tables in the database
# (commented due to using alembic migrations)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)