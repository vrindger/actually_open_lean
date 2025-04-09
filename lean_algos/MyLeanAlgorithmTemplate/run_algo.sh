cp -rf ../../base .
BASE_DIR=./base
git submodule update --remote

ALGO=MyLeanAlgorithmTemplate
lower_case_algo=$(echo $ALGO | tr '[:upper:]' '[:lower:]')

bash $BASE_DIR/docker_cleanup.sh  # optional if u want to save each docker image/container for some weird reason

docker build --build-arg GITHUB_USERNAME=vrindger \
            --build-arg GITHUB_PAT=$GITHUB_PAT \
            -t lean_$lower_case_algo:debug \
            -f Dockerfile .

rm -rf base
# run built image
docker run -it lean_$lower_case_algo:debug  --config /base/config.json --algorithm-location /base/algo.py