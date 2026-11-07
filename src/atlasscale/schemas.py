from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    job_id: str = Field(min_length=1)
    task: str = Field(min_length=1)
    priority: int = Field(default=1, ge=1)