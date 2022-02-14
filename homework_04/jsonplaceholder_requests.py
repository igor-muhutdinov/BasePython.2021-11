"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def get_data_from_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_users_data_from_url():
    return await get_data_from_url(USERS_DATA_URL)


async def get_posts_data_from_url():
    return await get_data_from_url(POSTS_DATA_URL)
