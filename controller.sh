IMAGE_NAME="flask_amcef_app"
CONTAINER_NAME="flask_amcef"

case "$1" in
  run)
    if [[ "$(docker container ls -a -q -f name=$CONTAINER_NAME 2> /dev/null)" == "" ]]; then
        echo "Building image..."
        docker build -t "$IMAGE_NAME" .
    fi
    docker run -p 3000:3000 --name "$CONTAINER_NAME" "$IMAGE_NAME"
  ;;
  clr)
    docker stop "$CONTAINER_NAME" || true
    docker rm "$CONTAINER_NAME" || true
    docker rmi "$IMAGE_NAME" || true
    ;;
  restart)
    docker stop "$CONTAINER_NAME" || true
    docker start "$CONTAINER_NAME" 
    ;;
  update)
    ./controller.sh clr
    ./controller.sh run
    ;;
  stop)
    docker stop $(docker ps -a -q)
    ;;
  help)
    echo "Here are commands that you can run with my app and docker. Enjoy!"
    echo "install - Installs needed files for running aplicaiton"
    echo "run - Starts flask app"
    echo "clr - Deletes Image for this projects"
    echo "restart - Restarts app"
    echo "update - Removes containers and image and creates new (do if there are changes in code)"
    echo "stop - Stops any running containers"
    ;;
  *)
    echo "Usage: install | run | clr | help | restart | update | stop"
    exit 1
    ;;
esac