from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, UniqueConstraint

from app.database import Base


class Environment(str, Enum):
    DEVELOPMENT = "development"
    CI = "ci"
    PRODUCTION = "production"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    environment = Column(SQLEnum(Environment), nullable=False, default=Environment.DEVELOPMENT)
    created_at = Column(String)
    updated_at = Column(String)

    # Ensure (name, environment) uniqueness
    __table_args__ = (
        UniqueConstraint('name', 'environment', name='uq_item_name_environment'),
    )
