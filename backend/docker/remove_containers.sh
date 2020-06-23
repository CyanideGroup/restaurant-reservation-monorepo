for CONTAINER_NAME in $*
do 
    docker rm -f $CONTAINER_NAME
done