Django filter
=============

Test suite settings
-------------------

Via ``dm repo test django-filter --show``

::

    {
        "apps_file": {
            "source": "settings/filter_apps.py",
            "target": "src/django-filter/tests/mongo_apps.py",
        },
        "clone_dir": "src/django-filter",
        "migrations_dir": {
            "source": "src/django-mongodb-templates/project_template/mongo_migrations",
            "target": "src/django-filter/tests/mongo_migrations",
        },
        "settings": {
            "test": {
                "source": "settings/filter_settings.py",
                "target": "src/django-filter/tests/settings.py",
            },
            "migrations": {
                "source": "settings/filter_settings.py",
                "target": "src/django-filter/tests/settings.py",
            },
            "module": {"test": "tests.settings", "migrations": "tests.settings"},
        },
        "test_command": "./runtests.py",
        "test_dir": "src/django-filter",
        "test_dirs": ["src/django-filter/tests"],
    }
