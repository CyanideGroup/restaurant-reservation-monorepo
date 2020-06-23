docker build -t  robertwojtas/admin_gateway . # build docker image
docker run -it --name admin_gateway --network cyanidenet -p 5001:5001 robertwojtas/admin_gateway # run container
