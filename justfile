# https://github.com/casey/just
image_name := 'fastapi-rest-smg:dev'

build:
    docker build -t {{image_name}} .

run:
    docker run -d -p 8000:8000 -w /app -v "$(pwd):/app" {{image_name}}

shell:
    docker exec -it {{image_name}} -- bash
