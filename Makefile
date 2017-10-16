staging:
	docker-compose -f docker-compose.yaml -f docker-compose.staging.yaml up

dev:
	docker-compose up

docker-clean:
	docker rmi -f chvotedemonstrator_backend || true
	docker rmi -f chvotedemonstrator_frontend || true
	for n in $$(docker ps -a -q); do docker rm $$n; done
	for n in $$(docker images | awk '/<none>/{ print $$3 }'); do docker rmi -f $$n; done

.PHONY: staging dev docker-clean
