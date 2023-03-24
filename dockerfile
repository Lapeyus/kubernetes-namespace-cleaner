FROM python:3.7 AS base

RUN pip install kubernetes
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]
