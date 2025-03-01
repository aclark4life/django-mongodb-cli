# django-mongodb-cli

For [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) development.

## About

This library automates most of the setup for testing
[django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend)
with [MongoDB's Django fork](https://github.com/mongodb-forks/django)
and third party libraries.

> [!NOTE]
> MongoDB's Django fork is for testing only and is not a requirement for using
> django-mongodb-backend.

## Installation

```bash
git clone https://github.com/aclark4life/django-mongodb-cli
cd django-mongodb-cli
python -m venv .venv
source .venv/bin/activate
just install
```

## Usage

### Run tests

#### Django

```
django-mongodb-cli repo clone django
django-mongodb-cli repo install django
django-mongodb-cli repo test django
```

### Start project

```bash
django-mongodb-cli startproject mysite
```
