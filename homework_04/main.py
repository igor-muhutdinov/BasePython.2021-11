"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
from models import create_tables, engine, User, Post
from jsonplaceholder_requests import get_users_data_from_url, get_posts_data_from_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


async def async_main():
    await create_tables()
    users, posts = await asyncio.gather(get_users_data_from_url(), get_posts_data_from_url())
    await add_users_to_db_from_json(users)
    await add_posts_to_db_from_json(posts)


async def add_users_to_db_from_json(users: dict):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            for single_user in users:
                user = User(name=single_user['name'],
                            username=single_user['username'],
                            email=single_user['email'])
                session.add(user)


async def add_posts_to_db_from_json(posts: dict):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        session: AsyncSession
        async with session.begin():
            for single_post in posts:
                post = Post(user_id=single_post['userId'],
                            title=single_post['title'],
                            body=single_post['body'])
                session.add(post)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
