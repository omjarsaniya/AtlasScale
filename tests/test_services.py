import pytest

from atlasscale.repositories import InMemoryJobRepository
from atlasscale.services import (
    JobAlreadyExistsError,
    JobNotFoundError,
    JobService,
)


@pytest.fixture
def job_service():
    repository = InMemoryJobRepository()
    return JobService(repository)


def test_create_job(job_service):
    job = job_service.create_job(
        job_id="job-101",
        task="generate_report",
        priority=5,
    )

    assert job.job_id == "job-101"
    assert job.task == "generate_report"
    assert job.priority == 5
    assert job.status == "pending"


def test_create_duplicate_job_raises_error(job_service):
    job_service.create_job("job-102", "process_file")

    with pytest.raises(JobAlreadyExistsError):
        job_service.create_job("job-102", "process_file")


def test_get_existing_job(job_service):
    created_job = job_service.create_job(
        "job-103",
        "generate_report",
        priority=3,
    )

    retrieved_job = job_service.get_job("job-103")

    assert retrieved_job is created_job


def test_get_nonexistent_job_raises_error(job_service):
    with pytest.raises(JobNotFoundError):
        job_service.get_job("job-999")


def test_create_job_with_invalid_priority(job_service):
    with pytest.raises(ValueError):
        job_service.create_job(
            job_id="job-104",
            task="process_file",
            priority=-1,
        )