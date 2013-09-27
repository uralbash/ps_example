#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts import initializedb
from psycopg2.extras import register_hstore
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    TestHSTORE,
    TestTEXT,
    TestBOOL,
    TestDND,
    TestUNION,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    conn = DBSession.connection()
    register_hstore(conn.engine.raw_connection(), True)
    initializedb.main(argv=["init", "development.ini"])

    # pyramid_jinja2 configuration
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("example:templates")
    env = config.get_jinja2_environment()

    # if variable is None print '' instead of 'None'
    def _silent_none(value):
        if value is None:
            return ''
        return value
    env.finalize = _silent_none

    # Добавляет sacrud и модели для него
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings = config.registry.settings
    settings['sacrud_models'] = (TestHSTORE, TestTEXT, TestBOOL, TestDND,
                                 TestUNION)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.scan()
    return config.make_wsgi_app()
