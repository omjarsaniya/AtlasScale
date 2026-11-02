from atlasscale.job import Job


def main():
    # Create a job
    job = Job(
        job_id="job-001",
        task="generate_report",
        priority=5,
    )

    print(f"Job ID: {job.job_id}")
    print(f"Task: {job.task}")
    print(f"Priority: {job.priority}")
    print(f"Initial status: {job.status}")

    # Start the job
    job.start()
    print(f"After starting: {job.status}")

    # Complete the job
    job.complete()
    print(f"After completion: {job.status}")


if __name__ == "__main__":
    main()