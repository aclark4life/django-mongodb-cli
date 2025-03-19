# django-mongodb-cli

For [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) development.

## About

This library automates configuration for testing
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

##### Clone, install, and test

```
dm repo clone django
dm repo install django
dm repo test django
```

##### List tests

```
dm repo test django -l
```

##### Run specific tests

```
dm repo test django queries_
```

#### 3rd Party Libraries

Same as above but with `django` replaced by 3rd party library name e.g. `django-filter`.

### Start project

```bash
dm startproject mysite
```
