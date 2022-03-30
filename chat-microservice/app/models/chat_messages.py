from uuid import uuid1,uuid4

from cassandra.cqlengine import columns, connection, management, models, query

# https://stackoverflow.com/a/24291261
class ChatMessages(models.Model):
    """Chat Messages Object Mapper Model"""
    __table_name__ = 'chat_messages'
    message_id = columns.UUID(default=uuid4)
    from_user = columns.Text(primary_key=True, partition_key=True)
    to_user = columns.Text(primary_key=True, partition_key=True)
    body = columns.Text()
    time = columns.TimeUUID(primary_key=True, default=uuid1, clustering_order='DESC')

    def __repr__(self):
        return f'{self.message_id} {self.from_user} {self.to_user} {self.body} {self.time}'
