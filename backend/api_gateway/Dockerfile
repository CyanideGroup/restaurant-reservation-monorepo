FROM python:alpine

RUN apk add build-base libressl-dev libffi-dev

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["api_gateway.py"]
