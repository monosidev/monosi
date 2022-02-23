build-api:
	docker build -f deployment/docker/Dockerfile.api -t monosi/monosi-server:latest .

run-api:
	docker run --rm -p 5000:5000 monosi/monosi-server:latest

build-client:
	docker build -f deployment/docker/Dockerfile.client -t monosi/monosi-client:latest .

build-simple:
	docker build -f deployment/docker/Dockerfile.simple -t monosi/monosi:latest .

run-simple:
	docker run --rm -p 3000:3000 monosi/monosi:latest

compose-build:
	cd ./deployment/docker; docker compose build

compose-up:
	cd ./deployment/docker; docker compose up

compose-down:
	cd ./deployment/docker; docker compose down

pkg-test:
	pip install -r requirements.pkg.txt
	python3 -m build
	python3 -m twine upload --repository testpypi dist/*

pkg-prod:
	pip install -r requirements.pkg.txt
	python3 -m build
	python3 -m twine upload dist/*
