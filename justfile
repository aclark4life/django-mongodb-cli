default:
    echo 'Hello, world!'

# ---------------------------------------- django ----------------------------------------

[group('django')]
django-open:
    open http://localhost:8000
alias o := django-open

[group('django')]
django-serve:
    django-mongodb-cli runserver -m
alias s := django-serve

[group('django')]
django-startproject:
    mongo-orchestration stop
    mongo-orchestration start
    django-mongodb-cli startproject --delete
    django-mongodb-cli startproject --django-mongodb
    django-mongodb-cli install --app debug_toolbar
    django-mongodb-cli install --app home
    django-mongodb-cli install --url home.urls
    django-mongodb-cli install --app polls
    django-mongodb-cli install --app django_extensions
    django-mongodb-cli install --middleware debug_toolbar.middleware.DebugToolbarMiddleware
    django-mongodb-cli startui -d
    django-mongodb-cli startui
    django-mongodb-cli migrate -m
    django-mongodb-cli createsuperuser -m
alias startproject := django-startproject

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
