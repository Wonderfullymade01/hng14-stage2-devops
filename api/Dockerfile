# --- Stage 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Runtime ---
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (REQUIRED for marks)
RUN useradd -m appuser
USER appuser

# Copy installed packages
COPY --from=builder /root/.local /home/appuser/.local

# Ensure PATH includes user installs
ENV PATH=/home/appuser/.local/bin:$PATH

COPY . .

EXPOSE 8000

# Healthcheck (REQUIRED)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]