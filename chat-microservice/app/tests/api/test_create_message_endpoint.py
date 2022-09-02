import uuid

from app.models.chat_messages import ChatMessages
from app.models.chat import Chat

from fastapi.testclient import TestClient


def test_create_chat_message_201(
  client: TestClient, 
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  chat = Chat.create(
      chat_id = str(uuid.uuid4()),
      users_id = [main_from_user_uid, main_to_user_uid],
      users_name = ["Frank", "Pepe"]
  )  
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": main_to_user_uid,
    "body": f'Message Body',
    "chat_id": str(chat.chat_id)
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 201
  assert ChatMessages.objects().count() == 1

def test_create_chat_message_401(
  client: TestClient, 
  unauthorized_user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": main_to_user_uid,
    "body": f'Message Body',
    "chat_id": "123"
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=unauthorized_user_token_header
  )
  data = res.json()
  assert res.status_code == 401
  assert ChatMessages.objects().count() == 0

def test_create_chat_message_422_no_chat_id(
  client: TestClient,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  cassandra_session
):
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": 1,
    "body": ["Hello"]
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 422
  assert ChatMessages.objects().count() == 0

def test_no_allow_create_chat_message_if_chat_not_found(
  client,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  cassandra_session
):
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": '1',
    "body": f'Message Body',
    "chat_id": str(uuid.uuid4())
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 401
  assert ChatMessages.objects().count() == 0

def test_no_allow_create_chat_message_if_to_user_not_match(
  client: TestClient,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  wrong_to_user_id = "101"
  chat = Chat.create(
      chat_id = str(uuid.uuid4()),
      users_id = [main_from_user_uid, main_to_user_uid],
      users_name = ["Frank", "Pepe"]
  )  
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": wrong_to_user_id,
    "body": f'Message Body',
    "chat_id": str(chat.chat_id)
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 401
  assert ChatMessages.objects().count() == 0

def test_no_allow_create_chat_message_if_from_user_not_match(
  client: TestClient,
  user_token_header: dict[str, str], 
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  wrong_from_user_id = "101"
  chat = Chat.create(
      chat_id = str(uuid.uuid4()),
      users_id = [wrong_from_user_id, main_to_user_uid],
      users_name = ["Frank", "Pepe"]
  )  
  new_message = {
    "from_user": main_from_user_uid,
    "to_user": main_to_user_uid,
    "body": f'Message Body',
    "chat_id": str(chat.chat_id)
  }
  res =  client.post(
    f"/api/v1/messaging/",
    json=new_message, 
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 401
  assert ChatMessages.objects().count() == 0
