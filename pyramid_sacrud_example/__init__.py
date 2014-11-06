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
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_sqlalchemy import Session as DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['ini_file'] = global_config['__file__']
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          root_factory='.includes.auth.security.RootFactory',
                          session_factory=session_factory)

    config.include('pyramid_sqlalchemy')
    config.include('pyramid_jinja2')
    config.include('.includes')
    config.include('.initialize')

    # pyramid_elfinder
    config.include('pyramid_elfinder')

    # pyramid_sacrud_gallery
    config.include('pyramid_sacrud_gallery')

    # sacrud_catalog
    conn = DBSession.connection()
    dialect = conn.dialect.name.lower()
    if dialect == 'postgresql':
        config.include("pyramid_sacrud_catalog")

    # sacrud_pages - put it after all routes
    config.include("pyramid_sacrud_pages")

    # Make WSGI application
    config.scan('.views')
    return config.make_wsgi_app()
