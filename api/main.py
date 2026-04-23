from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()

# ----------------------------
# Redis configuration
# ----------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# ----------------------------
# HEALTH CHECK (REQUIRED)
# ----------------------------
@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}


# ----------------------------
# ROOT ENDPOINT (TEST FIX)
# ----------------------------
@app.get("/")
def root():
    return {"message": "Job API is running"}


# ----------------------------
# CREATE JOB
# ----------------------------
@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())

    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", mapping={"status": "queued"})

    return {"job_id": job_id, "status": "queued"}


# ----------------------------
# GET JOB STATUS
# ----------------------------
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        return {"error": "not found"}

    return {
        "job_id": job_id,
        "status": status
    } 