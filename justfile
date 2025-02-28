default:
    echo 'Hello, world!'

install: pip-install git-clone dev-install
alias i := install

alias u := git-update

dev-install:
    django-mongodb-cli repo install django
    django-mongodb-cli repo install django-filter
    django-mongodb-cli repo install django-mongodb-backend
    django-mongodb-cli repo install django-rest-framework

# ---------------------------------------- git ----------------------------------------
[group('git')]
git-clone:
    django-mongodb-cli repo clone django
    django-mongodb-cli repo clone django-filter
    django-mongodb-cli repo clone django-mongodb-backend
    django-mongodb-cli repo clone django-mongodb-project
    django-mongodb-cli repo clone django-project-templates
    django-mongodb-cli repo clone django-rest-framework

git-update:
    django-mongodb-cli repo update django
    django-mongodb-cli repo update django-filter
    django-mongodb-cli repo update django-mongodb-backend
    django-mongodb-cli repo update django-mongodb-project
    django-mongodb-cli repo update django-project-templates
    django-mongodb-cli repo update django-rest-framework

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
