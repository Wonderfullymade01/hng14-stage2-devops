FROM python:3.11-slim

WORKDIR /app

# non-root user (REQUIRED)
RUN useradd -m appuser
USER appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

CMD ["python", "worker.py"]