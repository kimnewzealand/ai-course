from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Environment(str, Enum):
    DEVELOPMENT = "development"
    CI = "ci"
    PRODUCTION = "production"


class ItemBase(BaseModel):
    name: str = Field(
        min_length=1, max_length=100, description="Item name (1-100 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Item description (optional, max 500 characters)",
    )
    environment: Environment = Field(description="Deployment environment")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(BaseModel):
    id: int = Field(description="Unique item identifier")
    name: str = Field(description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    environment: Environment = Field(description="Deployment environment")
    created_at: str = Field(description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)
