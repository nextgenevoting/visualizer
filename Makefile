dev:
	urxvt -e sh -c 'tmuxp load tmuxp.yaml'

up:
	docker-compose up

build:
	docker-compose build

docker-clean:
	docker rmi -f chvotedemonstrator_backend || true
	docker rmi -f chvotedemonstrator_frontend || true
	for n in $$(docker ps -a -q); do docker rm $$n; done
	for n in $$(docker images | awk '/<none>/{ print $$3 }'); do docker rmi -f $$n; done

.PHONY: up build docker-clean
