import os
import time
import redis

# Connect to Redis (same config as API)
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

def process_job(job_id):
    print(f"Processing job {job_id}", flush=True)

    # simulate work
    time.sleep(2)

    # update job status in Redis
    r.hset(f"job:{job_id}", "status", "completed")

    print(f"Done: {job_id}", flush=True)


print("Worker started... waiting for jobs", flush=True)

# MAIN WORKER LOOP
while True:
    # IMPORTANT FIX: must match API queue name "jobs"
    job = r.brpop("jobs", timeout=5)

    if job:
        _, job_id = job
        process_job(job_id)