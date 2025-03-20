ALGO=scratch
lower_case_algo=$(echo $ALGO | tr '[:upper:]' '[:lower:]')

bash docker_cleanup.sh

docker build --build-arg CONFIG_TO_USE=$ALGO \
            --build-arg GITHUB_USERNAME=$GITHUB_USERNAME \
            --build-arg GITHUB_PAT=$GITHUB_PAT \
            -t lean_$lower_case_algo:debug \
            -f Dockerfile_scratch .

# run built image
docker run -it lean_$lower_case_algo:debug