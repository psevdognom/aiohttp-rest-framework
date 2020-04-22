import pytest
from aiohttp.test_utils import TestClient
from aiopg.sa.result import ResultProxy

from tests import models
from tests.aiopg.app import get_app
from tests.aiopg.utils import async_engine_connection


@pytest.fixture
async def user():
    async with async_engine_connection() as conn:
        query = models.users.select().limit(1)
        result: ResultProxy = await conn.execute(query)
        return await result.fetchone()


@pytest.fixture
async def get_last_created_user():
    async def _get_last_user():
        async with async_engine_connection() as conn:
            query = models.users.select().order_by(models.users.c.created_at.desc()).limit(1)
            result: ResultProxy = await conn.execute(query)
            return await result.fetchone()

    return _get_last_user


@pytest.fixture
async def get_user_by_id():
    async def _get_user_by_id(user_id):
        async with async_engine_connection() as conn:
            query = models.users.select(models.users.c.id == user_id)
            result: ResultProxy = await conn.execute(query)
            return await result.fetchone()

    return _get_user_by_id


@pytest.fixture
async def client(aiohttp_client):
    client: TestClient = await aiohttp_client(get_app())
    return client
