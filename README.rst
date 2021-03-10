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


TODOS
-------------
- units tests for **RequestSchedule** model's **schedule** method
- units tests for **RequestSchedule** model's **save** method
- units tests for **make_request** services method
- units tests for **process_request** task
- prevent IPv4 & IPv6 unsafe networks being adding as a url host
    - `IPv4 & IPv6 unsafe networks <https://github.com/crunch-io/requests-safe#ipv4-unsafe-networks>`_
