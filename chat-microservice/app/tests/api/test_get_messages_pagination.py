import pytest
import uuid

from fastapi.testclient import TestClient

from app.models.chat_messages import ChatMessages
from app.models.chat import Chat

from dataclasses import dataclass

@dataclass
class ChatMessage:
    """Class for keeping track of an item in inventory."""
    from_user: str
    to_user: str
    chat_id: str
    body: str


def test_pagination_get_messages(
    cassandra_session,
    client: TestClient, 
    user_token_header
):
    frank_id = str(uuid.uuid4())
    pepe_id = str(uuid.uuid4())
    
    chat_record = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [str(uuid.uuid4()), str(uuid.uuid4())],
        users_name = ["Frank", "Pepe"]
    )

    # Create a conversation between Frank and Pepe

    conversation = [
        ChatMessage(frank_id, pepe_id, chat_record.chat_id, 'Hello Pepe!'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'Hello Frank!'),
        ChatMessage(frank_id, pepe_id, chat_record.chat_id, 'How are you Pepe?'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'Fine'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'What about you Frank?'),
        ChatMessage(frank_id, pepe_id, chat_record.chat_id, 'Pepe my mom died I am very sad'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'Damn it, What a pitty'),
        ChatMessage(frank_id, pepe_id, chat_record.chat_id, 'Yes bro, very sad'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'By the way Frank, I need your help'),
        ChatMessage(frank_id, pepe_id, chat_record.chat_id, 'For what?'),
        ChatMessage(pepe_id, frank_id, chat_record.chat_id, 'To be happy Frank, I miss you (Romantic music turn on)'),
    ]

    for m in conversation:
        ChatMessages.create(
            from_user=m.from_user, 
            to_user=m.to_user, 
            chat_id=str(m.chat_id), 
            body=m.body
        )
        ChatMessages.create(
            from_user="X", 
            to_user="Y", 
            chat_id=str(uuid.uuid4()), 
            body="Noise Message"
        )
    
    assert ChatMessages.objects().count() == len(conversation) * 2
    
    res = client.get(
      f"/api/v1/chat/{chat_record.chat_id}/messages/",
      params={
        "chat_id": str(chat_record.chat_id),
        "quantity": 3
      },
      headers=user_token_header
    )
    assert res.status_code == 200

    data = res.json()
    
    assert len(data) == 3

    assert data[0]["body"] == conversation[10].body
    assert data[1]["body"] == conversation[9].body
    assert data[2]["body"] == conversation[8].body
    
    last_time = data[-1]["time"] # By the way Frank, I need your help

    res = client.get(
      f"/api/v1/chat/{chat_record.chat_id}/messages/",
      params={
        "chat_id": str(chat_record.chat_id),
        "time": last_time,
        "quantity": 5
      },
      headers=user_token_header
    )
    assert res.status_code == 200
    
    data = res.json()

    assert len(data) == 5

    assert data[0]["body"] == conversation[7].body
    assert data[1]["body"] == conversation[6].body
    assert data[2]["body"] == conversation[5].body
    assert data[3]["body"] == conversation[4].body
    assert data[4]["body"] == conversation[3].body

    last_time = data[-1]["time"]

    res = client.get(
      f"/api/v1/chat/{chat_record.chat_id}/messages/",
      params={
        "chat_id": str(chat_record.chat_id),
        "time": last_time,
        "quantity": 5
      },
      headers=user_token_header
    )
    assert res.status_code == 200

    data = res.json()

    assert len(data) == 3
    assert data[0]["body"] == conversation[2].body
    assert data[1]["body"] == conversation[1].body
    assert data[2]["body"] == conversation[0].body
