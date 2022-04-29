import pytest

from jose import jwt

from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from cassandra import AlreadyExists
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.cqlengine import connection, management
from cassandra.query import dict_factory

from app.api.deps import get_kafka_producer
from app.models.chat_messages import ChatMessages
from app.models.chat import Chat
from app.core import settings
from app.main import app
from app.tests.mocks.kafka_producer_mock import KafkaProducerMock

from datetime import datetime, timedelta


keyspace = settings.CASSANDRA_KEYSPACE_TESTING

@pytest.fixture()
def cassandra_session():
    cluster = Cluster(
        ['127.0.0.1'], 
        protocol_version=4, 
        load_balancing_policy=RoundRobinPolicy(),
        
    )

    db_session = cluster.connect()

    try:
        db_session.execute(
            'CREATE KEYSPACE %s WITH replication = '
            "{'class': 'SimpleStrategy', 'replication_factor': '1'} "
            'AND durable_writes = true;' % keyspace)
    except AlreadyExists:
        pass
        
    
    db_session.row_factory = dict_factory
    db_session.set_keyspace(keyspace)
    connection.set_session(db_session)

    management.sync_table(ChatMessages)
    management.sync_table(Chat)
    
    db_session.execute(f'TRUNCATE {keyspace}.{Chat.__table_name__}')
    db_session.execute(f'TRUNCATE {keyspace}.{ChatMessages.__table_name__}')

    yield

    db_session.execute(f'TRUNCATE {keyspace}.{Chat.__table_name__}')
    db_session.execute(f'TRUNCATE {keyspace}.{ChatMessages.__table_name__}')

    db_session.shutdown()

@pytest.fixture(autouse=True)
async def override_dependency():
    app.dependency_overrides[get_kafka_producer] = KafkaProducerMock

@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac, LifespanManager(app):
        yield ac

@pytest.fixture()
def current_user_id():
    return "1"

@pytest.fixture()
def user_token_header(current_user_id: str) -> dict[str, str]:
    access_token = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=30), 
            "user_id": current_user_id
        },
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture()
def unauthorized_user_token_header(current_user_id: str) -> dict[str, str]:
    access_token = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=30), 
            "user_id": "2"
        },
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {access_token}"}
