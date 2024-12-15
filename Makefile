IMAGE_NAME = picpay-app
CONTAINER_NAME = picpay-container
PORT = 8000

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

restart: stop build run

push:
	docker tag $(IMAGE_NAME) your-repo/$(IMAGE_NAME):latest
	docker push your-repo/$(IMAGE_NAME):latest

clean: stop
	docker rmi $(IMAGE_NAME) || true

build-run: build run
