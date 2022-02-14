"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or \
              "postgresql+asyncpg://postgres:password@localhost/postgres"

engine = create_async_engine(PG_CONN_URI, echo=True)
Base = declarative_base(engine)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default="", server_default="")
    username = Column(String, nullable=False, default="", server_default="")
    email = Column(String, nullable=False, default="", server_default="")

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    title = Column(String, nullable=False, default="", server_default="")
    body = Column(String, nullable=False, default="", server_default="")

    user = relationship("User", back_populates="posts")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(create_tables())
