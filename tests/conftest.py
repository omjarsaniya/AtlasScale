import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import delete

load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    raise RuntimeError("TEST_DATABASE_URL is not configured")

os.environ["DATABASE_URL"] = test_database_url

from atlasscale.database.connection import Base, engine, SessionLocal
from atlasscale.database.models import JobModel
from atlasscale.database import models


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)

    yield


@pytest.fixture(autouse=True)
def clean_test_database():

    with SessionLocal() as session:
        session.execute(delete(JobModel))
        session.commit()

    yield

    with SessionLocal() as session:
        session.execute(delete(JobModel))
        session.commit()