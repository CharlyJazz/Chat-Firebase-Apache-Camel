import uuid

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

def test_create_a_single_record(cassandra_session):
    model_instance = ChatMessages.create(
        from_user=str(uuid.uuid4()),
        to_user=str(uuid.uuid4()),
        chat_id=str(uuid.uuid4()),
        body='Test Body'
    )
    assert ChatMessages.objects().count() == 1

def test_pagination_and_relationship(cassandra_session):
    frank_id = str(uuid.uuid4())
    pepe_id = str(uuid.uuid4())
    
    chat_record = Chat.create(
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
            chat_id="Z", 
            body="Noise Message"
        )
    
    assert ChatMessages.objects().count() == len(conversation) * 2

    page_1 = ChatMessages.objects(
        chat_id=str(chat_record.chat_id)
    ).limit(3)

    assert len(page_1) == 3
    assert page_1[0]["body"] == conversation[10].body
    assert page_1[1]["body"] == conversation[9].body
    assert page_1[2]["body"] == conversation[8].body
    
    last_time = page_1[-1]["time"]

    page_2 = ChatMessages.objects(
        chat_id=str(chat_record.chat_id)
    ).filter(time__lt=last_time).limit(5)

    assert len(page_2) == 5
    assert page_2[0]["body"] == conversation[7].body
    assert page_2[1]["body"] == conversation[6].body
    assert page_2[2]["body"] == conversation[5].body
    assert page_2[3]["body"] == conversation[4].body
    assert page_2[4]["body"] == conversation[3].body

    last_time = page_2[-1]["time"]

    page_3 = ChatMessages.objects(
        chat_id=str(chat_record.chat_id)
    ).filter(time__lt=last_time).limit(5)

    assert len(page_3) == 3
    assert page_3[0]["body"] == conversation[2].body
    assert page_3[1]["body"] == conversation[1].body
    assert page_3[2]["body"] == conversation[0].body
