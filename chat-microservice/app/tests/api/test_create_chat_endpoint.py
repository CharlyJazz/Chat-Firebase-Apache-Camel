import uuid

from app.models.chat_messages import ChatMessages
from app.models.chat import Chat

from fastapi.testclient import TestClient


def test_create_chat_created_201(
  client: TestClient,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  users_id = [main_from_user_uid, main_to_user_uid]
  res =  client.post(
    f"/api/v1/chat/",
    json={
      "users_id": users_id,
    }, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 201
  assert Chat.objects().count() == 1
  assert 'chat_id' in data 
  assert 'users_id' in data
  assert 'users_name' in data
  assert main_from_user_uid in data['users_id']
  assert main_to_user_uid in data['users_id']

def test_create_chat_current_user_not_in_users_id_401(
  client: TestClient,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  res =  client.post(
    f"/api/v1/chat/",
    json={
      "users_id": [400, 200],
    }, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 401
  assert data['detail'] == 'User is not authorized to do this action'
  assert Chat.objects().count() == 0

def test_create_chat_user_not_authorized_401(
  client: TestClient,
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  res =  client.post(
    f"/api/v1/chat/",
    json={
      "users_id": [400, 200],
    }
  )
  data = res.json()
  assert res.status_code == 401
  assert Chat.objects().count() == 0

def test_create_chat_already_exist_the_chat(
  client: TestClient,
  user_token_header,
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  users_id = [main_from_user_uid, main_to_user_uid]
  chat = Chat.create(
      chat_id = str(uuid.uuid4()),
      users_id = users_id,
      users_name = ["Frank", "Pepe"]
  )
  res =  client.post(
    f"/api/v1/chat/",
    json={
      "users_id": users_id
    },
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 422
  assert data['detail'] == 'There is a chat for this users'
