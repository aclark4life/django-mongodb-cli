==================
Django MongoDB CLI
==================

.. note::

    This documentation is for developers of third party libraries that want to integrate with Django MongoDB Backend.

Third party library support
===========================

Support for third party libraries is determined via the following:

- Test suites
- Project integrations
- Known limitations

Test suites
-----------

For each third party library that is supported, the following tasks are performed:

- The test suite is configured to run with Django MongoDB Backend

  - Evaluate test runner configuration
    - Replace with ``pytest`` if possible

  - Update django settings
  - Update or disable migrations

- The test suite is run with Django MongoDB Backend
- The test results are recorded
- The test suite is updated

  - Replace static primary key references with dynamic references or static ``ObjectId`` references


Project integrations
--------------------

Known limitations
-----------------

- URL configuration
