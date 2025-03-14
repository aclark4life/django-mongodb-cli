default:
    echo 'Hello, world!'

install: pip-install git-clone dev-install
alias i := install

dev-install:
    dm repo install django-mongodb-backend
    dm repo install django-mongodb-extensions

# ---------------------------------------- git ----------------------------------------

[group('git')]
git-clone:
    dm repo clone django-mongodb-app
    dm repo clone django-mongodb-backend
    dm repo clone django-mongodb-extensions
    dm repo clone django-mongodb-project
    dm repo clone django-mongodb-templates

# ---------------------------------------- django ----------------------------------------

[group('django')]
django-open:
    open http://localhost:8000
alias o := django-open

[group('django')]
django-serve:
    dm runserver
alias s := django-serve

[group('django')]
django-migrate:
    dm manage migrate
alias m := django-migrate

[group('django')]
django-createsuperuser:
    dm createsuperuser
alias su := django-createsuperuser

# ---------------------------------------- mongodb ----------------------------------------

[group('mongodb')]
db-init:
    mongosh `echo ${MONGODB_URI}` --eval 'db.dropDatabase()'

# ---------------------------------------- python ----------------------------------------

# install python dependencies and activate pre-commit hooks
[group('python')]
pip-install: check-venv
    pip install -U pip
    pip install -e .
    pre-commit install

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

[group('npm')]
npm-install:
    npm install
