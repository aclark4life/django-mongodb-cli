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

### Install package

```bash
python -m pip install .
```

## Usage

### Clone and install development repositories

```bash
django-mongodb-cli clone
```

### Run tests

```bash
django-mongodb-cli runtests
```

### Start a new project

```bash
django-mongodb-cli startproject mysite
```

> [!NOTE]
> Start MongoDB before running the following commands.

### Run migrations, create superuser, and start server

```bash
django-mongodb-cli migrate
django-mongodb-cli createsuperuser
django-mongodb-cli runserver
```
