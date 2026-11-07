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
        
        
def test_start_job_changes_status_to_running(job_service):
    job = job_service.create_job(
        job_id="job-start-001",
        task="generate_report",
    )

    started_job = job_service.start_job(job.job_id)

    assert started_job.status == "running"


def test_start_job_persists_status(job_service):
    job = job_service.create_job(
        job_id="job-start-002",
        task="process_file",
    )

    job_service.start_job(job.job_id)

    retrieved_job = job_service.get_job(job.job_id)

    assert retrieved_job.status == "running"


def test_start_nonexistent_job_raises_error(job_service):
    with pytest.raises(JobNotFoundError):
        job_service.start_job("nonexistent-job")


def test_start_already_running_job_raises_error(job_service):
    job = job_service.create_job(
        job_id="job-start-003",
        task="generate_report",
    )

    job_service.start_job(job.job_id)

    with pytest.raises(ValueError):
        job_service.start_job(job.job_id)
        
def test_complete_job_changes_status_to_completed(job_service):
    job = job_service.create_job(
        job_id="job-complete-001",
        task="generate_report",
    )

    job_service.start_job(job.job_id)

    completed_job = job_service.complete_job(job.job_id)

    assert completed_job.status == "completed"


def test_complete_job_persists_status(job_service):
    job = job_service.create_job(
        job_id="job-complete-002",
        task="process_file",
    )

    job_service.start_job(job.job_id)
    job_service.complete_job(job.job_id)

    retrieved_job = job_service.get_job(job.job_id)

    assert retrieved_job.status == "completed"


def test_complete_pending_job_raises_error(job_service):
    job = job_service.create_job(
        job_id="job-complete-003",
        task="generate_report",
    )

    with pytest.raises(ValueError):
        job_service.complete_job(job.job_id)
        
        
def test_fail_job_changes_status_to_failed(job_service):
    job = job_service.create_job(
        job_id="job-fail-001",
        task="process_file",
    )

    job_service.start_job(job.job_id)

    failed_job = job_service.fail_job(job.job_id)

    assert failed_job.status == "failed"


def test_fail_job_persists_status(job_service):
    job = job_service.create_job(
        job_id="job-fail-002",
        task="generate_report",
    )

    job_service.start_job(job.job_id)
    job_service.fail_job(job.job_id)

    retrieved_job = job_service.get_job(job.job_id)

    assert retrieved_job.status == "failed"


def test_fail_pending_job_raises_error(job_service):
    job = job_service.create_job(
        job_id="job-fail-003",
        task="process_file",
    )

    with pytest.raises(ValueError):
        job_service.fail_job(job.job_id)