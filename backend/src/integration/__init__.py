from fastapi import FastAPI

from src.integration.infrastructure.sora.dependencies import get_sora_director


def setup_integration(app: FastAPI):
    # Deferred initialization - director will be created when first accessed
    pass
