# django-mongodb-cli

For [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) development.

## About

This library automates most of the setup for testing django-mongodb-backend with Django and third party packages.

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

### Run tests

```
django-mongodb-cli repo test django
```

### Start a new project

```bash
django-mongodb-cli startproject mysite
```
