# Pyhon Celery demo

This project simply demonstrate how to use the [Celery Task Queue](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) to create a distributed task environment.

This is just a Demo to play little bit with Celery it is not intended to use in production.

Stack:

- [Python3](https://www.python.org/) (package manager: [Poetry](https://python-poetry.org/))
- [Celery](https://docs.celeryq.dev/en/stable/index.html) (broker: [RabbitMQ](https://rabbitmq.com/), backend: [MongoDB](https://www.mongodb.com/), ui: [Flower](https://flower.readthedocs.io/en/latest/))
- [Flask 3](https://flask.palletsprojects.com/) (wsgi: [Gunicorn](https://gunicorn.org/))
- [Docker](https://www.docker.com/)

## Setup and run

Install Docker Engine or Docker Desktop. Minimum Docker Engine version: `24.0.7`. [Install Docker](https://docs.docker.com/engine/install/).

Copy `example.env` to `.env`. Docker Compose will use this env file. `example.env` has a good defaults but maybe you have to choose different `*PUBLIC_PORT` numbers if you already use these ports. Check the `.env` file for details.

Start the docker environment from the root dir of the project:

```bash
docker compompose up --detach
```

Issue a POST request to the `/api/tasks/fibonacci` endpoint:

```http
POST http://localhost:8000/api/tasks/fibonacci
Content-Type: application/json

{
  "n": 10
}
```

E.g. with the following curl command:

```bash
curl --request POST \
  --url http://localhost:8000/api/tasks/fibonacci \
  --header 'content-type: application/json' \
  --data '{"n": 10}'
```

You should get a `200 OK` response with the task's ID.

If you changed the `HTTP_SERVER_PUBLIC_PORT` env variable in from `8000` to something else use that port number in the curl/http request.

## Usage

### HTTP server endpoints

A [Flask HTTP server](https://flask.palletsprojects.com/en/3.0.x/) is configured to schedule tasks and execute management requests for Celery. It has the following endpoints.

#### POST /api/tasks/fibonacci

Calculates the nth fibonacci number in a Celery Worker. 

Arguments (JSON Body): 
- n: the nth fibonacci number to calculate. It should be a number.

Response:
- 200 OK, with the argument and the Celery task ID.

Example: 

```http
POST http://localhost:8000/api/tasks/fibonacci
Content-Type: application/json

{
  "n": 10
}
```

#### POST /api/tasks/long-add

Adds two numbers and waits a minute (to simulate a long running tasks).

Arguments (JSON Body):
- a: the first operand, it should be a number.
- b: the second operand, it should be a number.

Response:
- 200 OK, with the argument and the Celery task ID.

Example: 

```http
POST http://localhost:8000/api/tasks/long-add
Content-Type: application/json

{
  "a": 4,
  "b": 5
}
```

#### GET /api/tasks/{task_id}

Get details of the currently executing task using the Celery API. Only the started or received tasks are listed.

Arguments (path parameter)
- task_id: The ID received in the POST /api/tasks/{task_name}'s response.

Response:
- The task's details from Celery API.

Example:
```http
GET http://localhost:8000/api/tasks/d733ed00-304b-4439-85d3-b2ad980ad6cf
```

### Using the VSCode REST Client

If you are using VSCode and installed the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension, the `requests.http` file contains the configured requests.

### Accessing Flower

[Flower](https://flower.readthedocs.io/en/latest/) is a UI to monitor the Celery Task Queue.

You can reach it by default on the `http://localhost:8001` URL. The port number can be configured in the `.env` file (`CELERY_UI_PUBLIC_PORT`).

### Accessing MonogoDB

A backend can be configured for Celery to store the task's results. For this project a MongoDB backend is configured.

You can reach the running MongoDB instance with any MongoDB client, e.g. with [MongoDB Compass](https://www.mongodb.com/products/tools/compass) from outside.

The default connection string from outside of the docker environment is: 

```
mongodb://guest:secret@localhost:27017/?authMechanism=DEFAULT&authSource=admin
```

If you change the `MONGODB_PUBLIC_PORT`, `MONGODB_USER` or `MONGODB_PASSWORD` change the connection string according to that.

### Accessing the Rabbit MQ management interface

Rabbit MQ has a built in management interface. You can reach it from the browser at `http://localhost:8002` by default. The default user is `guest` the default password `secret`.

You can change these defaults with the `RABBITMQ_UI_PUBLIC_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD` env variables in the `.env` file.  

### Add more workers

If you scale up the `worker` service in docker compose they are automatically added to Celery.

```bash
docker compose up --detach --scale woker=3
```

## Development

### Project structure

- `./src`: the base python package
- `./src/server.py`: the Flask HTTP server
- `./src/worker..py`: the Celery workers
- `./src/config.py`: Reading some env variables to a configuration.
- `./src/gunicorn.conf.py`: A Gunicorn WSGI server config to run the Flask server in the container. It reads also env variables.
- `./Dockerfile`: Multistage Docker build file for the server and the worker containers.
- `docker-compose.yml`: All services with server and worker to run the environment.
- `requests.http`: VSCode REST Client's example HTTP requests.- `pyproject.toml`: Poerty config file, contains the dependency versions.

### Docker

Unfortunately the docker environment is not prepared for convenient development. You can rebuild the docker environment each time if you modify the source code with the following command:

```bash
docker compose build
```

Or you can run the server and the worker processes outside of the docker environment, while using the docker env to provide the db and broker services.

### Docker Services

- `server`: It is an HTTP server, it provides the HTTP endpoints to schedule the Celery tasks. It needs an access to the broker.
- `worker`: It starts a Celery wroker to execute the scheduled tasks. It should be connected to the `db` and the `broker` services. It is scalable.
- `db`: A MongoDB service used as a result backend for Celery. The task's results are stored in this DB.
- `broker`: Provides a RabbitMQ queue for Celery to distribute the tasks among the workers.
- `celery-ui`: Hosts Flower, Celery ready made UI for interrogation and basic management.

### Running outside of the docker environment

This python projec is based on [Poetry](https://python-poetry.org/).

Install the dependencies in a virtual environment:

```bash
poetry install
```

You can execute command within the virtual environment with `poetry run`. You need also define the environment variables for this execution (check `config.py` and gunicorn.conf.py).

Provide env variables in a linux environment:

```bash
export $(dev.env | xargs) && poetry run {command}
```

You can start the different service with the usual commands:

Flask HTTP Server:

```bash
poetry run flask --app src.server run
```

Celery Worker:

```bash
poetry run celery --app src.worker worker --loglevel INFO --events
```



