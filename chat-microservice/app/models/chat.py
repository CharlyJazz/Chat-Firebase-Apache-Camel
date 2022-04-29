from uuid import uuid1,uuid4

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
    """
    __table_name__ = 'chat'
    chat_id = columns.UUID(primary_key=True, partition_key=True, default=uuid4)
    users_id = columns.Set(value_type=columns.Text)
    users_name = columns.Set(value_type=columns.Text)

    def __repr__(self):
        return f'{self.chat_id} {self.users_id} {self.users_name}'
