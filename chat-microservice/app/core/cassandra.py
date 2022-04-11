from cassandra import AlreadyExists
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.cqlengine import connection, management
from cassandra.query import dict_factory

from app.models.chat_messages import ChatMessages
from app.core.config import settings

cassandra_cluster_global = None

def cassandra_connect():
    global cassandra_cluster_global
    cluster = Cluster(
        [settings.CASSANDRA_CLUSTER_ADDRESS], 
        protocol_version=settings.CASSANDRA_PROTOCOL_VERSION, 
        load_balancing_policy=RoundRobinPolicy()
    )

    db_session = cluster.connect()
    # Configures the default connection with a preexisting cassandra.cluster.Session
    # Note: the mapper presently requires a Session row_factory set to dict_factory.
    # This may be relaxed in the future
    db_session.row_factory = dict_factory

    try:
        db_session.execute(
            'CREATE KEYSPACE %s WITH replication = '
            "{'class': 'SimpleStrategy', 'replication_factor': '1'} "
            'AND durable_writes = true;' % settings.CASSANDRA_KEYSPACE)
    except AlreadyExists:
        pass

    db_session.set_keyspace(settings.CASSANDRA_KEYSPACE)
    connection.set_session(db_session)
    management.sync_table(ChatMessages)

    cassandra_cluster_global = cluster

def cassandra_shutdown():
  global cassandra_cluster_global
  cassandra_cluster_global.shutdown()
