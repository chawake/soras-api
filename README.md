# Sora API

## Getting Started

Install uv
```bash
pip install uv
```

Or via script
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies
```bash
uv sync --frozen
```

Create the virtual environment
```bash
cp example.env .env
# Edit .env with the required settings
```

Run
```bash
docker compose up -d --build
```
Run the dev profile (database and app ports exposed)
```bash
docker compose --profile dev up -d --build
```

Or locally
```bash
uvx uvicorn backend.src.main:app --reload
```

## Code Documentation

Main structure
```
backend
├── alembic                 Alembic files (DB migrations)
├── alembic.ini
└── src                     Modules
    ├── core                Internal settings / common utilities
    │   ├── config.py
    │   ├── admin.py
    │   └── logging_setup.py
    ├── db                  ORM settings and DB connections
    ├── integration         Integration module for external services
    ├── main.py             Entry point
    └── task                Task module: queueing, execution, etc.
```

Module structure
```
task
├── api                         External data layer

│   ├── dependencies.py         Module dependencies
│   ├── admin.py                sqladmin ModelView configuration
│   └── rest.py                 FastAPI endpoints

├── application                 Business logic layer
│   ├── interfaces
│   │   ├── task_repository.py  DB task model operations
│   │   ├── task_runner.py      Interface for running tasks and retrieving results
│   │   └── task_uow.py         Unit of Work, simplifies session management
│   └── use_cases
│       ├── create_task.py      Persist task in DB
│       ├── get_task.py         Fetch task from DB
│       └── run_task.py         Run task (via integration)

├── domain                      Data layer
│   ├── dtos.py
│   ├── entities.py             Domain models of the module
│   └── mappers.py              Convert models between representations

└── infrastructure              Data access layer, interface implementations
    └── db                      Database access
        ├── orm.py              ORM models (SQLAlchemy)
        ├── task_repository.py
        └── unit_of_work.py
```

Task workflow
1) src.task.api.rest - FastAPI POST /api/task
2) src.task.application.use_cases.create_task - Persist in DB
3) src.task.application.use_cases.run_task - Runs in the background, executes task and waits for the result
4) src.integration.infrastructure.task_runner - Integration handling (HTTP: send request, receive response)
5) src.task.application.use_cases.run_task - Persist the result (content or error) in DB
6) src.task.api.rest - FastAPI GET /api/task/{task_id}
7) src.task.application.use_cases.get_task - Fetch task from DB

The architecture makes it easy to extend the business logic, refactor individual parts, and build tests. Stick to it for simpler API maintenance.
