import uuid

import pytest
from sqlalchemy import delete

from atlasscale.database.connection import SessionLocal
from atlasscale.database.models import JobModel
from atlasscale.job import Job
from atlasscale.postgres_repository import PostgresJobRepository


@pytest.fixture
def db_session():
    session = SessionLocal()

    try:
        yield session

    finally:
        session.rollback()
        session.close()


@pytest.fixture
def repository(db_session):
    return PostgresJobRepository(db_session)


@pytest.fixture
def job_id():
    return f"test-{uuid.uuid4()}"


@pytest.fixture
def cleanup(job_id):
    yield

    with SessionLocal() as session:
        session.execute(
            delete(JobModel).where(JobModel.job_id == job_id)
        )
        session.commit()


def test_save_and_retrieve_job(repository, job_id, cleanup):
    job = Job(
        job_id=job_id,
        task="generate_report",
        priority=3,
    )

    repository.save(job)

    retrieved_job = repository.get_by_id(job_id)

    assert retrieved_job is not None
    assert retrieved_job.job_id == job_id
    assert retrieved_job.task == "generate_report"
    assert retrieved_job.priority == 3
    assert retrieved_job.status == "pending"


def test_job_exists(repository, job_id, cleanup):
    job = Job(job_id, "process_file")

    repository.save(job)

    assert repository.exists(job_id) is True


def test_nonexistent_job_does_not_exist(repository, job_id):
    assert repository.exists(job_id) is False


def test_get_nonexistent_job_returns_none(repository, job_id):
    assert repository.get_by_id(job_id) is None


def test_save_updates_existing_job(repository, job_id, cleanup):
    job = Job(job_id, "process_file", priority=1)

    repository.save(job)

    job.priority = 5
    repository.save(job)

    retrieved_job = repository.get_by_id(job_id)

    assert retrieved_job.priority == 5


def test_repository_preserves_job_status(repository, job_id, cleanup):
    job = Job(job_id, "generate_report")

    job.start()
    job.complete()

    repository.save(job)

    retrieved_job = repository.get_by_id(job_id)

    assert retrieved_job.status == "completed"