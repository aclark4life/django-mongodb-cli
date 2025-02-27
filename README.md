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

### Install `django-mongodb-cli` package and dependencies

```bash
just install
```

## Usage

### Run Django and third party library test suites

#### Run the Django test suite in `src/django`.

```bash
django-mongodb-cli repo clone django
django-mongodb-cli repo install django
django-mongodb-cli repo test django
```

### Start a new project

```bash
django-mongodb-cli startproject mysite
```
