"""Product endpoints, including stock adjustment."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[schemas.ProductRead])
def list_products(
    db: Session = Depends(get_db),
    search: str | None = Query(None, description="Match product name or SKU."),
    category_id: int | None = Query(None, description="Filter by category."),
    low_stock: bool = Query(False, description="Only items at/below their threshold."),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return crud.list_products(
        db,
        search=search,
        category_id=category_id,
        low_stock=low_stock,
        skip=skip,
        limit=limit,
    )


@router.post(
    "", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED
)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    return crud.create_product(db, payload)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.patch("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    return crud.update_product(db, product_id, payload)


@router.post("/{product_id}/stock", response_model=schemas.ProductRead)
def adjust_stock(
    product_id: int,
    payload: schemas.StockAdjustment,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    """Add or remove stock relative to the current quantity."""
    return crud.adjust_stock(db, product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    crud.delete_product(db, product_id)
