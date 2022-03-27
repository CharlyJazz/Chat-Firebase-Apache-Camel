import uuid

from app.models.chat_messages import ChatMessages


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
    ).order_by("-time")

    assert all_messages_asc_order[0].body == 'Message Number 9'

    assert len(all_messages_asc_order) == quantity
