compose-build:
	cd ./deployment/docker; docker compose build

compose-up:
	cd ./deployment/docker; docker compose up -d

compose-pull:
	cd ./deployment/docker; docker compose pull

compose:
	make compose-pull
	make compose-up

compose-down:
	cd ./deployment/docker; docker compose down

