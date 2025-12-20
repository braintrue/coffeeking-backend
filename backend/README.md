# CoffeeKing Backend

This repository contains a small FastAPI service that powers the backend for
the **CoffeeKing** application.  It provides a minimal MVP for handling
authentication, menu management, table management, ordering and matching.  The
project is designed to be easy to extend for future functionality.

## 📁 프로젝트 구조

- `app/` – The application code.  This package contains the FastAPI app
  definition, configuration, database helpers, models, schemas, routers and
  utilities.
  - `main.py` – FastAPI application entry‐point.  It registers all
    routers, applies CORS middleware and seeds the database on startup.
  - `config.py` – Pydantic settings model used to load configuration from
    environment variables or defaults.
  - `database.py` – SQLAlchemy engine and session helpers.
  - `models/` – SQLAlchemy models for users, menus, tables, orders and
    matches.
  - `schemas/` – Pydantic models used for request and response validation.
  - `routers/` – FastAPI routers handling auth, menus, tables, orders and
    matches.  Routers encapsulate the API endpoints and associated
    dependencies.
  - `utils/` – Utility modules for security (JWT, password hashing) and
    database seeding.
- `data/menus_seed.json` – Seed data used to populate the menus table
  automatically on startup.
- `tests/` – A small suite of tests validating the authentication flow and
  order creation logic.

## 🚀 빠른 시작

### 로컬 개발

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  You can explore the
OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### Docker

To run the service in Docker:

```bash
docker compose up --build
```

Once the containers are up, visit `http://localhost:8000/docs` to verify the
service is running.

## 🔑 환경 변수

Use the `.env.example` file as a template for your environment.  Copy it to
`.env` and adjust values as necessary.  At minimum you should change the
`JWT_SECRET_KEY`.

```env
DATABASE_URL=sqlite:///./coffeeking.db
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🧰 기본 기능

The current MVP provides the following features:

- **Authentication**: Users can register, log in and receive a JWT.  The
  `/auth/me` endpoint returns the current user when provided with a valid
  token.
- **Menu management**: Create, list, update and delete menu items via the
  `/menus` endpoints.  Menus are seeded from `menus_seed.json` on startup
  if the table is empty.
- **Table management**: Create tables, list them, fetch a specific table,
  update their status or delete them via the `/tables` endpoints.
- **Ordering**: Authenticated users can create orders which calculate the
  total price based on the menu items selected.  Orders are always
  associated with the user making the request; any `user_id` in the payload
  is ignored to prevent tampering.
- **Matching**: Users can create a match on a table and others can join.
  Match hosts and guests are always set based on the authenticated user.

The project is intentionally minimal but structured so that additional domain
logic can be added easily.