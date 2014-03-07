#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
This module for initialize project.
"""
import os
import sys
import transaction

from subprocess import Popen, PIPE
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    TestHSTORE,
    TestBOOL,
    TestDND,
    TestTEXT,
    TestUNION,
    DBSession,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def add_fixture(model, fixtures):
    """
    Add fixtures to database.

    Example::

        hashes = ({'foo': {'foo': 'bar', '1': '2'}}, {'foo': {'test': 'data'}})
        add_fixture(TestHSTORE, hashes)

    """
    with transaction.manager:
        DBSession.query(model).delete()
        for fixture in fixtures:
            DBSession.add(model(**fixture))


def add_hstore():
    hashes = ({'foo': {'foo': 'bar', '1': '2'}},
              {'foo': {'test': 'data'}})
    add_fixture(TestHSTORE, hashes)


def add_bool():
    booles = ({'foo': True},
              {'foo': False})
    add_fixture(TestBOOL, booles)


def add_text():
    text = []
    for i in range(10):
        try:
            out = Popen(["fortune", ""], stdout=PIPE).communicate()[0]
        except OSError:
            from jinja2.utils import generate_lorem_ipsum
            out = generate_lorem_ipsum()
        text.append({'foo': out, 'ufoo': out, 'fooText': out, 'ufooText': out})
    add_fixture(TestTEXT, text)


def add_dnd():
    dnd = ({'name': 'foo', 'value': 1, 'position1': 1},
           {'name': 'foo1', 'value': 2, 'position1': 2},
           {'name': 'foo2', 'value': 3, 'position1': 3},
           {'name': 'foo3', 'value': 4, 'position1': 4},
           {'name': 'foo4', 'value': 5, 'position1': 5},
           {'name': 'foo5', 'value': 6, 'position1': 6})
    add_fixture(TestDND, dnd)


def add_union():
    uni = ({'name': 'foo',  'foo': True,  'cash': 100, 'double_cash': 100.13},
           {'name': 'foo1', 'foo': False, 'cash': 200, 'double_cash': 100.500},
           {'name': 'foo2', 'foo': True,  'cash': 1024, 'double_cash': 100.13},
           {'name': 'foo3', 'foo': False, 'cash': 100500, 'double_cash': 1.13},
           {'name': 'foo4', 'foo': False, 'cash': 19, 'double_cash': 6660.10},
           {'name': 'foo5', 'foo': True,  'cash': -123, 'double_cash': 130.03})
    add_fixture(TestUNION, uni)


def add_extension(engine, *args):
    """
    Add extension to PostgreSQL database.
    """
    conn = engine.connect()
    for ext in args:
        conn.execute('CREATE EXTENSION IF NOT EXISTS "%s"' % ext)
    conn.execute('COMMIT')
    conn.close()


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    # дропает БД
    Base.metadata.drop_all(engine)
    # добавляет расширения
    add_extension(engine, "plpythonu", "hstore", "uuid-ossp")

    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    add_hstore()
    add_bool()
    add_dnd()
    add_text()
    add_union()
