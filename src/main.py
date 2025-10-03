from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .core.config import settings
from .core.scheduler import Scheduler
from .api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    sched = Scheduler()
    sched.start()
    
    yield

    sched.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[settings.URL, "127.0.0.1", "localhost"]
)

app.include_router(router)
