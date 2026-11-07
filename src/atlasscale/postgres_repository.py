from sqlalchemy import delete
from sqlalchemy.orm import Session

from atlasscale.database.models import JobModel
from atlasscale.interfaces import JobRepository
from atlasscale.job import Job, JobStatus


class PostgresJobRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, job: Job) -> Job:

        model = self.session.get(JobModel, job.job_id)

        if model is None:
            model = JobModel(
                job_id=job.job_id,
                task=job.task,
                priority=job.priority,
                status=job.status.value,
            )

            self.session.add(model)

        else:
            model.task = job.task
            model.priority = job.priority
            model.status = job.status.value

        self.session.commit()

        return job

    def get_by_id(self, job_id: str) -> Job | None:

        model = self.session.get(JobModel, job_id)

        if model is None:
            return None

        return self._to_domain(model)

    def exists(self, job_id: str) -> bool:

        return self.session.get(JobModel, job_id) is not None

    def clear(self) -> None:

        self.session.execute(delete(JobModel))
        self.session.commit()

    @staticmethod
    def _to_domain(model: JobModel) -> Job:

        job = Job(
            job_id=model.job_id,
            task=model.task,
            priority=model.priority,
        )

        if model.status == JobStatus.RUNNING.value:
            job.start()

        elif model.status == JobStatus.COMPLETED.value:
            job.start()
            job.complete()

        elif model.status == JobStatus.FAILED.value:
            job.start()
            job.fail()

        elif model.status != JobStatus.PENDING.value:
            raise ValueError(
                f"Unknown job status: {model.status}"
            )

        return job