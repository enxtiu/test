import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.model import Base

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

engine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)
session_marker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def created_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin as conn:
        await conn.run_sync(Base.metadata.drop_all)