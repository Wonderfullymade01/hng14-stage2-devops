# ---------- Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Runtime ----------
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

ENV PATH=/home/appuser/.local/bin:$PATH

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"] 