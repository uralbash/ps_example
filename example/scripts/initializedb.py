#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
init data
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
    DBSession,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def add_fixture(model, fixtures):
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
        out = Popen(["fortune", ""], stdout=PIPE).communicate()[0]
        text.append({'foo': out, 'ufoo': out, 'fooText': out, 'ufooText': out})
    add_fixture(TestTEXT, text)


def add_dnd():
    dnd = ({'name': 'foo', 'value': 1},
           {'name': 'foo1', 'value': 2},
           {'name': 'foo2', 'value': 3},
           {'name': 'foo3', 'value': 4},
           {'name': 'foo4', 'value': 5},
           {'name': 'foo5', 'value': 6})
    add_fixture(TestDND, dnd)


def add_extension(engine, *args):
    # добавляет расширения
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
