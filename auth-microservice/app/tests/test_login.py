import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from app.core.config import settings
from app.tests.factories import UserFactory


@pytest.mark.asyncio()
async def test_login_400(client: AsyncSession):
    login_data = {
        "username": settings.FIRST_USER_USERNAME,
        "password": settings.FIRST_USER_PASSWORD.get_secret_value(),
    }
    res = await client.post("/api/v1/login/", data=login_data)
    assert res.status_code == 400

@pytest.mark.asyncio()
async def test_login_200(client: AsyncSession, session: AsyncConnection):
    session.add(UserFactory())
    await session.commit()
    login_data = {
        "username": settings.FIRST_USER_USERNAME,
        "password": settings.FIRST_USER_PASSWORD.get_secret_value(),
    }
    res = await client.post("/api/v1/login/", data=login_data)
    data = res.json()
    assert data['access_token']
    assert data['token_type'] == 'bearer'
    assert res.status_code == 200
