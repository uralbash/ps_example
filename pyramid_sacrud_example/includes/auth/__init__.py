#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Auth of user
"""
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import unauthenticated_userid
from ziggurat_foundations.models import groupfinder
from pyramid_sqlalchemy import Session

from .models import User


def get_user(request):
    """ The below line is just an example, use your own method of
    accessing a database connection here (this could even be another
    request property such as request.db, implemented using this same
    pattern).
    """

    userid = unauthenticated_userid(request)
    if userid is not None:
        """this should return None if the user doesn't exist in the database"""
        return Session.query(User).get(userid)


def add_auth(config):
    authn_policy = AuthTktAuthenticationPolicy('sosecret',
                                               callback=groupfinder,
                                               hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(get_user, 'user', reify=True)


def includeme(config):
    config.include('ziggurat_foundations.ext.pyramid.sign_in')
    config.include(add_auth)
    config.include('.routes')
    config.add_jinja2_search_path("templates")
    config.scan('.views')
