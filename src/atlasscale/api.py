from fastapi import FastAPI, HTTPException

from atlasscale.schemas import JobCreateRequest
from atlasscale.postgres_repository import PostgresJobRepository
from atlasscale.services import (
    JobService,
    JobAlreadyExistsError,
    JobNotFoundError,
)


# Create repository
job_repository = PostgresJobRepository()

# Inject repository into service
job_service = JobService(job_repository)


app = FastAPI(
    title="AtlasScale API",
    description="A job execution and state management system",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {
        "message": "AtlasScale API is running",
        "status": "healthy",
    }


@app.post("/jobs", status_code=201)
def create_job_endpoint(request: JobCreateRequest):
    try:
        job = job_service.create_job(
            job_id=request.job_id,
            task=request.task,
            priority=request.priority,
        )

    except JobAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return {
        "job_id": job.job_id,
        "task": job.task,
        "priority": job.priority,
        "status": job.status,
    }


@app.get("/jobs/{job_id}")
def get_job_endpoint(job_id: str):
    try:
        job = job_service.get_job(job_id)

    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        ) from exc

    return {
        "job_id": job.job_id,
        "task": job.task,
        "priority": job.priority,
        "status": job.status,
    }