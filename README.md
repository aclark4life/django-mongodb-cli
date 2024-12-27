# django-mongodb-cli

For [django-mongodb](https://github.com/mongodb-labs/django-mongodb) development.

## Installation


### Clone repository

```bash
git clone https://github.com/aclark4life/django-mongodb-cli
cd django-mongodb-cli
```

### Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install `django-mongodb-cli` package

```bash
python -m pip install .
```

## Usage

### Clone development repositories

Defined in `pyproject.toml`.

```bash
django-mongodb-cli repo -c
```

### Run tests

Run the Django test suite in `src/django`.

```bash
django-mongodb-cli test
```

Run the Wagtail test suite in `src/wagtail`.

```bash
django-mongodb-cli test -w
```

### Start a new project

```bash
django-mongodb-cli startproject mysite
```

#### Run migrations, create superuser, start server

```bash
django-mongodb-cli migrate
django-mongodb-cli createsuperuser
django-mongodb-cli runserver
```
