build:
	docker build . -t trade_bot:latest

up_dev:
	docker-compose -f docker-compose-dev.yaml up

up:
	docker-compose up

upd:
	docker-compose up -d

down_dev:
	docker-compose -f docker-compose-dev.yaml down

down:
	docker-compose down

test:
	docker-compose -f docker-compose-dev.yaml run trade_bot python /app/manage.py test

lint:
	docker-compose run trade_bot flake8 .

check: lint test
	echo "Success"

migrate:
	docker-compose run trade_bot python manage.py migrate

makemigrations:
	docker-compose run trade_bot python manage.py makemigrations

shell: compose_build
	docker-compose run trade_bot python manage.py shell

connect_bot:
	docker-compose run trade_bot python manage.py connect_bot

manage_help:
	docker-compose run trade_bot python manage.py help