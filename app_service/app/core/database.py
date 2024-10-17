import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get('POSTGRES_URL')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

async def get_session() ->  AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def initiate_database():
    pass

async def close_database():
    await engine.dispose()