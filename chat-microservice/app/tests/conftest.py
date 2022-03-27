import pytest

from cassandra import AlreadyExists
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.cqlengine import columns, connection, management, models, query
from cassandra.cqlengine.connection import log as cql_logger

from app.models.chat_messages import ChatMessages

db_session = None
keyspace = 'python_test_environment'
table_name = 'chat_messages'

@pytest.fixture(scope="module")
def cassandra_session():
    global db_session
    
    cluster = Cluster(
        ['127.0.0.1'], 
        protocol_version=4, 
        load_balancing_policy=RoundRobinPolicy()
    )

    db_session = cluster.connect()

    try:
        db_session.execute(
            'CREATE KEYSPACE %s WITH replication = '
            "{'class': 'SimpleStrategy', 'replication_factor': '1'} "
            'AND durable_writes = true;' % keyspace)
    except AlreadyExists:
        pass

    db_session.set_keyspace(keyspace)
    connection.set_session(db_session)
    management.sync_table(ChatMessages)

@pytest.fixture()
def cassandra_db():
    global db_session

    yield

    db_session.execute(
        f'TRUNCATE {keyspace}.{table_name}'
    )
