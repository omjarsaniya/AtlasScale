import logging
from enum import Enum


logger = logging.getLogger(__name__)



class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    def __str__(self):
        return self.value


ALLOWED_TRANSITIONS = {
    JobStatus.PENDING: {JobStatus.RUNNING},
    JobStatus.RUNNING: {
        JobStatus.COMPLETED,
        JobStatus.FAILED,
    },
    JobStatus.COMPLETED: set(),
    JobStatus.FAILED: set(),
}


class Job:
    def __init__(self, job_id, task, priority=1):
        if not isinstance(job_id, str) or not job_id.strip():
            raise ValueError("Job ID must be a non-empty string")

        if not isinstance(task, str) or not task.strip():
            raise ValueError("Task must be a non-empty string")

        if type(priority) is not int or priority < 1:
            raise ValueError("Priority must be a positive integer")

        self.job_id = job_id
        self.task = task
        self.priority = priority
        self._status = JobStatus.PENDING

    @property
    def status(self):
        return self._status

    def _change_status(self, new_status):
        if not isinstance(new_status, JobStatus):
            raise ValueError(f"Invalid job status: {new_status}")

        allowed_statuses = ALLOWED_TRANSITIONS[self._status]

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Invalid job state transition: "
                f"{self._status} -> {new_status}"
            )

        old_status = self._status
        self._status = new_status

        logger.info(
            "Job %s status changed: %s -> %s",
            self.job_id,
            old_status,
            new_status,
        )

    def start(self):
        self._change_status(JobStatus.RUNNING)

    def complete(self):
        self._change_status(JobStatus.COMPLETED)

    def fail(self):
        self._change_status(JobStatus.FAILED)