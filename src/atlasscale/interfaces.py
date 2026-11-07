from typing import Protocol

from atlasscale.job import Job


class JobRepository(Protocol):

    def save(self, job: Job) -> Job:
        ...

    def get_by_id(self, job_id: str) -> Job | None:
        ...

    def exists(self, job_id: str) -> bool:
        ...

    def clear(self) -> None:
        ...