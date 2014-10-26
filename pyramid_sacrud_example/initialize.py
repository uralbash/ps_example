#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Init DB
"""
from pyramid_sqlalchemy import Session as DBSession

from .scripts import initializedb


def includeme(config):
    settings = config.registry.settings
    # init Postgres
    engine = DBSession.bind.engine
    conn = DBSession.connection()
    dialect = conn.dialect.name.lower()
    if dialect == 'postgresql':
        from psycopg2.extras import register_hstore
        initializedb.add_extension(engine, 'hstore')
        register_hstore(engine.raw_connection(), True)

    # initializedb
    if settings.get('sacrud.debug_reload_database', False):
        initializedb.main(argv=["init", settings['ini_file']])

    config.add_jinja2_extension('jinja2.ext.with_')
    config.add_jinja2_search_path("pyramid_sacrud_example:templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
