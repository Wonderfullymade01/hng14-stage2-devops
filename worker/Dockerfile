# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (SECURITY REQUIREMENT)
RUN useradd -m appuser

# Copy dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Ensure PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy app code
COPY . .

# Switch to non-root user
USER appuser

# Healthcheck (Redis dependency check)
HEALTHCHECK --interval=30s --timeout=5s --retries=5 --start-period=15s \
  CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379))); r.ping()"

CMD ["python", "worker.py"] 