# FastAPI Template - Clean Layered Architecture

A production-ready FastAPI template with a layered architecture (controller, service, repository), **MySQL** persistence via **SQLAlchemy**, **Pydantic** request/response schemas, and optional **Docker Compose** for the database (and optionally the app).

## Table of Contents

- [FastAPI Template - Clean Layered Architecture](#fastapi-template---clean-layered-architecture)
  - [Table of Contents](#table-of-contents)
  - [🚀 Key Features](#-key-features)
  - [📋 Prerequisites](#-prerequisites)
    - [Verify Installation](#verify-installation)
  - [⚡ Quick Start](#-quick-start)
  - [🗄️ Database & Seeding](#️-database--seeding)
  - [✅ STEP-BY-STEP FASTAPI SETUP (Layered Architecture)](#-step-by-step-fastapi-setup-layered-architecture)
  - [📁 Project Structure](#-project-structure)
  - [🏗️ Architecture Overview](#️-architecture-overview)
    - [🏗️ FINAL FLOW (Important to Understand)](#️-final-flow-important-to-understand)
    - [Layer Responsibilities](#layer-responsibilities)
  - [🔌 API Endpoints](#-api-endpoints)
    - [User resource (CRUD)](#user-resource-crud)
    - [List Users](#list-users)
    - [Get User by ID](#get-user-by-id)
    - [Create User](#create-user)
    - [Update User](#update-user)
    - [Delete User](#delete-user)
  - [🧪 Development](#-development)
    - [Running in Development Mode](#running-in-development-mode)
    - [Running in Production Mode](#running-in-production-mode)
    - [Code Structure Guidelines](#code-structure-guidelines)
  - [🔧 Configuration](#-configuration)
    - [Environment Variables](#environment-variables)
    - [Adding New Features](#adding-new-features)
  - [📦 Dependencies](#-dependencies)
    - [Core Dependencies](#core-dependencies)
    - [Updating Dependencies](#updating-dependencies)
  - [🚀 Deployment](#-deployment)
    - [Docker Compose (MySQL)](#docker-compose-mysql)
    - [Docker Image (App Only)](#docker-image-app-only)
    - [Cloud Platforms](#cloud-platforms)
  - [🐛 Troubleshooting](#-troubleshooting)
    - [Common Issues](#common-issues)
  - [📚 Additional Resources](#-additional-resources)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [👤 Author](#-author)

## 🚀 Key Features

- **🏗️ Clean Layered Architecture**: Controller, service, and repository layers with clear boundaries
- **💉 Dependency Injection**: FastAPI `Depends` for services and SQLAlchemy sessions (request-scoped DB access)
- **🗄️ MySQL + SQLAlchemy**: ORM models under `app/models/`, repositories use `Session` for queries
- **📋 Pydantic Schemas**: `UserCreate`, `UserUpdate`, and `UserResponse` in `app/schemas/` (`from_attributes` on responses)
- **✏️ User CRUD**: Full create / read / update / delete for users via `/api/v1/users` (repository commits; duplicate emails return **409 Conflict**)
- **🌱 Seed Scripts**: Standalone scripts under `scripts/` to populate data (`python -m scripts.seed_users` or `python -m scripts.seed_all`)
- **🐳 Docker Compose**: MySQL 8 service with health checks and persistent volume (optional app service in `docker-compose.yml`)
- **🔌 API Versioning**: Routes under `/api/v1`
- **⚡ FastAPI**: Automatic OpenAPI docs (Swagger UI / ReDoc)
- **🔄 Startup**: SQLAlchemy `create_all` on startup for development tables (use migrations for production)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **pip** (Python package installer)
- **MySQL 8** (local install, or run only the DB via Docker Compose)
- **Docker Desktop** (optional, recommended for MySQL without a local server)
- **Git** (optional, for version control)
- Basic knowledge of Python and REST APIs

### Verify Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version
```

## ⚡ Quick Start

**1. Start MySQL**

Either install MySQL locally and create a database and user, or start only the database with Docker:

```bash
docker compose up -d
```

This starts the `db` service (MySQL 8) on port `3306` by default. Defaults: database `appdb`, user `appuser`, password `apppass`, root password `rootsecret` (override with env vars or a `.env` file used by Compose).

**2. Configure the app**

Set `DATABASE_URL` so it matches your MySQL credentials (PyMySQL driver):

```env
DATABASE_URL=mysql+pymysql://appuser:apppass@127.0.0.1:3306/appdb
```

You can place this in a `.env` file in the project root; `app/core/config.py` loads it via `pydantic-settings`.

**3. Install and run**

```bash
# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Optional: load sample users (requires DB running)
python -m scripts.seed_users

uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/api/v1/users` (list users)
- `http://127.0.0.1:8000/api/v1/users/1` (user by id, after seeding)

## 🗄️ Database & Seeding

- **Tables**: Created on app startup with SQLAlchemy `Base.metadata.create_all` (development only; use Alembic or another migration tool for production).
- **Seed data**: Run separately when you want demo rows (by default **50** users with rotating roles):

```bash
python -m scripts.seed_users
# or run all seed entrypoints
python -m scripts.seed_all
```

If you run the API in Docker and MySQL is another Compose service, use the same commands with Compose, for example:

```bash
docker compose run --rm <app-service-name> python -m scripts.seed_users
```

Uncomment and configure the `app` service in `docker-compose.yml` if you want the API containerized; otherwise run `uvicorn` on the host against the Compose MySQL URL shown above.

**Schema changes**: If you change SQLAlchemy models after tables already exist, drop the database or volume and recreate, or add migrations—otherwise MySQL will not match the models.

## ✅ STEP-BY-STEP FASTAPI SETUP (Layered Architecture)

The full tutorial (scaffold, repository/service/controller layers, startup wiring, run, and test) lives in **[docs/step-by-step-setup.md](docs/step-by-step-setup.md)**.

## 📁 Project Structure

```
fastapi-template/
├── app/
│   ├── main.py                     # FastAPI app, router include, DB create_all on startup
│   │
│   ├── api/v1/
│   │   └── controller.py           # HTTP routes; uses response_model with Pydantic schemas
│   │
│   ├── services/
│   │   └── user_service.py         # Business logic
│   │
│   ├── repositories/
│   │   └── user_repository.py      # SQLAlchemy Session-based data access
│   │
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/                    # Pydantic API models (UserCreate, UserUpdate, UserResponse)
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   ├── db/
│   │   ├── base.py                 # Declarative Base
│   │   └── session.py              # engine, SessionLocal, get_db
│   │
│   └── core/
│       ├── config.py               # Settings (DATABASE_URL from env)
│       └── dependencies.py         # get_db, get_user_repository, get_user_service
│
├── scripts/
│   ├── seed_users.py               # Seed users (run manually)
│   └── seed_all.py                 # Entry point for all seeds
│
├── dockerfile                      # App image (uvicorn)
├── docker-compose.yml              # MySQL + optional app service
├── requirements.txt
├── Readme.md
└── docs/
    └── step-by-step-setup.md
```

## 🏗️ Architecture Overview

### 🏗️ FINAL FLOW (Important to Understand)

```
HTTP Request
   ↓
Controller (API)
   ↓
Service Layer (Business Logic)
   ↓
Repository (DB / API)
```

**Request flow:**

- **Repositories** receive a SQLAlchemy `Session` (injected per request via `get_db`).
- **Services** receive a repository instance from FastAPI `Depends`.
- **Controllers** depend on services and return Pydantic-friendly dicts or ORM-backed `response_model` types.

### Layer Responsibilities

1. **Controller Layer (`app/api/`)**
   - HTTP routing, status codes, `response_model` (Pydantic schemas)

2. **Service Layer (`app/services/`)**
   - Business rules and orchestration; calls repositories

3. **Repository Layer (`app/repositories/`)**
   - SQLAlchemy queries via `Session`; returns plain dicts or ORM rows as needed for services/schemas

4. **Models (`app/models/`)**
   - SQLAlchemy ORM table definitions

5. **Schemas (`app/schemas/`)**
   - Pydantic models: `UserCreate` (POST body), `UserUpdate` (optional fields for PATCH), `UserResponse` (read models)

6. **Core (`app/core/`)**
   - `config.py`: `DATABASE_URL` and settings
   - `dependencies.py`: `get_db`, repository and service providers

## 🔌 API Endpoints

Base path: **`/api/v1`**.

Read responses use **`UserResponse`**: `id`, `name`, `email`, `role`.

### User resource (CRUD)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users` | List all users |
| `GET` | `/users/{user_id}` | Get one user |
| `POST` | `/users` | Create user (body: `UserCreate`) → **201** |
| `PATCH` | `/users/{user_id}` | Partial update (body: `UserUpdate`) |
| `DELETE` | `/users/{user_id}` | Delete user → **204** (no body) |

- **409 Conflict**: `POST` or `PATCH` when `email` is already used by another user.
- **404 Not Found**: `GET` / `PATCH` / `DELETE` when `user_id` does not exist.

### List Users

**Endpoint:** `GET /api/v1/users`

Returns an array of users.

**Example:**

```bash
curl http://localhost:8000/api/v1/users
```

### Get User by ID

**Endpoint:** `GET /api/v1/users/{user_id}`

**Parameters:**

- `user_id` (path, integer): User primary key

**Response:**

- `200 OK`: User found

  ```json
  {
    "id": 1,
    "name": "Seed User 01",
    "email": "seed01@example.com",
    "role": "admin"
  }
  ```

- `404 Not Found`: User not found (`{"detail": "User not found"}`)

**Example:**

```bash
curl http://localhost:8000/api/v1/users/1
```

### Create User

**Endpoint:** `POST /api/v1/users`

**Body** (`UserCreate`):

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "editor"
}
```

- `201 Created`: Returns the created `UserResponse`.
- `409 Conflict`: Email already registered.

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/users ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"role\":\"editor\"}"
```

(On bash/macOS, use single quotes around the JSON in `-d`.)

### Update User

**Endpoint:** `PATCH /api/v1/users/{user_id}`

**Body** (`UserUpdate`): all fields optional; only send fields to change.

```json
{
  "role": "admin"
}
```

- `200 OK`: Returns updated `UserResponse`.
- `404 Not Found`: Unknown `user_id`.
- `409 Conflict`: `email` already used by another user.

**Example:**

```bash
curl -X PATCH http://localhost:8000/api/v1/users/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"role\":\"viewer\"}"
```

### Delete User

**Endpoint:** `DELETE /api/v1/users/{user_id}`

- `204 No Content`: Deleted successfully (empty body).
- `404 Not Found`: Unknown `user_id`.

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/v1/users/1
```

## 🧪 Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running in Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Code Structure Guidelines

- **Controllers**: Thin; delegate to services; declare `response_model` with Pydantic schemas where useful
- **Services**: Business logic and validation rules
- **Repositories**: SQLAlchemy only; no HTTP or Pydantic in repositories
- **ORM models** (`app/models/`): SQLAlchemy `Column` definitions
- **Schemas** (`app/schemas/`): Pydantic contracts (`UserCreate`, `UserUpdate`, `UserResponse`)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (optional; loaded by `pydantic-settings` in `app/core/config.py`):

```env
# MySQL (SQLAlchemy + PyMySQL)
DATABASE_URL=mysql+pymysql://appuser:apppass@127.0.0.1:3306/appdb
```

When using Docker Compose for MySQL only, point `DATABASE_URL` at `127.0.0.1` and the published port (default `3306`). If you run the app **inside** Compose on the same network as `db`, use host `db` and port `3306` in the URL.

Compose-related overrides (optional):

| Variable | Role |
|----------|------|
| `MYSQL_ROOT_PASSWORD` | MySQL root password (default `rootsecret`) |
| `MYSQL_DATABASE` | Database name (default `appdb`) |
| `MYSQL_USER` / `MYSQL_PASSWORD` | Application user (defaults `appuser` / `apppass`) |
| `MYSQL_PORT` | Host port mapped to MySQL (default `3306`) |
| `APP_PORT` | Used if you expose the app service in Compose (default `8000`) |

### Adding New Features

1. **Add a new endpoint:**
   - Add route handler in `app/api/v1/controller.py`
   - Create or use existing service method
   - Update repository if needed

2. **Add a new service:**
   - Add a service class under `app/services/`
   - Wire it in `app/core/dependencies.py` with `Depends` (chain `get_db` → repository → service as needed)

3. **Add a new repository:**
   - Accept `Session` in `__init__(self, db: Session)` and use `Depends(get_db)` via a `get_*_repository` function

## 📦 Dependencies

### Core Dependencies

- **fastapi** (0.128.0): Web framework
- **uvicorn** (0.40.0): ASGI server
- **pydantic** (2.12.5): Validation and settings
- **pydantic-settings** (2.7.0): `DATABASE_URL` from environment / `.env`
- **sqlalchemy** (2.0.36): ORM and Core
- **pymysql** (1.1.1): MySQL driver used in the SQLAlchemy URL (`mysql+pymysql://...`)
- **cryptography** (44.0.2): Required by PyMySQL for MySQL 8 default authentication (`caching_sha2_password`)

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Add a new package
pip install <package-name>
pip freeze > requirements.txt
```

## 🚀 Deployment

### Docker Compose (MySQL)

The repo includes **`docker-compose.yml`** with a **`db`** service (MySQL 8, health check, named volume `mysql_data`). Start the database:

```bash
docker compose up -d
```

The **`app`** service may be commented out so you can develop with `uvicorn` on the host while MySQL runs in Docker. To run the API in Compose as well, uncomment the `app` service, set `DATABASE_URL` for the in-network hostname `db`, rebuild, and run `docker compose up --build`.

### Docker Image (App Only)

The **`dockerfile`** in the project root builds the API image:

```bash
docker build -f dockerfile -t fastapi-template .
docker run -p 8000:8000 -e DATABASE_URL=mysql+pymysql://USER:PASS@HOST:3306/DBNAME fastapi-template
```

Pass a real `DATABASE_URL` for your MySQL instance (Compose service name, managed cloud host, etc.).

### Cloud Platforms

This application can be deployed to:
- **Heroku**: Use Procfile with `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **AWS**: Use AWS Elastic Beanstalk or ECS
- **Google Cloud**: Use Cloud Run or App Engine
- **Azure**: Use Azure App Service
- **DigitalOcean**: Use App Platform

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port
   uvicorn app.main:app --port 8001
   ```

2. **Module not found errors:**
   ```bash
   # Ensure virtual environment is activated
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Import errors:**
   - Ensure you're running from the project root directory
   - Check that all `__init__.py` files are present

4. **`RuntimeError: 'cryptography' package is required` (PyMySQL / seed / DB):**
   - Install dependencies from `requirements.txt` (includes `cryptography`).

5. **409 on create/update user:**
   - Choose a different `email`; addresses are unique in the database.

6. **Database connection errors / `Can't connect to MySQL`:**
   - Confirm MySQL is running (`docker compose ps` or your local service).
   - Check `DATABASE_URL` user, password, host, port, and database name.
   - Wait for the Compose `db` health check to pass before starting the app.

7. **Empty `GET /api/v1/users` or 404 on `GET /users/{id}` after deploy:**
   - Run `python -m scripts.seed_users` after the database is up and tables exist.

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Your Name - Your Email

---

**Happy Coding! 🎉**
