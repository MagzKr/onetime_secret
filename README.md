# Onetime secret

Service for transmitting encrypted messages.

# Install dependencies and run app for local development:
```shell
pip install poetry
poetry install
```
Create .env file based on [.env.example](.env.example)
```shell
docker-compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```
App will be launched on http://127.0.0.1:8000.

# Run tests:
```shell
 ENVIRONMENT=PYTEST pytest
```

# Run app in docker container:
```shell
docker-compose -f docker-compose.dev.yml up -d
```
App will be launched on http://127.0.0.1.
