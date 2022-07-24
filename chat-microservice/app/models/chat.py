from uuid import uuid4

from cassandra.cqlengine import columns, connection, management, models, query

# https://stackoverflow.com/a/24291261
class Chat(models.Model):
    """Chat Model
    To start a conversation we must create a Chat record.
    With a unique chat_id.
    All users id inside users_id.
    All users name inside users_id.
    Queries that this model meet:
    Q1 - Find all chats where a user is
    Q2 - Check if two users belongs to the same chat
    """
    __table_name__ = 'chat'
    chat_id = columns.UUID(primary_key=True, partition_key=True, default=uuid4)
    users_id = columns.Set(value_type=columns.Text)
    users_name = columns.Set(value_type=columns.Text)

    def __repr__(self):
        return f'{self.chat_id} {self.users_id} {self.users_name}'

    """
    Query to find if there are chats with the from_user_id on it
    And then loop the chats to find the to_user_id
    Return a boolean value
    """
    @staticmethod
    def users_id_belongs_to_chat(chat_id: str, from_user_id: str, to_user_id: str) -> bool:
        kwargs = {
            "users_id__contains": f"{from_user_id}"
        }
        if chat_id is not None:
            kwargs["chat_id"] = chat_id
        chats = Chat.objects().filter(**kwargs).allow_filtering().all()
        for chat in chats:
            if to_user_id in list(chat.users_id):
                return True
        return False

