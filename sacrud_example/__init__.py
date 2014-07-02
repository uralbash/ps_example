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
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import BeforeRender, subscriber
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config
from ziggurat_foundations.models import groupfinder

from .lib.common import get_user
from .models import Base, DBSession
from .models.auth import PERMISSION_VIEW
from .models.funny_models import MPTTPages
from .sacrud_config import get_sacrud_models
from .scripts import initializedb
from sacrud.common.pyramid_helpers import set_jinja2_silent_none
from sacrud_pages.common import get_pages_menu


def get_menu(**kwargs):
    return get_pages_menu(DBSession, MPTTPages, **kwargs)


@subscriber(BeforeRender)
def add_global(event):
    event['page_menu'] = get_menu


def add_routes(config):
    # Auth
    config.add_route('login', '/login/')
    config.add_route('user_password_send',
                     'user/password/send/')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Auth
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          root_factory='sacrud_example.models.auth.RootFactory',
                          session_factory=session_factory)
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder,
                                               hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_request_method(get_user, 'user', reify=True)
    config.set_default_permission(PERMISSION_VIEW)

    # Static
    config.add_static_view('static', 'static', cache_max_age=3600)
    add_routes(config)

    # Database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    conn = DBSession.connection()

    # initializedb
    initializedb.add_extension(engine, 'hstore')
    register_hstore(conn.engine.raw_connection(), True)
    ini_file = global_config['__file__']
    initializedb.main(argv=["init", ini_file])

    config.include('pyramid_jinja2')
    config.commit()
    config.add_jinja2_extension('jinja2.ext.with_')
    config.add_jinja2_search_path("sacrud_example:templates")

    # SACRUD
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings = config.registry.settings
    settings['sacrud.models'] = get_sacrud_models()

    # pyramid_elfinder
    config.include('pyramid_elfinder.connector')

    # sacrud_catalog
    config.include("sacrud_catalog")

    # sacrud_pages - put it after all routes
    config.set_request_property(lambda x: MPTTPages,
                                'sacrud_pages_model', reify=True)
    config.include("sacrud_pages")

    # change None in Jinja2 template on empty string
    set_jinja2_silent_none(config)
    config.scan()
    return config.make_wsgi_app()
