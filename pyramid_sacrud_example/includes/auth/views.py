#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Views for login, logout
"""
from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPSeeOther
from pyramid.security import authenticated_userid, NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ziggurat_foundations.ext.pyramid.sign_in import (ZigguratSignInBadAuth,
                                                      ZigguratSignInSuccess,
                                                      ZigguratSignOut)


@view_config(context=ZigguratSignInSuccess, permission=NO_PERMISSION_REQUIRED)
def sign_in(request):
    return HTTPFound(location='/',
                     headers=request.context.headers)


@view_config(context=ZigguratSignInBadAuth, permission=NO_PERMISSION_REQUIRED)
def bad_auth(request):
    # action like a warning flash message on bad logon
    return HTTPFound(location=request.route_url('login'),
                     headers=request.context.headers)


@view_config(context=ZigguratSignOut, permission=NO_PERMISSION_REQUIRED)
def sign_out(request):
    return HTTPFound(location='/',
                     headers=request.context.headers)


@view_config(route_name='login', renderer='/auth/login.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def login(request):
    return {}


@view_config(route_name='user_password_send', permission=NO_PERMISSION_REQUIRED)
def password_send(request):
    return HTTPFound(location='/')


@view_config(context=HTTPForbidden, renderer='403.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def forbidden_view(request):
    if authenticated_userid(request) is None:
        location = request.route_url('login', _query={'came_from': request.path})
        return HTTPSeeOther(location)

    request.response.status = 403
    return {
        # params required for rendering 403.jinja2
    }
