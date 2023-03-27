FROM python:3.10

RUN mkdir -p /app

WORKDIR /app
COPY requirements.txt main.py dynamodb_bean_template.j2 /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "main"]
