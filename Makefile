TEST_DATABASE_URL=postgres://postgres@localhost:5466/postgres

# Print this help message
help:
	@echo
	@awk '/^#/ {c=substr($$0,3); next} c && /^([a-zA-Z].+):/{ print "  \033[32m" $$1 "\033[0m",c }{c=0}' $(MAKEFILE_LIST) |\
        sort |\
        column -s: -t |\
        less -R

# Sort python files
isort:
	@echo "--- 🐍 Isorting 🐍 ---"
	poetry run isort app

# Ruffing python files
ruff:
	@echo "--- 🐕 Ruffing 🐕 ---"
	poetry run ruff app

# Format python files
black:
	@echo "--- 🎩 Blacking 🎩 ---"
	poetry run black app --check

# Typecheck python files
mypy:
	@echo "--- ⚡ Mypying ⚡ ---"
	poetry run mypy

# Run all linters
lint: isort ruff black mypy

postgres:
	touch .env.dev
	docker compose up -d db
	until psql $(TEST_DATABASE_URL) -c 'select 1'; do sleep 2; done

migrate: postgres
	docker compose run worker python manage.py migrate

migrations: postgres
	docker compose run worker python manage.py makemigrations

# Run tests in ci. Including setting up docker
ci/test: postgres
	@echo "--- 💃 Testing 💃 ---"
	DATABASE_URL=$(TEST_DATABASE_URL) poetry run py.test --cov app

# Run all tests
test:
	@echo "--- 💃 Testing 💃 ---"
	poetry run py.test --cov app

# Test and lint in CI
# ci: ci/test lint
ci: lint