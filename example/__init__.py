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
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config
from ziggurat_foundations.models import groupfinder

from example.lib.common import get_user
from example.models import Base, DBSession
from example.models.auth import (Company, ExternalIdentity, Group,
                                 GroupPermission, GroupResourcePermission,
                                 PERMISSION_VIEW, Resource, User, UserGroup,
                                 UserPermission, UserResourcePermission)
from example.models.funny_models import (TestAllTypes, TestBOOL,
                                         TestCustomizing, TestDND, TestFile,
                                         TestHSTORE, TestTEXT, TestUNION,
                                         WidgetPosition)
from example.scripts import initializedb
from sacrud_pages.models import MPTTPages


def add_routes(config):
    config.add_route('home', '/')

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
                          root_factory='example.models.auth.RootFactory',
                          session_factory=session_factory)
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder,
                                               hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_request_method(get_user, 'user', reify=True)
    config.set_default_permission(PERMISSION_VIEW)

    # Columns and positions start at 0
    sacrud_models = {
        'Postgres': {
            'tables': [TestHSTORE],
        },
        '': {
            'tables': [TestTEXT, TestBOOL, TestDND, TestUNION, TestFile],
            'column': 0,
            'position': 1,
        },
        'Just for fun': {
            'tables': [TestAllTypes],
            'column': 1,
            'position': 0,
        },
        'Customizing example': {
            'tables': [TestCustomizing],
            'column': 1,
            'position': 1,
        },
        'Pages': {
            'tables': [MPTTPages],
            'column': 2,
            'position': 0,
        },
        'Auth': {
            'tables': [Company, Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'column': 2,
            'position': 1,
        },
    }

    # sacrud_models = {
    #     'Postgres': [TestHSTORE],
    #      '': [TestTEXT, TestBOOL, TestDND, TestUNION, TestFile],
    #      'Just for fun': [TestAllTypes],
    #      'Customizing example': [TestCustomizing],
    #      'Pages': [MPTTPages],
    #      'Auth': [Company, Group, GroupPermission, UserGroup,
    #               GroupResourcePermission, Resource, UserPermission,
    #               UserResourcePermission, User, ExternalIdentity]
    # }

    # Database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    conn = DBSession.connection()

    initializedb.add_extension(engine, 'hstore')
    register_hstore(conn.engine.raw_connection(), True)
    ini_file = global_config['__file__']
    initializedb.main(argv=["init", ini_file], sacrud_models=sacrud_models)

    # pyramid_jinja2 configuration
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("example:templates")

    # pyramid_elfinder
    config.include('pyramid_elfinder.connector')

    # SACRUD
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings = config.registry.settings
    settings['sacrud.models'] = sacrud_models

    config.add_static_view('static', 'static', cache_max_age=3600)

    add_routes(config)
    config.scan()

    # sacrud_pages - put it after all routes
    config.include("sacrud_pages")

    return config.make_wsgi_app()
