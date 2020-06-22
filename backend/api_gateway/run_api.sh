docker rm -f $(docker ps -aq) # delete all containers
docker build -t  robertwojtas/api_gateway . # build docker image
docker run -it -p 5000:5000 robertwojtas/api_gateway # run container
