#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Catalog
"""
from pyramid_sqlalchemy import Session as DBSession


def includeme(config):
    conn = DBSession.connection()
    dialect = conn.dialect.name.lower()
    if dialect == 'postgresql':
        config.include("pyramid_sacrud_catalog")
