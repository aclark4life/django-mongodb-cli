# django-mongodb-cli

For [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) development and usage.

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

### Run Django and third party library test suites

#### Clone development repositories

Defined in `pyproject.toml`.

```bash
django-mongodb-cli repo --clone
```

#### Run the Django test suite in `src/django`.

```bash
django-mongodb-cli runtests
```

#### Run the Wagtail test suite in `src/wagtail`.

```bash
django-mongodb-cli runtests --wagtail
```

#### Run the Django Filter test suite in `src/django-filter`.

```bash
django-mongodb-cli runtests --django-filter
```

#### Run the Django Rest Framework test suite in `src/django-rest-framework`.

```bash
django-mongodb-cli runtests --django-rest-framework
```

### Start a new project

```bash
django-mongodb-cli startproject mysite
```

#### Run migrations

```bash
django-mongodb-cli migrate
```

#### Create a superuser

```bash
django-mongodb-cli createsuperuser
```

#### Start the development server

```bash
django-mongodb-cli runserver
```
