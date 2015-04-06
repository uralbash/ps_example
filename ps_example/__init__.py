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

from pyramid_sacrud.includes.assets import add_jinja2_silent_none

from .includes.auth.security import RootFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['ini_file'] = global_config['__file__']
    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        session_factory=session_factory_from_settings(settings))

    config.include('pyramid_sqlalchemy')
    config.include('pyramid_jinja2')
    config.include('pyramid_elfinder')
    config.include('.initialize')
    config.include('.includes')
    app = config.make_wsgi_app()
    add_jinja2_silent_none(config)
    return app
