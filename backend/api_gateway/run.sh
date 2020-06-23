docker build -t  robertwojtas/api_gateway . # build docker image
docker run -it --name api_gateway --network cyanidenet -p 5000:5000 robertwojtas/api_gateway # run container
