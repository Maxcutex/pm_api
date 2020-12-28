# Profile Manager API
PM Api is a python solution cloned from Vessel Api. It handles the api backend solution for Profile Manager


## Setup

Run: `$ pip install -r requirements.txt` and `pre-commit install` for linting

This will pull and install all vessel dependencies into the current or active virtual environment. Copy the content of
`.env_sample` into `.env` and set proper environment variables.

On the prompt execute the following
```
export $(cat .env)
```


Execute the following code to seed the database
```
flask seed-database
```

Execute the following command in the terminal to start the redis server
```
bash redis.sh
```

Execute the following code to migrate all data tables/object
```
python run.py db migrate
```

## Start Server
In the `project_root` with environment activated,

Run: `$ python run.py runserver`

Open your browser and enter `http://127.0.0.1:5000/api/v1/`



## vessel CLI Tool
Vessel comes with a small CLI tool to help generate commmonly used utilities like `models`, `repositories`, `blueprints`,
 `controllers`, `tests` and `factories`

 Example:
 ```
 Usage: python vessel.py

 Command Line Arguments
    make:model name eg. python vessel.py make:model user [--with_repo [_controller] ]
	make:repo name eg. python vessel.py make:repo user
	make:blueprint name eg. python vessel.py make:blueprint vendors [--url_prefix=vendors]
	make:controller name eg. python vessel.py make:controller user
	make:test name eg python vessel.py make:test test_user_repo - This command will parse paths and write to the valid paths provided
	make:factory name eg python vessel.py make:factory role
    show_routes eg python vessel.py show_routes
 ```

## Tests
Ofcourse there's support for testing using pytest. To create a new test suite, simply run the make:test command on the CLI.

eg. `$ python vessel.py make:test integration/endpoints/test_user_endpoints`

To run tests `$ python -m pytest`

## Folder and Code Structure
```
|-- project_root
    |-- app/
        |-- blueprints/
            |-- base_blueprint.py
        |-- controllers/
            |-- __init__.py
            |-- base_controller.py
        |-- models/
            |-- __init__.py
            |-- base_model.py
        |-- repositories/
            |-- __init__.py
            |-- base_repo.py
        |-- utils/
            |-- __init__.py
            |-- auth.py
            |-- security.py
        |-- __init__.py
        |-- test_db.db
    |-- config/
        |-- __init__.py
        |-- env.py
    |-- factories
        |-- __init__.py
    |-- migrations
    |-- tests
        |-- integration/
            |-- endpoints/
                |-- __init__.py
                |-- test_dummy_endpoints.py
            |-- __init__.py
        |-- unit
            |-- repositories/
            |-- test_auth.py
        |-- __init__.py
        |-- base_test_case.py
    |-- .env_sample
    |-- .gitignore
    |-- LICENSE
    |-- Procfile
    |-- pytest.ini
    |-- README.md
    |-- requirements.txt
    |-- run.py
    |-- vessel.py
```

### Quick Start
Running the backend application in docker with make.

Starts all services including Postgres, Redis and the api at http://localhost:4070.

```
make up
```

Rebuild and launch all containers including api at http://localhost:4070.
```
make buildup
```

Clean code and stop any docker container.
```
make stop
```

Clean code and destroy docker processes, images and volumes.
```
make destroy
```

Destroy docker processes, images and volumes.
```
make destroy-all
```

Clean code and destroy docker processes.
```
make down
```

Download docker images in parallel.
```
make pull
```

Connect to the shell inside the api container.
```
make shell
```

Connect to the shell inside the Postgres container.
```
make shell-db
```

Connect to the shell inside the Redis container.
```
make shell-redis
```

Remove all compiled files, coverage. 'sudo' maybe needed.
```
make clean
```

Seed database from seed data files.
```
make seed-database
```

Compile requirements.txt from requirements.in and build the images for the api service.
```
make pip-compile
```

Compile requirements.txt from requirements.in upgrading the packages and build the images for the api service.
```
