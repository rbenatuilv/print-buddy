from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .core.config import settings
from .api import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[settings.URL, "127.0.0.1", "localhost"]
)

app.include_router(router)
