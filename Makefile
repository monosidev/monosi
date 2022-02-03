build-api:
	docker build -f deployment/docker/Dockerfile.api -t monosi/monosi-server:latest .

run-api:
	docker run --rm -p 5000:5000 monosi/monosi-server:latest

build-client:
	docker build -f deployment/docker/Dockerfile.client -t monosi/monosi-webapp:latest .

build-simple:
	docker build -f deployment/docker/Dockerfile.simple -t monosi/monosi:latest .

run-simple:
	docker run --rm -p 3000:3000 monosi/monosi:latest

build:
	cd ./deployment/docker; docker-compose build

run:
	cd ./deployment/docker; docker-compose up
