docker build -t robertwojtas/reservation_database .
docker run --name reservation_database --network cyanidenet -d -p 5433:5432 robertwojtas/reservation_database
