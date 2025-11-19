from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqladmin import Admin

from src.db.engine import engine
from src.core.admin import authentication_backend
from src.core.logging_setup import setup_fastapi_logging
from src.integration import setup_integration
from src.task.api.rest import router as task_router
from src.task.api.admin import TaskAdmin

app = FastAPI(title="Sora API")
setup_fastapi_logging(app)
setup_integration(app)

@app.get("/")
async def root():
    return JSONResponse({
        "status": "running",
        "message": "Sora API is running",
        "docs": "/docs",
        "admin": "/admin",
        "api": "/api/task"
    })

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(task_router, tags=["Task"], prefix="/api/task")

# Admin interface
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(TaskAdmin)