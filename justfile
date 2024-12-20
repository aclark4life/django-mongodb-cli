default:
    echo 'Hello, world!'

# ---------------------------------------- django ----------------------------------------

[group('django')]
django-open:
    open http://localhost:8000
alias o := django-open

[group('django')]
django-serve:
    django-mongodb-cli runserver
alias s := django-serve

[group('django')]
django-startproject:
    django-mongodb-cli startproject --delete
    django-mongodb-cli startproject --django
    django-mongodb-cli install --app debug_toolbar
    django-mongodb-cli install --app home
    django-mongodb-cli install --url home.urls
    django-mongodb-cli install --app polls
    django-mongodb-cli install --app django_extensions
    django-mongodb-cli install --middleware debug_toolbar.middleware.DebugToolbarMiddleware
    django-mongodb-cli migrate
    django-mongodb-cli createsuperuser

# ---------------------------------------- python ----------------------------------------

# install python dependencies and activate pre-commit hooks
[group('python')]
pip-install: check-venv
    pip install -U pip
    pip install -e .
    pre-commit install
alias i := pip-install

# ensure virtual environment is active
[group('python')]
check-venv:
    #!/bin/bash
    PYTHON_PATH=$(which python)
    if [[ $PYTHON_PATH == *".venv/bin/python" ]]; then
      echo "Virtual environment is active."
    else
      echo "Virtual environment is not active."
      exit 1
    fi

[group('wagtail')]
wagtail-startproject:
    django-mongodb-cli startproject --delete
    django-mongodb-cli startproject --wagtail
    django-mongodb-cli install --app debug_toolbar --settings-path backend/settings/base.py
    django-mongodb-cli install --app polls --settings-path backend/settings/base.py
    django-mongodb-cli install --app django_extensions --settings-path backend/settings/base.py
    django-mongodb-cli install --middleware debug_toolbar.middleware.DebugToolbarMiddleware
    django-mongodb-cli migrate
    django-mongodb-cli createsuperuser
