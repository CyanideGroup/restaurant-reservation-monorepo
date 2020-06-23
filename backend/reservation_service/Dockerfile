FROM python:3.8-alpine as base

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY src /app

WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "reservation_service.py" ]