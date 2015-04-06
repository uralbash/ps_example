#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Routes for auth
"""


def includeme(config):
    config.add_route('login', '/login/')
    config.add_route('user_password_send',
                     'user/password/send/')
