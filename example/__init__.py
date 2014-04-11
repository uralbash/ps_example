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
from pyramid.view import view_config
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config
from ziggurat_foundations.models import groupfinder

from example.lib.common import get_user
from example.models import Base, DBSession
from example.models.auth import (Company, ExternalIdentity, Group,
                                 GroupPermission, GroupResourcePermission,
                                 PERMISSION_VIEW, Resource, User, UserGroup,
                                 UserPermission, UserResourcePermission)
from example.models.funny_models import (Pages, TestAllTypes, TestBOOL,
                                         TestCustomizing, TestDND, TestFile,
                                         TestHSTORE, TestTEXT, TestUNION)
from example.scripts import initializedb


@view_config(route_name='filebrowser', renderer='templates/filebrowser.jinja2')
def fileBrowser(request):
    return {}


def add_routes(config):
    config.add_route('home', '/')
    config.add_route('filebrowser', '/image/filebrowser')  # for tinymce img

    # Auth
    config.add_route('login', '/login/')
    config.add_route('user_password_send',
                     'user/password/send/')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    conn = DBSession.connection()
    register_hstore(conn.engine.raw_connection(), True)
    ini_file = global_config['__file__']
    initializedb.main(argv=["init", ini_file])

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
                                 'Auth': [Company, Group, GroupPermission,
                                          UserGroup, GroupResourcePermission,
                                          Resource, UserPermission,
                                          UserResourcePermission, User,
                                          ExternalIdentity]
                                 }

    config.add_static_view('static', 'static', cache_max_age=3600)

    add_routes(config)
    config.scan()

    return config.make_wsgi_app()
