from atlasscale.job import Job
from atlasscale.interfaces import JobRepository


class JobAlreadyExistsError(Exception):
    """Raised when a job ID already exists."""


class JobNotFoundError(Exception):
    """Raised when a requested job does not exist."""


class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(
        self,
        job_id: str,
        task: str,
        priority: int = 1,
    ) -> Job:

        if self.repository.exists(job_id):
            raise JobAlreadyExistsError(
                f"Job with ID '{job_id}' already exists"
            )

        job = Job(
            job_id=job_id,
            task=task,
            priority=priority,
        )

        self.repository.save(job)

        return job

    def get_job(self, job_id: str) -> Job:
        job = self.repository.get_by_id(job_id)

        if job is None:
            raise JobNotFoundError(
                f"Job with ID '{job_id}' was not found"
            )

        return job