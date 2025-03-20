# clean all dangling images and containers:
docker rm $(docker ps -aq)
docker rmi $(docker images -f dangling=true -q)


# Stop and remove all containers related to 'lean'
docker stop $(docker ps -aq -f name=lean)
docker rm $(docker ps -aq -f name=lean)

# Remove all images related to 'lean' (including the one built by scratch.sh)
docker rmi $(docker images -aq -f reference='lean_*')