import os

import pytest
from dotenv import load_dotenv


load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    raise RuntimeError("TEST_DATABASE_URL is not configured")

# Force all tests to use the isolated test database.
os.environ["DATABASE_URL"] = test_database_url


from atlasscale.database.connection import Base, engine
from atlasscale.database import models
from atlasscale.api import job_repository


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(autouse=True)
def clean_test_database():
    job_repository.clear()
    yield
    job_repository.clear()