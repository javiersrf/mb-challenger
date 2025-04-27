import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src import app
from src.core.database import get_db
from sqlmodel import SQLModel
from tests.factory.mms import MMsModelFactory


@pytest.fixture
def mock_request(allow_net_connect=False, verbose=False):
    import httpretty

    httpretty.reset()
    httpretty.enable(allow_net_connect=allow_net_connect, verbose=verbose)

    yield httpretty

    httpretty.disable()
    httpretty.reset()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:latest") as container:
        yield container


@pytest.fixture(scope="session")
def engine(postgres_container):
    connection_url = postgres_container.get_connection_url()
    engine = create_engine(connection_url, echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def set_session(db_session):
    for my_factory in [MMsModelFactory]:
        my_factory._meta.sqlalchemy_session = db_session
