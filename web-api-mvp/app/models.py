from sqlalchemy import Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
