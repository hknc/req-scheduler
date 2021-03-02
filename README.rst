Request Scheduler
==================

A simple tool that lets you schedule REST requests for a given point in time in the future.


Stack
-------------
  - Django
  - PostgreSQL
  - Redis
  - Celery Worker (for background tasks)
  - Celery Beat (for scheduling)

Running Locally With Docker
-------------

This brings up the stack for local development::

    $ docker-compose -f local.yml up

To run in a detached mode::

    $ docker-compose -f local.yml up -d

To run commands::

    $ docker-compose -f local.yml run --rm django python manage.py migrate


Online Demo
-------------

.. _`Demo app deployed to heroku -> https://req-scheduler.herokuapp.com/`: https://req-scheduler.herokuapp.com/
