from uuid import uuid1,uuid4

from cassandra.cqlengine import columns, connection, management, models, query

# https://stackoverflow.com/a/24291261
class ChatMessages(models.Model):
    """
    ChatMessages saves the messages that belong to a Chat.
    With a unique message_id.
    The chat_id belong to a Chat record.
    Queries that this model meet:
    Q1 - Get the last N message by a chat_id
    """
    __table_name__ = 'chat_messages'
    chat_id    = columns.UUID(primary_key=True, partition_key=True, required=True)
    from_user  = columns.Text(required=True)
    to_user    = columns.Text(required=True)
    message_id = columns.UUID(required=True, default=uuid4)
    body       = columns.Text(required=True)
    time       = columns.TimeUUID(primary_key=True, default=uuid1, clustering_order='DESC')

    def __repr__(self):
        return f'{self.chat_id} {self.message_id} {self.from_user} {self.to_user} {self.body} {self.time}'
