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
from subprocess import PIPE, Popen

import transaction
from jinja2.utils import generate_lorem_ipsum
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config

from pyramid_sacrud.security import permissions

from ..lib.fixture import add_fixture
from ..models import Base, DBSession
from ..models.auth import Company, User, UserPermission
from ..models.catalog import CatalogCategory, CatalogGroup, CatalogProduct
from ..models.funny_models import (MPTTPages, TestAllTypes, TestBOOL,
                                   TestCustomizing, TestFile, TestTEXT,
                                   TestUNION)
from ..models.postgres import TestHSTORE


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def add_hstore():
    hashes = ({'foo': "{'foo': 'bar', '1': '2'}"},
              {'foo': "{'test': 'data'}"})
    add_fixture(TestHSTORE, hashes)


def add_bool():
    booles = ({'foo': True},
              {'foo': False})
    add_fixture(TestBOOL, booles)


def add_text(settings):
    text = []
    n = int(settings.get('sacrud.debug_text_rows', 100))
    for i in range(n):
        try:
            out = Popen(["fortune", ""], stdout=PIPE).communicate()[0]
        except OSError:
            out = generate_lorem_ipsum()
        text.append({'foo': out.decode('utf-8'), 'ufoo': out.decode('utf-8'),
                     'fooText': out.decode('utf-8'),
                     'ufooText': out.decode('utf-8')})
    add_fixture(TestTEXT, text)


def add_union():
    uni = ({'name': 'foo',  'foo': True,  'cash': 100, 'double_cash': 100.13},
           {'name': 'foo1', 'foo': False, 'cash': 200, 'double_cash': 100.500},
           {'name': 'foo2', 'foo': True,  'cash': 1024, 'double_cash': 100.13},
           {'name': 'foo3', 'foo': False, 'cash': 100500, 'double_cash': 1.13},
           {'name': 'foo4', 'foo': False, 'cash': 19, 'double_cash': 6660.10},
           {'name': 'foo5', 'foo': True,  'cash': -123, 'double_cash': 130.03})
    add_fixture(TestUNION, uni)


def add_alltypes():
    objs = ({}, {}, {}, {}, {})
    add_fixture(TestAllTypes, objs)


def add_customizing():
    import random
    description = '''
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <p><img src="../../../../static/uploaded/foo.png" alt="" width="350" height="221" /></p>
        <hr />
        <h1>Use Pyramid with Go and Gevent-socketio!</h1>
        </body>
        </html>
    '''
    objs = [{'name': ('%06x' % random.randrange(16 ** 6)).upper(),
             'description': description, 'date': '2024-04-04'}
            for x in range(10)]
    add_fixture(TestCustomizing, objs)


def add_file():
    objs = [
        {'image': '/static/upload/60563666-c52a-4ec2-bc31-e21f9dcde296.gif'}]
    add_fixture(TestFile, objs)


def add_extension(engine, *args):
    """
    Add extension to PostgreSQL database.
    """
    conn = engine.connect()
    for ext in args:
        conn.execute('CREATE EXTENSION IF NOT EXISTS "%s"' % ext)
    conn.execute('COMMIT')
    conn.close()


def add_company():
    company = (
        {'name': u'ITCase'},
        {'name': u'RedHat'},
        {'name': u'Canonical'},
        {'name': u'Pylons'},
    )
    add_fixture(Company, company)


def add_catalog_group():
    rows = (
        {'name': u'3D Glass'},
        {'name': u'Drinks'},
        {'name': u'bar'},
        {'name': u'baz'},
    )
    add_fixture(CatalogGroup, rows)


def add_catalog_category():
    rows = (
        {'name': u'Electronics', 'group[]': ['1', '2']},
        {'name': u'Clothing'},
        {'name': u'Tableware'},
        {'name': u'Musical instruments'},
        {'name': u'Toys'},
        {'name': u'Weapon'},
        {'name': u'Melt'},
    )
    add_fixture(CatalogCategory, rows)


