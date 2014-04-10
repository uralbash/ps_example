#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Main for example
"""
from psycopg2.extras import register_hstore
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from example.scripts import initializedb

from .models import (Base, DBSession, Pages, TestAllTypes, TestBOOL,
                     TestCustomizing, TestDND, TestFile, TestHSTORE, TestTEXT,
                     TestUNION)


@view_config(route_name='filebrowser', renderer='templates/filebrowser.jinja2')
def fileBrowser(request):
    return {}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, session_factory=session_factory)
    conn = DBSession.connection()
    register_hstore(conn.engine.raw_connection(), True)
    ini_file = global_config['__file__']
    initializedb.main(argv=["init", ini_file])

    # pyramid_jinja2 configuration
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("example:templates")

    # SACRUD
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings = config.registry.settings
    settings['sacrud.models'] = {'Postgres': [TestHSTORE],
                                 '': [TestTEXT, TestBOOL, TestDND, TestUNION,
                                      TestFile],
                                 'Just for fun': [TestAllTypes],
                                 'Customizing example': [TestCustomizing],
                                 'Pages': [Pages],
                                 }

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('filebrowser', '/image/filebrowser')  # for tinymce img
    config.scan()
    return config.make_wsgi_app()
