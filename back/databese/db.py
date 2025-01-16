# imports from pip
from datetime import datetime

from sqlalchemy import Date, DateTime, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


# declare connection to DB
engine = create_async_engine("sqlite+aiosqlite:///database.db")

# create session for work with DB
new_session = async_sessionmaker(engine, expire_on_commit=False)

# declare table construction
Base = declarative_base()
class FoodHistory(Base):
    __tablename__ = "Food_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]
    Kcal: Mapped[float]
    Quantity: Mapped[str]
    UserId: Mapped[int]

# declare table construction
class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]
    Username: Mapped[str]
    Password: Mapped[str]
    RegDate: Mapped[Date] = mapped_column(Date, nullable=True)
    Token: Mapped[str] = mapped_column(String, nullable=True)
    SessionEnd: Mapped[datetime] = mapped_column(DateTime, nullable=True)


# func to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# func to drop tables
async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)