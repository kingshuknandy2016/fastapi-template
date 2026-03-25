# Step-by-step FastAPI setup (Layered Architecture)

### 🔹 STEP 1: Create Project Folder

```bash
mkdir fastapi_app
cd fastapi_app
```

### 🔹 STEP 2: Create & Activate Virtual Environment

Create the virtual environment:

```bash
python -m venv venv
```

**Activate it:**

**Linux / macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt when the virtual environment is active.

### 🔹 STEP 3: Install Dependencies

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

Create `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### 🔹 STEP 4: Create Folder Structure

Create the directory structure:

```bash
mkdir -p app/api/v1
mkdir -p app/services
mkdir -p app/repositories
mkdir -p app/core
mkdir -p app/models
```

Create empty `__init__.py` files:

**Linux / macOS:**
```bash
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/services/__init__.py
touch app/repositories/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
```

**Windows (PowerShell):**
```powershell
New-Item app/__init__.py -ItemType File
New-Item app/api/__init__.py -ItemType File
New-Item app/api/v1/__init__.py -ItemType File
New-Item app/services/__init__.py -ItemType File
New-Item app/repositories/__init__.py -ItemType File
New-Item app/core/__init__.py -ItemType File
New-Item app/models/__init__.py -ItemType File
```

Your structure should now look like:

```
fastapi_app/
├── app/
│   ├── api/v1/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   ├── models/
│   └── main.py
└── requirements.txt
```

### 🔹 STEP 5: Create Repository Layer

Create `app/repositories/user_repository.py`:

```python
class UserRepository:
    def __init__(self):
        # Simulating DB or external API
        self._users = {
            1: {"id": 1, "name": "Alice"},
            2: {"id": 2, "name": "Bob"},
        }

    def get_user_by_id(self, user_id: int):
        return self._users.get(user_id)
```

**👉 Purpose:**
- Talks to DB / external systems
- NO business logic

### 🔹 STEP 6: Create Service Layer

Create `app/services/user_service.py`:

```python
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
```

**👉 Purpose:**
- Contains business rules
- Uses repositories
- No HTTP / FastAPI imports

### 🔹 STEP 7: Create Dependency Container (Service Initialization)

Create `app/core/dependencies.py`:

```python
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class ServiceContainer:
    user_service: UserService | None = None


container = ServiceContainer()


def init_services():
    user_repo = UserRepository()
    container.user_service = UserService(user_repo)
```

**👉 Why this exists:**
- Services are created once
- Avoids re-creating objects per request
- Easy to test / extend

### 🔹 STEP 8: Create Controller Layer (API)

Create `app/api/v1/controller.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import container

router = APIRouter()


def get_user_service():
    if not container.user_service:
        raise RuntimeError("Service not initialized")
    return container.user_service


@router.get("/users/{user_id}")
def get_user(user_id: int, user_service=Depends(get_user_service)):
    try:
        return user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

**👉 Controller rules:**
- Handles HTTP stuff only
- Calls service
- Converts errors → HTTP responses

### 🔹 STEP 9: Create FastAPI Application & Startup Hook

Create `app/main.py`:

```python
from fastapi import FastAPI
from app.api.v1.controller import router
from app.core.dependencies import init_services

app = FastAPI(title="Layered FastAPI App")


@app.on_event("startup")
def startup_event():
    init_services()


app.include_router(router, prefix="/api/v1")
```

**👉 This is the critical requirement:**
✔️ Service layer is initialized at app startup / mounting time

### 🔹 STEP 10: Run the Application

From project root:

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

### 🔹 STEP 11: Test the API

Open browser or Postman:

```
GET http://127.0.0.1:8000/api/v1/users/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Alice"
}
```

**Try:**
```
GET /users/999
```

**You'll get:**
```json
{
  "detail": "User not found"
}
```

**Access Interactive Documentation:**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

[← Back to README](../Readme.md)
