from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.logging_setup import setup_fastapi_logging
from src.integration import setup_integration
from src.task.api.rest import router as task_router

app = FastAPI(title="Sora API")
setup_fastapi_logging(app)
setup_integration(app)

@app.get("/")
async def root():
    return JSONResponse({
        "status": "running",
        "message": "Sora API is running",
        "docs": "/docs",
        "api": "/api/task"
    })

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(task_router, tags=["Task"], prefix="/api/task")
