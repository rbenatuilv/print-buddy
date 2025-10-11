from sqlmodel import SQLModel, create_engine, Session
from ..core.config import settings


engine = create_engine(
    settings.DB_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
