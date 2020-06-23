FROM python:alpine

# RUN apk add build-base libressl-dev libffi-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "api_gateway.py" ]
