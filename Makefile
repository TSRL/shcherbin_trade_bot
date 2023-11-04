build:
	docker build . -t trade_bot:latest

compose_build:
	docker-compose build

up:
	docker-compose up

upd:
	docker-compose up -d

down:
	docker-compose down

test: compose_build
	docker-compose run trade_bot python /app/manage.py test

lint: compose_build
	docker-compose run trade_bot flake8 .

check: compose_build lint test
	echo "Success"

migrate: compose_build
	docker-compose run trade_bot python manage.py migrate

shell: compose_build
	docker-compose run trade_bot python manage.py shell

plug_tg_bot:
	docker-compose run trade_bot python manage.py createtgbot