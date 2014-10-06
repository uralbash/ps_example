*******
Install
*******

**Require:**

* fortune

Install fortune:

:code:`sudo apt-get install fortune`

.. note::
    For Debian like pkg system.

Clone project to local machine:

:code:`git clone git@github.com:uralbash/pyramid_sacrud_example.git`

SQLite support
==============

Initialize project:

:code:`initialize_example_db development.ini`

Run protject:

:code:`pserve development.ini http_port=8000`

Folow to `<http://localhost:8000/admin/>`_

PostgreSQL support
==================

PostgreSQL gives you additional tables with his special types (ARRAY, HSTORE, JSON, UUID, etc)

**Require:**

* PostgreSQL
* psycopg2

Copy `development_pg.ini` to `development_local.ini`, edit postgres connection line and create db in PostgreSQL.

Initialize project:

:code:`initialize_example_db development_local.ini`

Run protject:

:code:`pserve development_local.ini http_port=8000`

Folow to `<http://localhost:8000/admin/>`_

And see

.. image:: _static/img/index.png
