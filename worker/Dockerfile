# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Final stage ----------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy installed dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Copy app code
COPY . .

# Set environment
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

# ---------------- HEALTHCHECK (CORRECT) ----------------
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=10s \
  CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379))); r.ping()"

# Run worker
CMD ["python", "worker.py"] 