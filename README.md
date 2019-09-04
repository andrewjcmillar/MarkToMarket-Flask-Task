# MarkToMarket Flask Problem

This is a basic flask api which allows users to create and delete transactions associated with given projects.

## Requirements
- Python 3.7
- Pip (or alternatively use pipenv)
- A PostgreSQL database

Although the application has been created assuming the use of a PostgreSQL database, you can also use a sqllite database by updating an environment variable that is described below.

## Installation
Install required python packages with
```bash
pip install -r requirements.txt
```

Or alternatively if you prefer to use Pipenv Pipfiles have been provided

## Running the API
Once inside a python environment with the required dependencies simply use
```bash
flask run
```
To start the API at `localhost:5000/`

## Environment variables
| Variable | Default |
| -------- | :-------:
| PORT | 5000 |
| HOST | localhost |
| SQLALCHEMY_DATABASE_URI | 'postgresql://postgres:password@localhost:5432/postgres' |

Setting SQLALCHEMY_DATABASE_URI to a sqllite uri can allow you to run the app without a running postgres instance such as `sqlite:///foo.db`

## Improvements/Assumptions
- The model persistence part of the application is missing unit/integration tests, these should be added.
- It is assumed that all transactions must be associated with a project
- The user is currently just pulled from an request header, this would be requested with the auth method mentioned in the problem description
