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

def test_users_belongs_to_chat_method(cassandra_session):
    from_user_id, to_user_id = [str(uuid.uuid4()), str(uuid.uuid4())]
    first_chat = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [from_user_id, to_user_id],
        users_name = ["Frank", "Pepe"]
    )
    second_chat = Chat.create(
        chat_id = str(uuid.uuid4()),
        users_id = [from_user_id, str(uuid.uuid4())],
        users_name = ["Frank", "Manuel"]
    )
    assert first_chat.users_id_belongs_to_chat(
        first_chat.chat_id, 
        from_user_id, 
        to_user_id
    ) is True
    assert first_chat.users_id_belongs_to_chat(
        first_chat.chat_id, 
        from_user_id, 
        str(uuid.uuid4())
    ) is False
