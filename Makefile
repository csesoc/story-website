## DEVELOPMENT MODE

build-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

## PRODUCTION MODE

build:
	docker-compose up --build -d

run:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose down -v
	docker-compose up --build -d

## TESTS

test-backend:
	docker-compose exec backend pytest .
