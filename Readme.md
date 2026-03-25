# FastAPI Template - Clean Layered Architecture

A production-ready FastAPI template featuring a clean, scalable layered architecture with dependency injection, service container pattern, and best practices for building maintainable REST APIs.

## Table of Contents

- [FastAPI Template - Clean Layered Architecture](#fastapi-template---clean-layered-architecture)
  - [Table of Contents](#table-of-contents)
  - [🚀 Key Features](#-key-features)
  - [📋 Prerequisites](#-prerequisites)
    - [Verify Installation](#verify-installation)
  - [⚡ Quick Start](#-quick-start)
  - [✅ STEP-BY-STEP FASTAPI SETUP (Layered Architecture)](#-step-by-step-fastapi-setup-layered-architecture)
  - [📁 Project Structure](#-project-structure)
  - [🏗️ Architecture Overview](#️-architecture-overview)
    - [🏗️ FINAL FLOW (Important to Understand)](#️-final-flow-important-to-understand)
    - [Layer Responsibilities](#layer-responsibilities)
  - [🔌 API Endpoints](#-api-endpoints)
    - [Get User by ID](#get-user-by-id)
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
    - [Docker (Recommended)](#docker-recommended)
    - [Cloud Platforms](#cloud-platforms)
  - [🐛 Troubleshooting](#-troubleshooting)
    - [Common Issues](#common-issues)
  - [📚 Additional Resources](#-additional-resources)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [👤 Author](#-author)

## 🚀 Key Features

- **🏗️ Clean Layered Architecture**: Separation of concerns with Controller, Service, and Repository layers
- **💉 Dependency Injection**: Centralized service initialization using a service container pattern
- **📦 Modular Design**: Easy to extend and maintain with clear module boundaries
- **🔌 API Versioning**: Built-in support for API versioning (v1, v2, etc.)
- **⚡ FastAPI Framework**: Built on FastAPI for high performance and automatic API documentation
- **📝 Auto-Generated Docs**: Interactive API documentation with Swagger UI and ReDoc
- **🧪 Test-Ready**: Architecture designed for easy unit and integration testing
- **🔄 Startup Initialization**: Services initialized once at application startup for optimal performance
- **📊 Pydantic Models**: Type-safe data validation using Pydantic v2
- **🌐 RESTful API**: Follows REST principles and best practices

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **pip** (Python package installer)
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

```bash
# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/api/v1/users/1` (sample endpoint)

## ✅ STEP-BY-STEP FASTAPI SETUP (Layered Architecture)

The full tutorial (scaffold, repository/service/controller layers, startup wiring, run, and test) lives in **[docs/step-by-step-setup.md](docs/step-by-step-setup.md)**.

## 📁 Project Structure

```
fastapi-template/
├── app/
│   ├── __init__.py                 # App package initialization
│   ├── main.py                     # FastAPI application entry point
│   │
│   ├── api/                        # API Layer (Controllers)
│   │   └── v1/                     # API Version 1
│   │       ├── __init__.py
│   │       └── controller.py       # Route handlers and endpoints
│   │
│   ├── services/                   # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   └── user_service.py         # Business logic for user operations
│   │
│   ├── repositories/               # Repository Layer (Data Access)
│   │   ├── __init__.py
│   │   └── user_repository.py     # Data access layer for users
│   │
│   ├── models/                     # Data Models
│   │   └── __init__.py             # Pydantic models and schemas
│   │
│   └── core/                       # Core Configuration
│       ├── __init__.py
│       └── dependencies.py         # Dependency injection and service container
│
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
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

**Services are:**
- Created once
- Stored in a container
- Injected via Depends

### Layer Responsibilities

1. **Controller Layer (`app/api/`)**
   - Handles HTTP requests and responses
   - Validates input parameters
   - Calls appropriate service methods
   - Returns HTTP responses

2. **Service Layer (`app/services/`)**
   - Contains business logic
   - Orchestrates operations
   - Validates business rules
   - Calls repository methods

3. **Repository Layer (`app/repositories/`)**
   - Handles data access
   - Abstracts database/external API calls
   - Returns domain objects

4. **Core (`app/core/`)**
   - Dependency injection container
   - Service initialization
   - Shared utilities and configuration

## 🔌 API Endpoints

### Get User by ID

**Endpoint:** `GET /api/v1/users/{user_id}`

**Description:** Retrieves a user by their ID.

**Parameters:**
- `user_id` (path parameter, integer): The ID of the user to retrieve

**Response:**
- `200 OK`: User found
  ```json
  {
    "id": 1,
    "name": "Alice"
  }
  ```
- `404 Not Found`: User not found
  ```json
  {
    "detail": "User not found"
  }
  ```

**Example Request:**
```bash
curl http://localhost:8000/api/v1/users/1
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

- **Controllers**: Keep controllers thin - they should only handle HTTP concerns
- **Services**: Put all business logic in services
- **Repositories**: Keep data access logic isolated in repositories
- **Models**: Define Pydantic models for request/response validation

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database Configuration (when added)
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Adding New Features

1. **Add a new endpoint:**
   - Add route handler in `app/api/v1/controller.py`
   - Create or use existing service method
   - Update repository if needed

2. **Add a new service:**
   - Create service class in `app/services/`
   - Register in `app/core/dependencies.py`
   - Use in controllers via dependency injection

3. **Add a new repository:**
   - Create repository class in `app/repositories/`
   - Inject into services via constructor

## 📦 Dependencies

### Core Dependencies

- **fastapi** (0.128.0): Modern web framework
- **uvicorn** (0.40.0): ASGI server
- **pydantic** (2.12.5): Data validation

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Add a new package
pip install <package-name>
pip freeze > requirements.txt
```

## 🚀 Deployment

### Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t fastapi-template .
docker run -p 8000:8000 fastapi-template
```

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

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
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
