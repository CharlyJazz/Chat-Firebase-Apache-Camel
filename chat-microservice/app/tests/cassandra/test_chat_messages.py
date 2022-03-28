import uuid

from app.models.chat_messages import ChatMessages
from cassandra.query import SimpleStatement

def test_create_a_single_record(cassandra_session, cassandra_db):
    model_instance = ChatMessages.create(
        from_user=str(uuid.uuid4()),
        to_user=str(uuid.uuid4()),
        body='Test Body'
    )
    assert ChatMessages.objects().count() == 1

def test_get_all_messages_between_two_users(cassandra_session, cassandra_db):
    from_user_id = str(uuid.uuid4())
    to_user_id = str(uuid.uuid4())
    quantity = 9

    for i in range(1, quantity + 1):
        model_instance = ChatMessages.create(
            from_user=from_user_id,
            to_user=to_user_id,
            body=f'Message Number {str(i)}'
        )

    all_messages_asc_order = ChatMessages.objects(
        from_user=from_user_id, to_user=to_user_id
    )

    assert all_messages_asc_order[0].body == 'Message Number 9'

    assert len(all_messages_asc_order) == quantity


def test_paginate_messages(cassandra_session, cassandra_db, cassandra_db_session):
    from_user_id = str(uuid.uuid4())
    to_user_id = str(uuid.uuid4())
    quantity = 100

    ChatMessages.create(
        from_user="OTHER",
        to_user='OTHER',
        body=f'Message Number OTHER'
    )

    for i in range(1, quantity + 1):
        model_instance = ChatMessages.create(
            from_user=from_user_id,
            to_user=to_user_id,
            body=f'Message Number {str(i)}'
        )

    ChatMessages.create(
        from_user="OTHER",
        to_user='OTHER',
        body=f'Message Number OTHER'
    )

    results = ChatMessages.objects(
        from_user=from_user_id, to_user=to_user_id
    ).limit(10)

    assert results[0]["body"] == 'Message Number 100'

    last_time = results[9]["time"]

    results = ChatMessages.objects(
        from_user=from_user_id, to_user=to_user_id
    ).filter(time__lt=last_time).limit(10)

    assert results[0]["body"] == 'Message Number 90'

    last_time = results[9]["time"]

    results = ChatMessages.objects(
        from_user=from_user_id, to_user=to_user_id
    ).filter(time__lt=last_time).limit(10)

    assert results[0]["body"] == 'Message Number 80'

    # SHEEESH

