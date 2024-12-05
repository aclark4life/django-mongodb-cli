django-mongodb-cli
==================

For django-mongodb development.

Installation
------------

```bash
git clone https://github.com/aclark4life/django-mongodb-cli
cd django-mongodb-cli
python -m venv .venv
source .venv/bin/activate
python -m pip install .
django-mongodb-cli clone
django-mongodb-cli clone -i
django-mongodb-cli startproject --wagtail-mongodb
django-mongodb-cli migrate
django-mongodb-cli createsuperuser
django-mongodb-cli runserver
```
