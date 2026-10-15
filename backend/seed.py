"""Populate the database with a little sample data.

Run from the `backend/` folder:  python seed.py
"""

from app import models
from app.database import Base, SessionLocal, engine


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Product).first():
            print("Database already has products; skipping seed.")
            return

        beverages = models.Category(name="Beverages", description="Drinks & juices")
        snacks = models.Category(name="Snacks", description="Chips, nuts, bars")
        db.add_all([beverages, snacks])
        db.flush()  # assigns ids

        db.add_all(
            [
                models.Product(
                    name="Orange Juice 1L",
                    sku="BEV-OJ-1L",
                    price=3.50,
                    quantity=40,
                    low_stock_threshold=10,
                    category_id=beverages.id,
                ),
                models.Product(
                    name="Sparkling Water 500ml",
                    sku="BEV-SW-500",
                    price=1.20,
                    quantity=8,
                    low_stock_threshold=12,
                    category_id=beverages.id,
                ),
                models.Product(
                    name="Potato Chips 150g",
                    sku="SNK-PC-150",
                    price=2.00,
                    quantity=25,
                    low_stock_threshold=5,
                    category_id=snacks.id,
                ),
            ]
        )
        db.commit()
        print("Seeded sample categories and products.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
