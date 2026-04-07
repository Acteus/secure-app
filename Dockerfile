# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS builder
WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip==25.0.1 && \
    pip install --no-cache-dir --target /opt/python -r requirements.txt

COPY app/ /app/app/

FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/python

COPY --from=builder /opt/python /opt/python
COPY --from=builder /app /app

EXPOSE 8080
ENTRYPOINT ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app.main:app"]

