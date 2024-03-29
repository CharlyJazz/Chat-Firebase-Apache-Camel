import uuid

from app.models.chat_messages import ChatMessages
from app.models.chat import Chat

from fastapi.testclient import TestClient


def test_get_user_chats(
  client: TestClient,
  user_token_header: dict[str, str],
  main_from_user_uid: str,
  main_to_user_uid: str,
  cassandra_session
):
  total_chats = 10
  for i in range(total_chats):
    chat = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [main_from_user_uid, str(i + 1)],
        users_name = ["Frank", "Pepe"]
    )  
  res =  client.get(
    f"/api/v1/chat/",
    headers=user_token_header
  )
  data = res.json()
  assert res.status_code == 200
  assert len(data) == 10

