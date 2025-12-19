from collections.abc import AsyncGenerator
from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
import datetime


# Using SQLite for simplicity; replace with your DB URL
DATABASE_URL = "sqlite+aiosqlite:///./test.db" # Example using SQLite for simplicity


class Post(DeclarativeBase):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text, nullable=False)
    url = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
# Set up the async engine and session maker
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Create the database tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)
    
# Dependency to get DB session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session 