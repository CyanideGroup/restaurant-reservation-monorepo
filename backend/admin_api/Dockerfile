FROM python:alpine

# RUN apk add build-base libressl-dev libffi-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src /app

WORKDIR /app

EXPOSE 5001

ENTRYPOINT [ "python" ]

CMD [ "admin_gateway.py" ]