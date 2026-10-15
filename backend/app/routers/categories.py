"""Category endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.post(
    "", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED
)
def create_category(
    payload: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    return crud.create_category(db, payload)


@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_category(db, category_id)


@router.patch("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    payload: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    return crud.update_category(db, category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _user: models.User = Depends(get_current_user),
):
    crud.delete_category(db, category_id)
