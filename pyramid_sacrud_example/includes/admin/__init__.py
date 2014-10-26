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
from .config import get_sacrud_models
from pyramid_sqlalchemy import Session as DBSession


def includeme(config):
    config.add_jinja2_search_path("templates")
    config.include('pyramid_sacrud', route_prefix='/admin')
    settings = config.registry.settings
    conn = DBSession.connection()
    dialect = conn.dialect.name.lower()
    settings['pyramid_sacrud.models'] = get_sacrud_models(dialect)
