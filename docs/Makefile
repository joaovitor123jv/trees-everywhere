COLOR_RESET=\033[0m
COLOR_RED=\033[0;31m
COLOR_GREEN=\033[0;32m
COLOR_YELLOW=\033[0;33m
COLOR_BLUE=\033[0;34m

.PHONY: doc, clean, help

help: ## Show this help.
	@echo "${COLOR_YELLOW} ============= TreesEverywhere - Documentation ============= ${COLOR_RESET}"
	@echo " "
	@echo "Please use \`make ${COLOR_BLUE}<target>${COLOR_RESET}' where ${COLOR_BLUE}<target>${COLOR_RESET} is one of"
	@echo " "
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "- ${COLOR_BLUE}%-30s${COLOR_RESET} %s\n", $$1, $$2}'


clean: ## Removes remaining files from build. This runs automatically after building the docs.
	@rm -f main.aux main.toc main.out main.lol main.log


doc: ## Builds the documentation.
	@cd .. && make setup
	@bash -c "source ../venv/bin/activate && pdflatex --shell-escape src/main.tex"
	@make clean

# Build the documentation, but does not require 'make setup' to be run first. Called from the main Makefile.
_doc:
	@bash -c "source ../venv/bin/activate && pdflatex --shell-escape src/main.tex"
	@make clean