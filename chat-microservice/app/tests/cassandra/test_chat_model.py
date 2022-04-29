import uuid

from app.models.chat import Chat

def test_create_a_single_record(cassandra_session):
    model_instance = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [str(uuid.uuid4()), str(uuid.uuid4())],
        users_name = ["Frank", "Pepe"]
    )
    assert Chat.objects().count() == 1

def test_chat_id_must_be_unique(cassandra_session):
    chat_id_unique = str(uuid.uuid4())
    for _ in range(3):
        Chat.create(
            chat_id = chat_id_unique,
            users_id = [str(uuid.uuid4()), str(uuid.uuid4())],
            users_name = ["Frank", "Pepe"]
        )
    assert Chat.objects().count() == 1

def test_find_all_franks_chat(cassandra_session):
    frank_id = str(uuid.uuid4())
    for _ in range(3):
        Chat.create(
            chat_id = str(uuid.uuid4()),
            users_id = [frank_id, str(uuid.uuid4())],
            users_name = ["Frank", "Pepe"]
        )
    for _ in range(3):
        Chat.create(
            chat_id = str(uuid.uuid4()),
            users_id = [str(uuid.uuid4()), str(uuid.uuid4())],
            users_name = ["Frank", "Pepe"]
        )
    assert Chat.objects().count() == 6
    franks_chat = Chat.objects().filter(users_id__contains=frank_id).allow_filtering()
    assert franks_chat.count() == 3
