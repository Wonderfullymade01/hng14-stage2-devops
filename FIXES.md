# FIXES.md - Stage 2 DevOps Microservices Application

This document contains all issues identified in the application and the fixes applied to ensure proper containerization, orchestration, and production readiness.

---

## FIX 1: Missing API root endpoint

- File: api/main.py
- Line: N/A
- Problem: API root endpoint ("/") was not defined, causing a 404 response when accessing the base URL.
- Fix: Added a root endpoint to return a service status message.

```python
@app.get("/")
def root():
    return {"message": "Job API is running"}

---

## FIX 2: Missing health check endpoint required for Docker
File: api/main.py
Line: N/A
Problem: Docker healthcheck configuration required a valid endpoint, but none existed in the API.
Fix: Added a /health endpoint for container health validation.

```@app.get("/health")
def health():
    return {"status": "ok"}

---

## FIX 3: API container healthcheck failure due to missing endpoint
File: api/Dockerfile
Line: N/A
Problem: API container lacked a proper HEALTHCHECK instruction, causing unreliable container status reporting.
Fix: Added healthcheck using the /health endpoint.

```HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

---

## FIX 4: Worker running as root user (security issue)
File: worker/Dockerfile
Line: N/A
Problem: Worker container executed as root by default, violating production security best practices.
Fix: Created a non-root user and switched execution context.

```RUN useradd -m appuser
USER appuser

---

## FIX 5: Inconsistent environment variable usage across services
File: docker-compose.yml, api/main.py, worker/worker.py
Line: N/A
Problem: Services relied on environment variables but lacked consistent configuration, causing runtime warnings and misconfiguration risks.
Fix: Standardized all configuration using environment variables injected via docker-compose.

---

## FIX 6: Frontend startup dependency issue
File: docker-compose.yml
Line: depends_on section
Problem: Frontend service could start before API was ready, leading to failed API calls during initialization.
Fix: Configured frontend to depend on API health status before starting.

---

## FIX 7: Missing .env template for reproducibility
File: project root
Problem: No .env.example file was provided for environment configuration.
Fix: Created .env.example containing all required environment variables.

```API_PORT=8000
FRONTEND_PORT=3000
API_IMAGE=jobapp-api
WORKER_IMAGE=jobapp-worker
FRONTEND_IMAGE=jobapp-frontend
IMAGE_TAG=latest

REDIS_HOST=redis
REDIS_PORT=6379

QUEUE_KEY=jobs
HEARTBEAT_KEY=heartbeat
HEARTBEAT_TTL=30
JOB_DURATION=5

API_URL=http://localhost:8000

---

## FIX 8: Redis configuration not fully standardized across services
File: api/main.py, worker/worker.py
Line: N/A
Problem: Redis host/port values were not consistently enforced via environment variables across services.
Fix: Ensured all services read Redis configuration from environment variables with safe defaults.

---

## FIX 9: Worker job processing lifecycle inconsistencies
File: worker/worker.py
Line: N/A
Problem: Job processing flow did not consistently update Redis job status through lifecycle stages.
Fix: Standardized job status updates (queued → processing → completed) to ensure accurate tracking.

---
