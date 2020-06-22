docker build -t robertwojtas/notification_database .
docker run --name notification_database --network cyanidenet -d -p 5435:5432 robertwojtas/notification_database
