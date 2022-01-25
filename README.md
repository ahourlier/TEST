# Urbanis - OSLO - Backend - Guide

This is the repository of Urbanis OSLO backend application.

## Environments and configuration
The app configuration rests in app/config.py file.
There are 3 different configurations:
- dev : Flask will run in debug mode. Testing mode is off.
- test : Flask will run in debug mode and in testing mode.
- prod : Flask will run in production mode. Debug mode is off and Testing mode is off.

/!\ Do not confuse the Flask application debug mode and the flask development server debug mode (see next section)

### dotenv 
Some configuration settings (like which configuration to use) use environment variables.
These environments variables can be set up directly in a .env file at the root for the repository.

Example of basic .env file for local environment:
```
DEV_SERVER=True
FLASK_ENV=dev
IS_LOCAL=True
DB_IP_ADDRESS=localhost
DB_PORT=5432
DB_NAME=oslo
DB_USER=postgres
DB_PASSWORD=root
TECHNICAL_ACCOUNT_EMAIL={{DELEGATED_ACCOUNT}}
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:root@localhost:5432/oslo
GOOGLE_CLOUD_PROJECT=app-oslo-dev
QUEUES_LOCATION=europe-west1
TRANSLATION_URL="https://storage.googleapis.com/app-oslo-dev-locales/oslo-fr-FR.json"
APPLICATION_MEMBERS_GOOGLE_GROUP="{{GOOGLE_GROUP_EMAIL}}"
API_URL="http://localhost:5000"
GROUP_NAME_ENV_PREFIX="{{SOME NAME PREFIX}}"
GROUP_EMAIL_ENV_PREFIX="{{SOME EMAIL PREFIX}}"
GSUITE_DOMAIN="{{GOOGLE_WORKSPACE_DOMAIN}}"
APPLICATION_ADMINS_GOOGLE_GROUP="{{A GOOGLE GROUP CREATED BEFORE ON WORKSPACE}}"
```

This will automatically setup the proper configuration at runtime.

FLASK_ENV is an environment variable with the name of the Flask configuration to enable (dev,test or prod)
If this environment variable is not set, the default configuration is *test*.

## Run the app
From root directory:
```bash
flask run
```
or
```bash
python main.py
```

The only difference between both commands is that the second one will run the development server with debug mode enabled if the environment variable DEV_SERVER is set to any value (you can use .env file or set it explicitely).

The _main.py_ file can be used as the entrypoint for running the application on Google App Engine.


## Run unit tests
From the root directory:
```bash
pytest app
```

To run with coverage
```bash
pytest --cov=app --cov-report=html --cov-config=.coveragerc app
```

## Database & migrations

In order to test the API, you need to configure a local db.
One way to do that is using docker-compose.

- Paste the following configurations into a file named "docker-compose.yml" in a directory out of the project directory :

```
version: '3.1'

services:

  postgres-development:
    image: postgres
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    restart: always
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: oslo
    ports:
      - 5432:5432
```

- You should modify the password.
- Then run : 
```docker-compose up -d```
(You can check that the container is running properly with ```docker ps```)

- Modify your .env file with the correct DB_IP_ADDRESS (probably "localhost"), DB_PORT, DB_NAME, DB_USERNAME and DB_PASSWORD
- Adjust your db by creating a new schema named "core"
- Run ````flask db upgrade```` to get updated tables


Database migrations are done with Flask-Migrate plugin.
Each time you modified SQL Alchemy models (or created new ones), run :
````
flask db migrate
flask db upgrade
````


### Configuration
Update _app/migrations/env.py_ file and import all models:

```python
from app.sample.users.model import User
# here import other models

from flask import current_app
``` 

### Generate migration file
Run
```bash
flask db migrate
```

This will generate a migration file in _app/migrations/versions_

### Apply migration to your db
To apply all migrations not already performed

```bash
flask db upgrade
```


## Cloud Task emulator
Cloud Task is used on this project in order to create Drives, Google Groups and such.

We use this [emulator](https://pypi.org/project/gcloud-tasks-emulator/).

To install it, simply run this command in your venv: 
```shell
pip install gcloud-tasks-emulator
```

And to run it, please run:
```shell
gcloud-tasks-emulator start --port=9090
```

## Cloud Functions
A Cloud Function is used to react to changes in Firestore.
De deploy it, move to folder `trigger_functions/` and run:

```shell
gcloud functions deploy on_update --project app-oslo-dev --entry-point on_update --runtime python38 --trigger-event "providers/cloud.firestore/eventTypes/document.update" --trigger-resource "projects/app-oslo-dev/databases/(default)/documents/thematiques/{thematiqueId}/steps/{stepId}" --region europe-west1

```
