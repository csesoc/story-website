## COMMON COMMANDS

.PHONY: stop

stop:
	docker-compose down

## DEVELOPMENT MODE

.PHONY: build-dev dev destroy-dev restart-dev

build-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

destroy-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v

restart-dev: destroy-dev build-dev

## PRODUCTION MODE

.PHONY: build run restart

build:
	docker-compose up --build -d

run:
	docker-compose up -d

restart:
	docker-compose down -v
	docker-compose up --build -d

## TESTS

.PHONY: test-backend

test-backend:
	docker-compose exec backend pytest ./test/puzzle $(args)
