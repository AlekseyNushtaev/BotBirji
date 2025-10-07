from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import atexit
import datetime


DB_URL = "sqlite+aiosqlite:///db/database.db"
engine = create_async_engine(DB_URL)  # Асинхронный движок SQLAlchemy
Session = async_sessionmaker(expire_on_commit=False, bind=engine)  # Фабрика сессий

atexit.register(engine.dispose)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Order(Base):
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    market: Mapped[str] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
    podcategory: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    min_price: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[str] = mapped_column(nullable=True)
    flag: Mapped[bool] = mapped_column(default=False)
    time_start: Mapped[datetime.datetime] = mapped_column(nullable=True)



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
