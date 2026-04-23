# Stage 2 DevOps: Microservices Task Processor

## Overview
This is a containerized microservices system designed for asynchronous job processing. It demonstrates core DevOps principles: service orchestration, health-dependent startup, and decoupled communication.

**Tech Stack:**
* **Frontend:** Node.js (Express)
* **API:** FastAPI (Python)
* **Queue:** Redis
* **Worker:** Python (Background Processor)

---

## Architecture Flow
1. **Frontend:** Sends a POST request to the API.
2. **API:** Generates a unique Job ID and pushes the task to the Redis queue.
3. **Worker:** Consumes the job from Redis and simulates processing.
4. **Redis:** Acts as the message broker and state store.
5. **Frontend:** Polls the API to retrieve the updated job status.

---

## Getting Started

### Prerequisites
* Docker & Docker Compose (v2.0+)
* Git

### Setup & Installation
1. **Clone the repository**
   ```bash
   git clone [https://github.com/wonderfullymade01/hng14-stage2-devops.git](https://github.com/wonderfullymade01/hng14-stage2-devops.git)
   cd hng14-stage2-devops

2. Configure Environment
```Bash
cp .env.example .env

3. Deploy the Stack
```Bash
docker compose up --build -d

4. Verify Status
Check that all services show (healthy):
```Bash
docker compose ps

Service,Endpoint,Description
Frontend,http://localhost:3000,Application UI
API Docs,http://localhost:8000/docs,Interactive Swagger API Docs
Health,http://localhost:8000/health,API Health Check

Testing the Workflow
To verify the background worker is processing jobs:

Access the Frontend at http://localhost:3000.

Trigger a new job via the UI.

Stream the worker logs to see real-time processing:

```Bash
docker compose logs -f worker

Development & DevOps Notes
Networking: All services communicate over a private bridge network. Redis is isolated and not exposed to the host machine for security.

Orchestration: Used depends_on with service_healthy conditions to ensure the API and Worker only start once the Redis broker is ready.

Resource Management: Applied CPU (0.5) and Memory (512MB) limits in the Compose file to simulate production resource constraints. 