"""Data-access layer: all database reads/writes live here.

Functions raise HTTPException for the common domain errors (not found,
duplicate SKU/name) so the route handlers stay thin.
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# --------------------------------------------------------------------------- #
# Category
# --------------------------------------------------------------------------- #
def get_category(db: Session, category_id: int) -> models.Category:
    category = db.get(models.Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not found",
        )
    return category


def list_categories(db: Session) -> list[models.Category]:
    return list(db.scalars(select(models.Category).order_by(models.Category.name)))


def create_category(db: Session, data: schemas.CategoryCreate) -> models.Category:
    exists = db.scalar(
        select(models.Category).where(models.Category.name == data.name)
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{data.name}' already exists",
        )
    category = models.Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session, category_id: int, data: schemas.CategoryUpdate
) -> models.Category:
    category = get_category(db, category_id)
    updates = data.model_dump(exclude_unset=True)

    new_name = updates.get("name")
    if new_name and new_name != category.name:
        clash = db.scalar(
            select(models.Category).where(models.Category.name == new_name)
        )
        if clash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category '{new_name}' already exists",
            )

    for field, value in updates.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    db.delete(category)
    db.commit()


# --------------------------------------------------------------------------- #
# Product
# --------------------------------------------------------------------------- #
def get_product(db: Session, product_id: int) -> models.Product:
    product = db.get(models.Product, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )
    return product


def list_products(
    db: Session,
    *,
    search: str | None = None,
    category_id: int | None = None,
    low_stock: bool = False,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Product]:
    stmt = select(models.Product)

    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            models.Product.name.ilike(pattern) | models.Product.sku.ilike(pattern)
        )
    if category_id is not None:
        stmt = stmt.where(models.Product.category_id == category_id)
    if low_stock:
        stmt = stmt.where(
            models.Product.quantity <= models.Product.low_stock_threshold
        )

    stmt = stmt.order_by(models.Product.name).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def _ensure_category_exists(db: Session, category_id: int | None) -> None:
    if category_id is not None and db.get(models.Category, category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {category_id} not found",
        )


def _ensure_sku_free(db: Session, sku: str, *, exclude_id: int | None = None) -> None:
    stmt = select(models.Product).where(models.Product.sku == sku)
    if exclude_id is not None:
        stmt = stmt.where(models.Product.id != exclude_id)
    if db.scalar(stmt):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A product with SKU '{sku}' already exists",
        )


def create_product(db: Session, data: schemas.ProductCreate) -> models.Product:
    _ensure_sku_free(db, data.sku)
    _ensure_category_exists(db, data.category_id)

    product = models.Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session, product_id: int, data: schemas.ProductUpdate
) -> models.Product:
    product = get_product(db, product_id)
    updates = data.model_dump(exclude_unset=True)

    if "sku" in updates and updates["sku"] != product.sku:
        _ensure_sku_free(db, updates["sku"], exclude_id=product_id)
    if "category_id" in updates:
        _ensure_category_exists(db, updates["category_id"])

    for field, value in updates.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def adjust_stock(
    db: Session, product_id: int, adjustment: schemas.StockAdjustment
) -> models.Product:
    product = get_product(db, product_id)
    new_quantity = product.quantity + adjustment.delta
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot adjust stock by {adjustment.delta}: "
                f"quantity would drop below zero (current: {product.quantity})"
            ),
        )
    product.quantity = new_quantity
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
