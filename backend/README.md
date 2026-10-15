# Store Inventory — Backend

A small **FastAPI + SQLAlchemy** backend for managing a store's inventory
(categories, products, stock levels). No authentication yet — user login will
be added later on a feature branch.

## Tech stack

- **FastAPI** — web framework & automatic OpenAPI docs
- **SQLAlchemy 2.0** — ORM
- **SQLite** — zero-config default database (swap `DATABASE_URL` for Postgres/MySQL later)
- **Pydantic v2** — request/response validation

## Project layout

```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, startup, route registration
│   ├── config.py        # Settings from env / .env
│   ├── database.py      # Engine, session, Base, get_db dependency
│   ├── models.py        # ORM models: Category, Product
│   ├── schemas.py       # Pydantic request/response models
│   ├── crud.py          # Data-access + domain logic
│   └── routers/
│       ├── categories.py
│       └── products.py
├── seed.py              # Optional sample data
├── requirements.txt
└── .env.example
```

## Setup & run

From the `backend/` folder:

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (optional) configure environment
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. (optional) load sample data
python seed.py

# 5. Run the API
uvicorn app.main:app --reload
```

- API base URL: `http://127.0.0.1:8000`
- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Health check: `GET /health`

## API endpoints

All endpoints are prefixed with `/api/v1`.

### Categories
| Method | Path                      | Description        |
|--------|---------------------------|--------------------|
| GET    | `/categories`             | List categories    |
| POST   | `/categories`             | Create a category  |
| GET    | `/categories/{id}`        | Get one category   |
| PATCH  | `/categories/{id}`        | Update a category  |
| DELETE | `/categories/{id}`        | Delete a category  |

### Products
| Method | Path                       | Description                                   |
|--------|----------------------------|-----------------------------------------------|
| GET    | `/products`                | List/search products (`search`, `category_id`, `low_stock`, `skip`, `limit`) |
| POST   | `/products`                | Create a product                              |
| GET    | `/products/{id}`           | Get one product                               |
| PATCH  | `/products/{id}`           | Update a product                              |
| POST   | `/products/{id}/stock`     | Adjust stock (`delta` +/-)                    |
| DELETE | `/products/{id}`           | Delete a product                              |

### Example: create a product

```bash
curl -X POST http://127.0.0.1:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Milk 1L","sku":"DRY-MILK-1L","price":1.80,"quantity":30,"low_stock_threshold":8}'
```

### Example: restock / sell

```bash
# add 12 units
curl -X POST http://127.0.0.1:8000/api/v1/products/1/stock \
  -H "Content-Type: application/json" -d '{"delta": 12, "reason": "restock"}'

# sell 3 units
curl -X POST http://127.0.0.1:8000/api/v1/products/1/stock \
  -H "Content-Type: application/json" -d '{"delta": -3, "reason": "sale"}'
```

## Notes / next steps

- Tables are auto-created on startup for convenience. Introduce **Alembic**
  migrations before this goes to production.
- **User login / auth** is intentionally left out — it will arrive on a
  dedicated feature branch.
