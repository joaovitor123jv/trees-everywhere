COLOR_RESET=\033[0m
COLOR_RED=\033[0;31m
COLOR_GREEN=\033[0;32m
COLOR_YELLOW=\033[0;33m
COLOR_BLUE=\033[0;34m

LOG_SUCCESS=bin/log_success.sh
LOG_WARNING=bin/log_warning.sh
LOG_ERROR=bin/log_error.sh
LOG_DEFAULT=bin/log_default.sh

BIN_HELPERS=${LOG_DEFAULT} ${LOG_WARNING} ${LOG_ERROR} ${LOG_SUCCESS}

.PHONY: help, doc, clean, update-requirements, setup, start, start-production, migrate, migrate-native, migrations, \
	migrations-native, django-shell, bash-shell, stop, clean

# Function to print current date
date = $(shell date +"%Y-%M-%d %H:%M:%S")

DJANGO_SRC_DIR = app_src
DJANGO_APP_NAME = trees_everywhere

help: ## Show this help.
	@echo "${COLOR_YELLOW} ============= Welcome to TreesEverywhere ============= ${COLOR_RESET}"
	@echo " "
	@echo "Please use \`make ${COLOR_BLUE}<target>${COLOR_RESET}' where ${COLOR_BLUE}<target>${COLOR_RESET} is one of"
	@echo " "
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "- ${COLOR_BLUE}%-30s${COLOR_RESET} %s\n", $$1, $$2}'


fix-permissions: ${BIN_HELPERS}
	@bash ${LOG_DEFAULT} "Enabling bin helpers execution..."
	@chmod +x $^
	@${LOG_SUCCESS} "Enabling bin helpers execution... DONE"


# The venv directory should not be included in the docker image, do NOT move it to app_src directory
venv: fix-permissions requirements.txt
	@${LOG_DEFAULT} "Creating python virtual environment..."
	@${LOG_WARNING} "\t Ensuring virtualenv is installed..."
	@python3 -m pip install virtualenv &> /dev/null
	@${LOG_WARNING} "\t Generating venv folder..."
	@python3 -m virtualenv venv &> /dev/null
	@${LOG_WARNING} "\t Installing requirements.txt libraries..."
	@venv/bin/pip install -r requirements.txt
	@${LOG_SUCCESS} "Creating python virtual environment... DONE"


update-requirements: venv ## Update requirements.txt
	@${LOG_DEFAULT} "Updating requirements.txt..."
	@venv/bin/pip freeze > requirements.txt
	@${LOG_SUCCESS} "Updating requirements.txt... DONE"


update-fixtures: ## Update fixtures
	@${LOG_DEFAULT} "Updating fixtures..."
	@docker-compose run ${DJANGO_APP_NAME} python manage.py dumpdata \
		--indent 4 \
		--natural-foreign \
		--natural-primary \
		--exclude auth.permission \
		--exclude sessions.session \
		--exclude admin.logentry \
		--exclude contenttypes \
		> fixtures.json
	@${LOG_SUCCESS} "Updating fixtures... DONE"


setup: fix-permissions venv ## Setup the project, installing python dependencies, fixing file permissions and creating virtual environments if needed
	@${LOG_SUCCESS} "Setting up the project... DONE"


docker-compose.yaml:
	@${LOG_ERROR} "Cannot find file named $$(pwd)/docker-compose.yaml"
	@${LOG_ERROR} "Ensure this file exists, and check the executed command and your current working directory"


start-production: docker-compose-production.yaml ## Start the application (production environment, docker-only)
	@${LOG_ERROR} "==== STARTING APPLICATION IN PRODUCTION MODE ===="
	$# Intentionally showing executed command. This is a security measure to ensure the user is aware of what is being executed
	docker-compose -f docker-compose-production.yml up -d


start: docker-compose.yaml ## Start the application (development environment)
	@${LOG_DEFAULT} "==== Starting application in development mode (over docker) ===="
	@${LOG_WARNING} "\t Starting database service over docker"
	@docker-compose up -d db
	@${LOG_WARNING} "\t Ensuring database structure is up to date"
	@make migrate
	@${LOG_WARNING} "\t Starting Django application service over docker"
	@docker-compose up


start-native: docker-compose.yaml venv ## Start the application (development environment)
	@${LOG_DEFAULT} "==== Starting application in development mode (native) ===="
	@${LOG_WARNING} "\t Starting database service over docker"
	@docker-compose -f docker-compose.yaml up -d db
	@${LOG_WARNING} "\t Ensuring database structure is up to date"
	@make migrate-native
	@${LOG_WARNING} "\t Starting Django application service over docker"
	@venv/bin/python $(DJANGO_SRC_DIR)/manage.py runserver 0.0.0.0:8000


migrate: ## Run migrations
	@${LOG_DEFAULT} "Running migrations..."
	@docker-compose run $(DJANGO_APP_NAME) python manage.py migrate
	@${LOG_SUCCESS} "Running migrations... DONE"


migrate-native: venv ## Run migrations (python native + postgresql on docker)
	@${LOG_DEFAULT} "Running migrations (native)..."
	@venv/bin/python $(DJANGO_SRC_DIR)/manage.py migrate
	@${LOG_SUCCESS} "Running migrations (native)... DONE"


migrations: ## Create migrations (use the argument 'name' to specify the name of the application)
	@${LOG_DEFAULT} "Parsing models to look for pending migrations..."
	docker-compose run $(DJANGO_APP_NAME) python manage.py makemigrations $(name)
	@${LOG_SUCCESS} "Parsing models to look for pending migrations... DONE"


load-fixtures: ## Load fixtures
	@${LOG_DEFAULT} "Loading fixtures..."
	@docker-compose run $(DJANGO_APP_NAME) python manage.py loaddata ./fixtures.json
	@${LOG_SUCCESS} "Loading fixtures... DONE"


django-shell: ## Run django shell on the app container
	@${LOG_WARNING} "Running Django shell (over docker). Good luck in whatever you need to do, fellow warrior!"
	@docker-compose run $(DJANGO_APP_NAME) python manage.py shell
	@${LOG_SUCCESS} "Finished shell process successfully!"


bash-shell: ## Run bash shell on the app container
	@${LOG_WARNING} "Running BASH shell. Good luck in whatever you need to do, fellow warrior!"
	@docker-compose run $(DJANGO_APP_NAME) bash
	@${LOG_SUCCESS} "Finished shell process successfully!"


stop: ## Stop the application
	@${LOG_WARNING} "==== Stopping application ===="
	@docker-compose down


doc: venv ## Generate documentation
	@${LOG_DEFAULT} "Generating documentation..."
	@cd docs && make _doc
	@${LOG_SUCCESS} "Generating documentation... DONE"


clean: ## Clean the project, removing all generated files, docker images, containers and volumes
	@Cleaning up..."
	@${LOG_WARNING} "\t Removing virtual environment..."
	@rm -rf venv
	@${LOG_WARNING} "\t Removing docker images..."
	@docker-compose down --rmi all &> /dev/null
	@${LOG_WARNING} "\t Removing docker volumes..."
	@docker-compose down --volumes &> /dev/null
	@${LOG_WARNING} "\t Removing database data..."
	@rm -rf db_data
	@${LOG_SUCCESS} "Cleaning up... DONE"