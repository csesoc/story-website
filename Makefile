## DEVELOPMENT MODE

build-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

destroy-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v

## PRODUCTION MODE

build:
	docker-compose up --build -d

run:
	docker-compose up -d

restart:
	docker-compose down -v
	docker-compose up --build -d

## TESTS

test-backend:
	docker-compose exec backend pytest .
