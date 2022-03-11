import pytest

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from typing import Dict

from app.tests.factories import UserFactory

@pytest.mark.asyncio()
async def test_get_users_200(client: AsyncSession, session: AsyncConnection, user_token_headers: Dict[str, str]):
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
async def test_get_user_by_id_200(client: AsyncSession, session: AsyncConnection, user_token_headers: Dict[str, str]):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()
    res = await client.get(f"/api/v1/users/{user.id}", headers=user_token_headers)
    data = res.json()
    assert res.status_code == 200
    assert data["username"] == user.username
    assert data["id"] == 2

@pytest.mark.asyncio()
async def test_get_user_by_id_404(client: AsyncSession, session: AsyncConnection, user_token_headers: Dict[str, str]):
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
