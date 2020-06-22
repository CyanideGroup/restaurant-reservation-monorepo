docker build -t robertwojtas/search_database .
docker run --name search_database --network cyanidenet -d -p 5434:5432 robertwojtas/search_database
