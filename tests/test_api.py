import pytest
from fastapi.testclient import TestClient

from atlasscale.api import app


@pytest.fixture
def client():
    # Start each test with clean job storage
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AtlasScale API is running",
        "status": "healthy",
    }


def test_create_job(client):
    response = client.post(
        "/jobs",
        json={
            "job_id": "job-101",
            "task": "generate_report",
            "priority": 5,
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "job_id": "job-101",
        "task": "generate_report",
        "priority": 5,
        "status": "pending",
    }


def test_create_duplicate_job(client):
    job_data = {
        "job_id": "job-102",
        "task": "process_file",
        "priority": 3,
    }

    first_response = client.post("/jobs", json=job_data)
    second_response = client.post("/jobs", json=job_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_get_existing_job(client):
    client.post(
        "/jobs",
        json={
            "job_id": "job-103",
            "task": "generate_report",
            "priority": 5,
        },
    )

    response = client.get("/jobs/job-103")

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-103"
    assert response.json()["task"] == "generate_report"
    assert response.json()["status"] == "pending"


def test_get_nonexistent_job(client):
    response = client.get("/jobs/job-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_create_job_with_invalid_priority(client):
    response = client.post(
        "/jobs",
        json={
            "job_id": "job-104",
            "task": "process_file",
            "priority": 0,
        },
    )

    assert response.status_code == 422
    

def test_start_job(client):
    # Create a job
    create_response = client.post(
        "/jobs",
        json={
            "job_id": "job-api-start-001",
            "task": "generate_report",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201

    # Start the job
    response = client.post("/jobs/job-api-start-001/start")

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-api-start-001"
    assert response.json()["status"] == "running"
    
    
def test_complete_job(client):
    # Create a job
    create_response = client.post(
        "/jobs",
        json={
            "job_id": "job-api-complete-001",
            "task": "generate_report",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201

    # Start the job
    start_response = client.post(
        "/jobs/job-api-complete-001/start"
    )

    assert start_response.status_code == 200
    assert start_response.json()["status"] == "running"

    # Complete the job
    response = client.post(
        "/jobs/job-api-complete-001/complete"
    )

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-api-complete-001"
    assert response.json()["status"] == "completed"
    
    
def test_fail_job(client):
    # Create a job
    create_response = client.post(
        "/jobs",
        json={
            "job_id": "job-api-fail-001",
            "task": "process_file",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201

    # Start the job
    start_response = client.post(
        "/jobs/job-api-fail-001/start"
    )

    assert start_response.status_code == 200
    assert start_response.json()["status"] == "running"

    # Fail the job
    response = client.post(
        "/jobs/job-api-fail-001/fail"
    )

    assert response.status_code == 200
    assert response.json()["job_id"] == "job-api-fail-001"
    assert response.json()["status"] == "failed"
    
    
def test_start_already_running_job_returns_422(client):
    client.post(
        "/jobs",
        json={
            "job_id": "job-invalid-start-001",
            "task": "generate_report",
        },
    )

    client.post("/jobs/job-invalid-start-001/start")

    response = client.post(
        "/jobs/job-invalid-start-001/start"
    )

    assert response.status_code == 422


def test_complete_pending_job_returns_422(client):
    client.post(
        "/jobs",
        json={
            "job_id": "job-invalid-complete-001",
            "task": "process_file",
        },
    )

    response = client.post(
        "/jobs/job-invalid-complete-001/complete"
    )

    assert response.status_code == 422