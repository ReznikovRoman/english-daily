# English Daily
... \# TODO: add description

## Stack
[RabbitMQ](https://www.rabbitmq.com/), [Redis](https://redis.io/), [AWS SNS](https://aws.amazon.com/sns/)


## Configuration
Docker containers:
1. redis

docker-compose files:
 1. `docker-compose.yml` - for local development.

To run docker containers, you need to create a `.env` file in the root directory.

**`.env` example:**
```dotenv
ENV=.env
```

### Start project:

Locally:
```shell
docker compose build
docker compose up
```

## Development
Sync environment with `requirements.txt` / `requirements.dev.txt` (will install/update missing packages, remove redundant ones):
```shell
make sync-requirements
```

Compile requirements.\*.txt files (have to re-compile after changes in requirements.\*.in):
```shell
make compile-requirements
```

Use `requirements.local.in` for local dependencies; always specify _constraints files_ (-c ...)

Example:
```shell
# requirements.local.txt

-c requirements.txt

ipython
```

### Code style:
Configure pre-commit locally:

```shell
pre-commit install
```

Before pushing a commit run all linters:

```shell
make lint
```

Fix some mistakes:

```shell
make fix
```
