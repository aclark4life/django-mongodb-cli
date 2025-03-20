# django-mongodb-cli

## About

For testing [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend)
with [MongoDB's Django fork](https://github.com/mongodb-forks/django) and [third party libraries](#third-party-libraries).

> [!NOTE]
> [MongoDB's Django fork](https://github.com/mongodb-forks/django) is for *testing* [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend)
> and is not a requirement for *using* django-mongodb-backend. To use django-mongodb-backend, `pip install django-mongodb-backend` is all that is needed.

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

## Third party libraries

These 3rd party libaries are supported:

- django-allauth
- django-debug-toolbar
- django-filter
- django-rest-framework
- wagtail
