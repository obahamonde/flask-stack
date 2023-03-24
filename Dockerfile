FROM python:3.8.5-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip\
    && pip install --no-cache-dir -r requirements.txt\
    && python -m prisma generate\
    && python -m prisma py fetch

CMD gunicorn app:app --bind 0.0.0.0:5000 --reload