def add_catalog_product():
    shoes = (
        {'name': u'Valenki',    'category[]': ['2']},
        {'name': u'Kamik',      'category[]': ['2']},
        {'name': u'Lapti',      'category[]': ['2']},
        {'name': u'Galoshes',   'category[]': ['2']},
        {'name': u'Sandals',    'category[]': ['2']},
    )
    music_instruments = (
        {'name': u'Balalaika',      'category[]': ['4']},
        {'name': u'Garmon',         'category[]': ['4']},
        {'name': u'Bayan',          'category[]': ['4']},
        {'name': u'Gypsy guitar',   'category[]': ['4']},
        {'name': u'Spoons',         'category[]': ['4']},
        {'name': u'Treshchotka',    'category[]': ['4']},
        {'name': u'Tambourine',     'category[]': ['4']},
    )
    weapon = (
        {'name': u'Shashka', 'category[]': ['6']},
    )
    tableware = (
        {'name': u'Granyonyi stakan', 'category[]': ['3']},
        {'name': u'Podstakannik', 'category[]': ['3']},
        {'name': u'Samovar', 'category[]': ['3']},
    )
    toys = (
        {'name': u'Cheburashka', 'category[]': ['5']},
        {'name': u'Matryoshka', 'category[]': ['5']},
        {'name': u'Petrushka',  'category[]': ['5']},
    )
    eat = (
        {'name': 'subway sub',  'category[]': ['7']},
        {'name': 'Borscht',     'category[]': ['7']},
        {'name': 'Solyanka',    'category[]': ['7']},
        {'name': u'Knedlík',    'category[]': ['7']},
        {'name': 'Manti',       'category[]': ['7']},
        {'name': 'Pelmeni',     'category[]': ['7']},
        {'name': 'Bliny',       'category[]': ['7']},
        {'name': 'Okroshka',    'category[]': ['7']},
        {'name': 'Shashlik',    'category[]': ['7']},
        {'name': 'Shchi',       'category[]': ['7']},
        {'name': 'Ukha',        'category[]': ['7']},
        {'name': 'Sausage',     'category[]': ['7']},
        {'name': u'Ciorbă',     'category[]': ['7']},
        {'name': u'Königsberger Klopse', 'category[]': ['7']},
    )
    drinks = (
        {'name': u'Kissel',     'category[]': ['7'], 'group[]': '2'},
        {'name': 'Coca-Cola',   'category[]': ['7'], 'group[]': ['2']},
        {'name': 'Kvass',       'category[]': ['7'], 'group[]': ['2']},
        {'name': 'Lemonade',    'category[]': ['7'], 'group[]': ['2']},
        {'name': 'Tea',         'category[]': ['7'], 'group[]': ['2']},
        {'name': 'Coffe',       'category[]': ['7'], 'group[]': ['2']},
        {'name': 'Medovukha',   'category[]': ['7'], 'group[]': ['2']},
    )
    add_fixture(CatalogProduct, shoes)
    add_fixture(CatalogProduct, music_instruments,  delete=False)
    add_fixture(CatalogProduct, weapon,             delete=False)
    add_fixture(CatalogProduct, tableware,          delete=False)
    add_fixture(CatalogProduct, toys,               delete=False)
    add_fixture(CatalogProduct, eat,                delete=False)
    add_fixture(CatalogProduct, drinks,             delete=False)


