import pytest

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from app.tests.factories import UserFactory
from app.core.config import settings

@pytest.mark.asyncio()
async def test_get_users_200(client: AsyncSession, session: AsyncConnection, user_token_headers: dict[str, str]):
    session.add(UserFactory(username="charly", hashed_password="124567"))
    session.add(UserFactory(username="jazz", hashed_password="124567"))
    await session.commit()
    res = await client.get("/api/v1/users/", headers=user_token_headers)
    data = res.json()
    assert res.status_code == 200
    assert len(data) == 3
    assert 'password_hashed' not in data[0]
    assert 'username' in data[0]
    assert 'id' in data[0]

@pytest.mark.asyncio()
async def test_get_users_401(client: AsyncSession, session: AsyncConnection):
    session.add(UserFactory(username="charly", hashed_password="124567"))
    session.add(UserFactory(username="jazz", hashed_password="124567"))
    await session.commit()
    res = await client.get("/api/v1/users/")
    data = res.json()
    assert res.status_code == 401
    assert len(data) == 1
    assert data["detail"] == settings.OAUTH2_NOT_AUTHENTICATED

@pytest.mark.asyncio()
async def test_get_users_403(client: AsyncSession, session: AsyncConnection):
    session.add(UserFactory(username="charly", hashed_password="124567"))
    session.add(UserFactory(username="jazz", hashed_password="124567"))
    await session.commit()
    res = await client.get("/api/v1/users/", headers={"Authorization": "Bearer FastAPI is awesome"})
    data = res.json()
    assert res.status_code == 403
    assert len(data) == 1
    assert data["detail"] == settings.GET_TOKEN_DATA_403

@pytest.mark.asyncio()
async def test_get_user_by_id_200(client: AsyncSession, session: AsyncConnection, user_token_headers: dict[str, str]):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()
    res = await client.get(f"/api/v1/users/{user.id}", headers=user_token_headers)
    data = res.json()
    assert res.status_code == 200
    assert data["username"] == user.username
    assert data["id"] == 2

@pytest.mark.asyncio()
async def test_get_user_by_id_401(client: AsyncSession, session: AsyncConnection):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()
    res = await client.get(f"/api/v1/users/{user.id}")
    data = res.json()
    assert res.status_code == 401
    assert len(data) == 1
    assert data["detail"] == settings.OAUTH2_NOT_AUTHENTICATED

@pytest.mark.asyncio()
async def test_get_user_by_id_403(client: AsyncSession, session: AsyncConnection):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()
    res = await client.get(f"/api/v1/users/{user.id}", headers={"Authorization": "Bearer FastAPI is awesome"})
    data = res.json()
    assert res.status_code == 403
    assert len(data) == 1
    assert data["detail"] == settings.GET_TOKEN_DATA_403


@pytest.mark.asyncio()
async def test_get_user_by_id_404(client: AsyncSession, session: AsyncConnection, user_token_headers: dict[str, str]):
    res = await client.get(f"/api/v1/users/2", headers=user_token_headers)
    data = res.json()
    assert res.status_code == 404

@pytest.mark.asyncio()
async def test_post_create_user(client: AsyncSession, session: AsyncConnection):
    user_data = {
        "username": 'charlyfunk',
        "password": 'charlyfunk',
    }
    res = await client.post(f"/api/v1/users/", json=user_data)
    data = res.json()
    assert res.status_code == 200 # It should be 201...
