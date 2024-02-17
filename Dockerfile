FROM python:3.11
WORKDIR /project

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ="Asia/Krasnoyarsk" \
    METRICS_GATEWAY_WORKERS=1 \
    WORKERS=1

COPY ./requirements.txt .

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c", "uvicorn --host 0.0.0.0 --port 8000 --workers=$WORKERS src.rest_app:app"]