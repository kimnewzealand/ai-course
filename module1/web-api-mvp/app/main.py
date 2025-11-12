from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal, init_db
from dotenv import load_dotenv
from typing import List
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Items API",
    description="A REST API for managing items",
    version="1.0.0",
    lifespan=lifespan
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API v1 Router
api_v1 = APIRouter(prefix="/v1", tags=["items"])

@api_v1.get("/items", response_model=List[schemas.Item], summary="Get all items")
def read_items_v1(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    """Retrieve a list of items with optional pagination."""
    return crud.get_items(db, limit=limit, offset=offset)

@api_v1.post("/items", response_model=schemas.Item, summary="Create a new item")
def create_item_v1(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Create a new item with the provided data."""
    return crud.create_item(db, item)

@api_v1.get("/items/{item_id}", response_model=schemas.Item, summary="Get item by ID")
def read_item_v1(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific item by its ID."""
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@api_v1.put("/items/{item_id}", response_model=schemas.Item, summary="Update an item")
def update_item_v1(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item with new data."""
    updated_item = crud.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@api_v1.delete("/items/{item_id}", summary="Delete an item")
def delete_item_v1(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by its ID."""
    deleted = crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

# Health check endpoint
@app.get("/health", summary="Health check", tags=["health"])
def health_check():
    """Check if the API is healthy and running."""
    return {"status": "healthy", "version": "1.0.0"}

# Mount the router
app.include_router(api_v1)
