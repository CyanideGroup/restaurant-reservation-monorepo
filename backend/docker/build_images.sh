for IMAGE_NAME in $*
do 
    docker rmi robertwojtas/$IMAGE_NAME:latest
    docker build -t ../robertwojtas/$IMAGE_NAME ./$IMAGE_NAME
done