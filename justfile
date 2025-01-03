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

[group('npm')]
npm-install:
    npm install
