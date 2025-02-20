# django-mongodb-cli

For [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) development.

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
just install
```

## Usage

### Run Django and third party library test suites

#### Clone development repositories

Defined in `pyproject.toml`.

```bash
django-mongodb-cli repo clone django-mongodb-backend
```

#### Install development repositories

```bash
django-mongodb-cli repo install django-mongodb-backend
```

#### Run the Django test suite in `src/django`.

This is the default behavior.

```bash
django-mongodb-cli runtests
```

Third party library test suites can be run by passing the appropriate flag.

##### Run the Wagtail test suite in `src/wagtail`.

```bash
django-mongodb-cli runtests --wagtail
```

##### Run the Django Filter test suite in `src/django-filter`.

```bash
django-mongodb-cli runtests --django-filter
```

##### Run the Django Rest Framework test suite in `src/django-rest-framework`.

```bash
django-mongodb-cli runtests --django-rest-framework
```

##### Run the Django Debug Toolbar test suite in `src/django-debug-toolbar`.

```bash
django-mongodb-cli runtests --django-debug-toolbar
```

##### Run the Django Allauth test suite in `src/django-allauth`.

```bash
django-mongodb-cli runtests --django-allauth
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
