# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (SECURITY REQUIREMENT)
RUN useradd -m appuser

# Copy installed dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Ensure PATH includes user installs
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY . .

# Switch to non-root user
USER appuser

EXPOSE 8000

# Healthcheck (production-grade)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 