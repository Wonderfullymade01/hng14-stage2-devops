# FIXES.md - Stage 2 DevOps Microservices Application

This document contains all issues identified in the application and the fixes applied to ensure proper containerization, orchestration, and production readiness.

---

## FIX 1: Missing API root endpoint

- **File:** api/main.py
- **Line:** 13-15
- **Problem:** API root endpoint ("/") was not defined, causing a 404 response when accessing the base URL.
- **Fix:** Added a root endpoint to return a service status message.

```python
@app.get("/")
def root():
    return {"message": "Job API is running"}
```
---

## FIX 2: Missing health check endpoint required for Docker
**File:** api/main.py
**Line:** 12-14 (after Redis client setup)
**Problem:** Docker healthcheck configuration required /health, but none existed in the API.
**Fix:** Added a /health endpoint for container health validation.

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```
---

## FIX 3: API container healthcheck failure due to missing endpoint
**File:** api/Dockerfile
**Line:** 25-28 (Added at the end of Dockerfile)
**Problem:** API container lacked a proper HEALTHCHECK instruction, causing unreliable container status reporting.
**Fix:** Added HTTP-based healthcheck using the /health endpoint.

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
   CMD curl --fail http://localhost:8000/health || exit 1
```
---

## FIX 4: Worker running as root user (security issue)
**File:** worker/Dockerfile
**Line:** 12-15
**Problem:** Worker container executed as root by default, violating production security best practices.
**Fix:** Created a non-root user and switched execution context.

```dockerfile
RUN useradd -m appuser
USER appuser
```
---

## FIX 5: Redis configuration not standardized across services
**File:** api/main.py, worker/worker.py
**Line:** 8-11 in both files
**Problem:** Redis host and port were not consistently enforced via environment variables.
**Fix:** Standardized Redis configuration using environment variables with defaults.

```python
host = os.getenv("REDIS_HOST", "redis")
port = int(os.getenv("REDIS_PORT", 6379))
```
---

## FIX 6: Frontend API URL hardcoded (Docker networking issue)
**File:** frontend/app.js
**Line:** 6
**Problem:** Using localhost breaks communication inside Docker containers.
**Fix:** Replaced with environment-based API URL.

```javascript
const API_URL = process.env.API_URL || "http://api:8000";
```
---

## FIX 7: Frontend dependency on API readiness
**File:** docker-compose.yml
**Line:** 42-48
**Problem:** Frontend could start before API was ready, leading to failed API calls.
**Fix:** Added dependency condition based on API health.

```yaml
depends_on:
  api:
    condition: service_healthy
```
---

## FIX 8: Redis worker missing retry safety on startup
**File:** worker/worker.py
**Line:** 10-20
**Problem:** Worker could crash if Redis was not ready at startup.
**Fix:** Added retry loop to wait for Redis availability.

```python
while True:
    try:
        r = redis.Redis(host=host, port=port, decode_responses=True)
        r.ping()
        break
    except Exception:
        time.sleep(2)
```
---

## FIX 9: Worker job processing lifecycle consistency
**File:** worker/worker.py
**Line:** 22-26
**Problem:** Job processing needed consistent status updates.
**Fix:** Ensured job status is updated correctly after processing.

```python
def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
```
---