def add_mptt_pages():
    """ level           Nested sets tree1
          1                    1(1)22
                  _______________|___________________
                 |               |                   |
          2    2(2)5           6(4)11             12(7)21
                 |               ^                   ^
          3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                |          |
          4                                  14(9)15   18(11)19

        level           Nested sets tree2
          1                    1(12)22
                  _______________|___________________
                 |               |                   |
          2    2(13)5         6(15)11             12(18)21
                 |               ^                    ^
          3    3(14)4     7(16)8   9(17)10   13(19)16   17(21)20
                                                 |          |
          4                                  14(20)15   18(22)19

    """
    pages = (
        {'in_menu': True,  'slug': '/',   'name': 'About company',
            'visible': True, 'parent_id': None},
        {'in_menu': True,  'slug': 'we-love-gevent',
            'name': u'We ♥  gevent',    'visible': True, 'parent_id': '1'},
        {'in_menu': True,  'slug': 'and-pyramid',
            'name': 'And Pyramid',      'visible': True, 'parent_id': '2'},
        {'in_menu': True,  'slug': 'our-history',     'name': 'Our history',
            'visible': False, 'parent_id': '1'},
        {'in_menu': True,  'slug': 'foo',             'name': 'foo',
            'visible': True, 'parent_id': '4'},
        {'in_menu': True,  'slug': 'kompania-itcase',
            'name': u'компания ITCase', 'visible': False, 'parent_id': '4'},
        {'in_menu': False, 'slug': 'our-strategy',
            'name': 'Our strategy',     'visible': True, 'parent_id': '1'},
        {'in_menu': False, 'slug': 'wordwide',        'name': 'Wordwide',
            'visible': True, 'parent_id': '7'},
        {'in_menu': True,  'slug': 'technology',      'name': 'Technology',
            'visible': False, 'parent_id': '8'},
        {'in_menu': False, 'slug': 'what-we-do',      'name': 'What we do',
            'visible': True,  'parent_id': '7'},
        {'in_menu': True,  'slug': 'at-a-glance',     'name': 'at a glance',
            'visible': True,  'parent_id': '10'},

        {'in_menu': True,  'slug': 'foo12', 'name': 'foo12',
            'visible': True, 'parent_id': None, 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo13', 'name': 'foo13',
            'visible': False, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo14', 'name': 'foo14',
            'visible': False, 'parent_id': '13', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo15', 'name': 'foo15',
            'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo16', 'name': 'foo16', 'redirect_type': '200',
            'redirect_page': '2', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo17', 'name': 'foo17', 'redirect_type': '301',
            'redirect_page': '3', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'yandex', 'name': 'yandex', 'redirect_type': '302',
            'redirect_url': 'http://ya.ru', 'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo19', 'name': 'foo19',
            'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo20', 'name': 'foo20',
            'visible': True, 'parent_id': '19', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo21', 'name': 'foo21',
            'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo22', 'name': 'foo22',
            'visible': True, 'parent_id': '21', 'tree_id': '12'},
    )
    add_fixture(MPTTPages, pages)


def add_user(user):
    new_user = User(user_name=user['login'], email=user['email'])
    new_user.regenerate_security_code()
    new_user.status = 1
    new_user.set_password(user['password'])
    new_user.name = user['name']
    new_user.surname = user['surname']
    new_user.middlename = user['middlename']
    new_user.type_id = 1
    new_user.company_id = 1
    DBSession.add(new_user)
    transaction.commit()


def add_admin_permission():
    admin_permissions = []
    for permission in permissions:
        admin_permissions.append({'user_id': '1', 'perm_name': permission})
    add_fixture(UserPermission, admin_permissions)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    # drop database
    Base.metadata.drop_all(engine)
    transaction.commit()

    # add postgres extension
    dialect = engine.dialect.name
    if dialect == 'postgresql':
        add_extension(engine,
                      "plpythonu",
                      "hstore",
                      "uuid-ossp")
        from ..models.postgres import Base as BasePostgres
        from ..models.catalog import Base as BaseCatalog
        BasePostgres.metadata.create_all(engine)
        BaseCatalog.metadata.create_all(engine)

    # create database
    Base.metadata.create_all(engine)

    # add_hstore()
    add_bool()
    add_text(settings)
    add_union()
    add_alltypes()
    add_customizing()
    add_file()
    add_mptt_pages()

    # Catalog
    if dialect == 'postgres':
        add_catalog_group()
        add_catalog_category()
        add_catalog_product()

    # Auth
    add_company()
    add_user({'login': 'admin', 'password': '123',
              'email': 'foo@bar.baz', 'name': 'Foo',
              'surname': 'Bar', 'middlename': 'Baz'})
    add_admin_permission()
