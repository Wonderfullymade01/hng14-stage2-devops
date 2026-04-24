# ---------- Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Runtime ----------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Ensure Python can find your package
ENV PYTHONPATH=/app

# Ensure installed packages are accessible
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy installed dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Fix ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Healthcheck (curl may not exist in slim image → safer fix below)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]