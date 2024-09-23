from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from .config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)