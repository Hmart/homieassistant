src=.

.PHONY: lint
lint: ## PEP8 syntax check
	@docker-compose run --rm --name flake8 --no-deps django python -m flake8 .

.PHONY: black
black: ## Black python code formatter
	@docker-compose run --rm --name black --no-deps django python -m black .

.PHONY: isort
isort: ## Orders imports alphabetically
	@docker-compose run --rm --name isort --no-deps django python -m isort -rc .

.PHONY: collectstatic
collectstatic: ## Collect static files
	@docker-compose run --rm --name collectstatic --no-deps django ./manage.py collectstatic --noinput

.PHONY: migrations
migrations: ## Create migrations
	@docker-compose run --rm --name makemigrations --no-deps django ./manage.py makemigrations

.PHONY: migrate
migrate: ## Run migrations
	@docker-compose run --rm --name manage_migrate --no-deps django ./manage.py migrate --noinput

opts	:= $(opts)

ifeq ("$(detach)", "yes")
	opts := $(opts) -d
endif
ifeq ("$(build)", "yes")
	opts := $(opts) --build
endif

ifneq ("$(test-path)", "")
	cargs := $(test-path)
else
	cargs := $(src)
endif
ifeq ("$(tag)", "")
	cargs := $(cargs) --exclude-tag=integration
else ifeq ("$(tag)", "all")
	cargs := $(cargs)
else
	cargs := $(cargs) --tag=$(tag)
endif
ifeq ("$(keepdb)", "yes")
	cargs := $(cargs) --keepdb
endif

.PHONY: createsuperuser
createsuperuser: ## Create admin user and 2FA QR code
	docker-compose run --rm django $(src)/manage.py createsuperuser --email $(email) --settings=homieassistant.settings
	@echo One time use token:
	docker-compose run --rm django $(src)/manage.py addstatictoken $(email) --settings=homieassistant.settings

.PHONY: addstatictoken
addstatictoken: ## Get 2FA code for email
	docker-compose run --rm django $(src)/manage.py addstatictoken $(email) --settings=homieassistant.settings

.PHONY: check
check: ## Django check
	@docker-compose run --rm django $(src)/manage.py check --settings=homieassistant.settings

.PHONY: test
test: ## Run unit tests - args: [detach=no] [keepdb=no] [test-path=.]
	docker-compose run --rm $(opts) django $(src)/manage.py test -t $(src) $(cargs) --settings=homieassistant.settings_test

.PHONY: fg
fg: ## Start a container session for project
	@docker-compose run --rm --name fg -w /app --entrypoint bash django

.PHONY: coverage
coverage: ## Measure and report code coverage
	docker-compose run --rm --name coverage django bash -c "coverage run $(src)/manage.py test -t $(src) --settings=homieassistant.settings_test && coverage report"

.PHONY: coverage-html
coverage-html: ## Measure code coverage and store it as browsable html in ./htmlcov/
	docker-compose run --name coverage django bash -c "coverage run $(src)/manage.py test -t $(src) --settings=homieassistant.settings_test && coverage html"
	@docker cp coverage:/app/htmlcov/ ./
	@docker rm coverage
	@echo "file://$$(cd "htmlcov"; pwd -P)/index.html"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
