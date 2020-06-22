docker build -t robertwojtas/restaurant_database .
docker run --name restaurant_database --network cyanidenet -d -p 5432:5432 robertwojtas/restaurant_database
