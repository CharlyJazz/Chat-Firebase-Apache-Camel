import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from app.models.chat_messages import ChatMessages


@pytest.mark.asyncio()
async def test_create_chat_message_201(
  client: AsyncSession, 
  user_token_header: Dict[str, str], 
  current_user_id: str,
  cassandra_session
):
    new_message = {
      "from_user": current_user_id,
      "to_user": '1',
      "body": f'Message Body'
    }
    res = await client.post(
      f"/api/v1/messaging/",
      json=new_message, 
      headers=user_token_header
    )
    data = res.json()
    assert res.status_code == 201
    assert ChatMessages.objects().count() == 1

@pytest.mark.asyncio()
async def test_create_chat_message_401(
  client: AsyncSession, 
  unauthorized_user_token_header: Dict[str, str], 
  current_user_id: str,
  cassandra_session
):
    new_message = {
      "from_user": current_user_id,
      "to_user": '1',
      "body": f'Message Body'
    }
    res = await client.post(
      f"/api/v1/messaging/",
      json=new_message, 
      headers=unauthorized_user_token_header
    )
    data = res.json()
    assert res.status_code == 401
    assert ChatMessages.objects().count() == 0

@pytest.mark.asyncio()
async def test_create_chat_message_422(
  client: AsyncSession, 
  user_token_header: Dict[str, str], 
  current_user_id: str,
  cassandra_session
):
    new_message = {
      "from_user": current_user_id,
      "to_user": 1,
      "body": ["Hello"]
    }
    res = await client.post(
      f"/api/v1/messaging/",
      json=new_message, 
      headers=user_token_header
    )
    data = res.json()
    assert res.status_code == 422
    assert ChatMessages.objects().count() == 0
