# Stage 2 DevOps Microservices Application

## Overview
This project is a containerized microservices system built with:
- FastAPI (API service)
- Redis (queue system)
- Worker (background job processor)
- Node.js Express (Frontend)

All services are orchestrated using Docker Compose.

---

## Architecture Flow
1. Frontend sends job request to API
2. API generates job ID and pushes it to Redis queue
3. Worker consumes job from Redis queue
4. Worker processes job and updates status in Redis
5. Frontend queries API for job status

---

## How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/wonderfullymade01/hng14-stage2-devops.git
cd hng14-stage2-devops