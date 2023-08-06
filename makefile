poetry: ## Make venv if applicable and install poetry requirements
poetry:
	poetry install

lint: ## Lint the codebase
lint:
	-ruff .
	-pylint ./blog/* ./users/* ./pull/* --reports yes
	-djlint . --lint
	-autoflake -r .
	-flake8 . --color always --count --statistics
	-black . --check

format: ## Format the codebase
format:
	isort .
	autoflake -r . --in-place --remove-unused-variables --remove-all-unused-imports
	black .

test: ## Run tests
test:
	pytest .

wipe-db: ## Wipe database and make a new one
wipe-db:
	python manage.py flush --noinput
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser --noinput

build: ## Build docker image
build:
	docker build -t $(DOCKER_NAME):$(DOCKER_TAG) -f docker/Dockerfile .

create: ## Create docker image
create: build
	docker create -it --name $(DOCKER_NAME) $(DOCKER_NAME):$(DOCKER_TAG)

start: ## Build and start docker image
start: build
	docker start $(DOCKER_NAME)

run: ## build, start and run docker image
run: start
	docker run -it $(DOCKER_NAME):$(DOCKER_TAG)

exec: ## build, start and exec into docker image
exec: start
	docker exec -it $(DOCKER_NAME) python