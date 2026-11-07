from atlasscale.job import Job


class InMemoryJobRepository:
    def __init__(self):
        self._jobs: dict[str, Job] = {}

    def save(self, job: Job) -> Job:
        self._jobs[job.job_id] = job
        return job

    def get_by_id(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def exists(self, job_id: str) -> bool:
        return job_id in self._jobs

    def clear(self) -> None:
        self._jobs.clear()