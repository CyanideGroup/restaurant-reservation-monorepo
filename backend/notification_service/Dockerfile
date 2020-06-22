FROM python:alpine

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY . /app

RUN pip install -r ./requirements.txt

EXPOSE 5672
EXPOSE 5432

ENTRYPOINT ["python", "./notification_service.py"]

