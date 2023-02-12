COLOR_RESET=\033[0m
COLOR_RED=\033[0;31m
COLOR_GREEN=\033[0;32m
COLOR_YELLOW=\033[0;33m
COLOR_BLUE=\033[0;34m

.PHONY: help, doc, clean, update-requirements, setup, start, start-production, migrate, migrations, django-shell, \
	bash-shell, stop, clean

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


# The venv directory should not be included in the docker image, do NOT move it to app_src directory
venv: requirements.txt
	@echo "[$(date)] ${COLOR_BLUE}Creating python virtual environment...${COLOR_RESET}"
	@echo "[$(date)] \t ${COLOR_YELLOW}Ensuring virtualenv is installed...${COLOR_RESET}"
	@python3 -m pip install virtualenv &> /dev/null
	@echo "[$(date)] \t ${COLOR_YELLOW}Generating venv folder...${COLOR_RESET}"
	@python3 -m virtualenv venv &> /dev/null
	@echo "[$(date)] \t ${COLOR_YELLOW}Installing requirements.txt libraries...${COLOR_RESET}"
	@venv/bin/pip install -r requirements.txt
	@echo "[$(date)] ${COLOR_GREEN}Creating python virtual environment... DONE${COLOR_RESET}"


update-requirements: venv ## Update requirements.txt
	@echo "[$(date)] ${COLOR_BLUE}Updating requirements.txt...${COLOR_RESET}"
	@venv/bin/pip freeze > requirements.txt
	@echo "[$(date)] ${COLOR_GREEN}Updating requirements.txt... DONE${COLOR_RESET}"


update-fixtures: venv ## Update fixtures
	@echo "[$(date)] ${COLOR_BLUE}Updating fixtures...${COLOR_RESET}"
	@docker-compose run ${DJANGO_APP_NAME} python manage.py dumpdata \
		--indent 4 \
		--natural-foreign \
		--natural-primary \
		--exclude auth.permission \
		--exclude contenttypes \
		> fixtures.json
	@echo "[$(date)] ${COLOR_GREEN}Updating fixtures... DONE${COLOR_RESET}"


setup: venv ## Setup the project, installing python dependencies and creating virtual environments if needed
	@echo "[$(date)] ${COLOR_GREEN}Setting up the project... DONE${COLOR_RESET}"


docker-compose.yaml:
	@echo "[$(date)] ${COLOR_RED}Cannot find file named $$(pwd)/docker-compose.yaml${COLOR_RESET}"
	@echo "[$(date)] \t ${COLOR_RED}Ensure this file exists, and check the executed command and your current"
	@echo "[$(date)] \t working directory${COLOR_RESET}"


start-production: docker-compose-production.yaml ## Start the application (production environment, docker-only)
	@echo "[$(date)] ${COLOR_RED}==== STARTING APPLICATION IN PRODUCTION MODE ====${COLOR_RESET}"
	@docker-compose -f docker-compose-production.yml up -d


start: docker-compose.yaml ## Start the application (development environment)
	@echo "[$(date)] ${COLOR_GREEN}==== Starting application in development mode (over docker) ====${COLOR_RESET}"
	@docker-compose up -d db
	@make migrate
	@docker-compose up


start-native: docker-compose.yaml venv ## Start the application (development environment)
	@echo "[$(date)] ${COLOR_GREEN}==== Starting application in development mode (native) ====${COLOR_RESET}"
	@docker-compose -f docker-compose.yaml up -d db
	@venv/bin/python $(DJANGO_SRC_DIR)/manage.py runserver 0.0.0.0:8000


migrate: ## Run migrations
	@echo "[$(date)] ${COLOR_BLUE}Running migrations...${COLOR_RESET}"
	@docker-compose run $(DJANGO_APP_NAME) python manage.py migrate
	@echo "[$(date)] ${COLOR_GREEN}Running migrations... DONE${COLOR_RESET}"


migrations: ## Create migrations (use the argument 'name' to specify the name of the application)
	@echo "[$(date)] ${COLOR_BLUE}Parsing models to look for pending migrations...${COLOR_RESET}"
	docker-compose run $(DJANGO_APP_NAME) python manage.py makemigrations $(name)
	@echo "[$(date)] ${COLOR_GREEN}Parsing models to look for pending migrations... DONE${COLOR_RESET}"


load-fixtures: ## Load fixtures
	@echo "[$(date)] ${COLOR_BLUE}Loading fixtures...${COLOR_RESET}"
	@docker-compose run $(DJANGO_APP_NAME) python manage.py loaddata ./fixtures.json
	@echo "[$(date)] ${COLOR_GREEN}Loading fixtures... DONE${COLOR_RESET}"


django-shell: ## Run django shell on the app container
	@echo "[$(date)] ${COLOR_YELLOW}Running Django shell. Good luck in whatever you need to do, fellow warrior!${COLOR_RESET}"
	@docker-compose run $(DJANGO_APP_NAME) python manage.py shell
	@echo "[$(date)] ${COLOR_GREEN}Finished shell process successfully!${COLOR_RESET}"


bash-shell: ## Run bash shell on the app container
	@echo "[$(date)] ${COLOR_YELLOW}Running BASH shell. Good luck in whatever you need to do, fellow warrior!${COLOR_RESET}"
	@docker-compose run $(DJANGO_APP_NAME) bash
	@echo "[$(date)] ${COLOR_GREEN}Finished shell process successfully!${COLOR_RESET}"


stop: ## Stop the application
	@echo "[$(date)] ${COLOR_RED}==== Stopping application ====${COLOR_RESET}"
	@docker-compose down


doc: venv ## Generate documentation
	@echo "[$(date)] ${COLOR_BLUE}Generating documentation...${COLOR_RESET}"
	@cd docs && make _doc
	@echo "[$(date)] ${COLOR_GREEN}Generating documentation... DONE${COLOR_RESET}"


clean: ## Clean the project, removing all generated files, docker images, containers and volumes
	@echo "[$(date)] ${COLOR_BLUE}Cleaning up...${COLOR_RESET}"
	@echo "[$(date)] \t ${COLOR_YELLOW}Removing virtual environment...${COLOR_RESET}"
	@rm -rf venv
	@echo "[$(date)] \t ${COLOR_YELLOW}Removing docker images...${COLOR_RESET}"
	@docker-compose down --rmi all &> /dev/null
	@echo "[$(date)] \t ${COLOR_YELLOW}Removing docker volumes...${COLOR_RESET}"
	@docker-compose down --volumes &> /dev/null
	@echo "[$(date)] \t ${COLOR_YELLOW}Removing database data...${COLOR_RESET}"
	@rm -rf db_data
	@echo "[$(date)] ${COLOR_GREEN}Cleaning up... DONE${COLOR_RESET}"