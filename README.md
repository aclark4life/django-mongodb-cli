# django-mongodb-cli

For django-mongodb development.

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

```bash
django-mongodb-cli clone
django-mongodb-cli clone -i
django-mongodb-cli startproject --wagtail-mongodb
django-mongodb-cli migrate
django-mongodb-cli createsuperuser
django-mongodb-cli runserver
```
