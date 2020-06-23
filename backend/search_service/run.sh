docker build -t robertwojtas/search_service .
docker run --name search_service --network cyanidenet -it robertwojtas/search_service
