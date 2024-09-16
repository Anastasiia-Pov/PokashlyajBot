from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy import BigInteger, String, ForeignKey
from typing import Annotated
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
engine = create_async_engine(url=f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column(String(1))
    region: Mapped[str] = mapped_column(String(25))


class User_lang(Base):
    __tablename__ = 'user_languange'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column()
    lang: Mapped[str] = mapped_column(String(2))


class Cough_sounds(Base):
    __tablename__ = 'coughs_recordings'

    id: Mapped[intpk]
    user_id: Mapped[int]
    sound: Mapped[str]


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
