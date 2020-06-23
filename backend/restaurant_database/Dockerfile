FROM postgres:12-alpine

ENV POSTGRES_PASSWORD=secretcyanideapp

COPY init_restaurant.sh /docker-entrypoint-initdb.d

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
