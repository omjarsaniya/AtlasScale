import logging

import pytest

from atlasscale.job import Job, JobStatus


def test_new_job_starts_as_pending():
    job = Job("job-001", "generate_report")

    assert job.status == JobStatus.PENDING


def test_job_can_start():
    job = Job("job-002", "process_file")

    job.start()

    assert job.status == "running"


def test_job_can_complete():
    job = Job("job-003", "generate_report")

    job.start()
    job.complete()

    assert job.status == "completed"


def test_job_can_fail():
    job = Job("job-004", "process_data")

    job.start()
    job.fail()

    assert job.status == "failed"


def test_invalid_transition_raises_error():
    job = Job("job-005", "generate_report")

    with pytest.raises(ValueError):
        job.complete()


def test_completed_job_cannot_start_again():
    job = Job("job-006", "process_file")

    job.start()
    job.complete()

    with pytest.raises(ValueError):
        job.start()


def test_empty_job_id_is_rejected():
    with pytest.raises(ValueError):
        Job("", "generate_report")


def test_empty_task_is_rejected():
    with pytest.raises(ValueError):
        Job("job-007", "")


def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError):
        Job("job-008", "process_file", priority=-1)
        
        
def test_jobs_have_independent_statuses():
    job1 = Job("job-101", "generate_report")
    job2 = Job("job-102", "process_pdf")

    job1.start()

    assert job1.status == "running"
    assert job2.status == "pending"
    

def test_new_job_uses_pending_enum():
    job = Job("job-201", "generate_report")

    assert job.status is JobStatus.PENDING
    

def test_invalid_status_type_is_rejected():
    job = Job("job-202", "generate_report")

    with pytest.raises(ValueError, match="Invalid job status"):
        job._change_status("running")
        
        
def test_failed_job_cannot_restart():
    job = Job("job-301", "generate_report")

    job.start()
    job.fail()

    with pytest.raises(ValueError):
        job.start()

    assert job.status == "failed"
    
    
def test_starting_job_creates_log_message(caplog):
    job = Job("job-401", "generate_report")

    with caplog.at_level(logging.INFO, logger="atlasscale.job"):
        job.start()

    assert "Job job-401 status changed: pending -> running" in caplog.text
    
    
def test_job_status_cannot_be_assigned_directly():
    job = Job("job-501", "generate_report")

    with pytest.raises(AttributeError):
        job.status = JobStatus.RUNNING

    assert job.status == JobStatus.PENDING
    
    
def test_non_string_job_id_is_rejected():
    with pytest.raises(ValueError, match="Job ID must be a non-empty string"):
        Job(["job-601"], "generate_report")


def test_whitespace_job_id_is_rejected():
    with pytest.raises(ValueError, match="Job ID must be a non-empty string"):
        Job("   ", "generate_report")


def test_non_string_task_is_rejected():
    with pytest.raises(ValueError, match="Task must be a non-empty string"):
        Job("job-602", 123)


def test_whitespace_task_is_rejected():
    with pytest.raises(ValueError, match="Task must be a non-empty string"):
        Job("job-603", "   ")