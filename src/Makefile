.PHONY: install
install:
	poetry install

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: makemigrations
makemigrations:
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: runserver
runserver:
	poetry run python manage.py runserver

.PHONY: superuser
superuser:
	poetry run python manage.py makesuperuser

.PHONY: update
update:
	install migrate install-pre-commit;

.PHONY: flake
flake:
	poetry run flake8

.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env; docker-compose -f docker-compose.yaml up --force-recreate db

.PHONY: users_delete
users_delete:
	poetry run python manage.py runscript scripts.delete_users

.PHONY: add_course_1
add_course_1:
	poetry run python manage.py runscript scripts.course_1


.PHONY: reset_words
reset_words:
	poetry run python manage.py runscript scripts.reset_words_table;

.PHONY: reset_courses
reset_courses:
	poetry run python manage.py runscript scripts.reset_courses_table

.PHONY: course_1
course_1:
	reset_words reset_courses add_course_1

.PHONY: add_course_2
add_course_2:
	poetry run python manage.py runscript scripts.course_2

.PHONY: course_2
course_2:
	reset_words reset_courses add_course_2
