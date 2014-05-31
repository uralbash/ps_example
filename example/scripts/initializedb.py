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

from example import get_sacrud_models
from example.lib.fixture import add_fixture
from example.models import Base, DBSession
from example.models.auth import Company, User
from example.models.funny_models import (CatalogCategory, CatalogGroup,
                                         CatalogProduct, MPTTPages,
                                         TestAllTypes, TestBOOL,
                                         TestCustomizing, TestDND, TestFile,
                                         TestHSTORE, TestTEXT, TestUNION,
                                         WidgetPosition)


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


def add_text():
    text = []
    for i in range(100):
        try:
            out = Popen(["fortune", ""], stdout=PIPE).communicate()[0]
        except OSError:
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
    objs = [{'image': '/static/upload/60563666-c52a-4ec2-bc31-e21f9dcde296.gif'}]
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


def add_catalog_category():
    group = DBSession.query(CatalogGroup).all()
    rows = (
        {'name': u'Electronics'},
        {'name': u'Clothing'},
        {'name': u'Tableware'},
        {'name': u'Musical instruments'},
        {'name': u'Toys'},
        {'name': u'Weapon'},
    )
    add_fixture(CatalogCategory, rows)
    tv = DBSession.query(CatalogCategory).first()
    tv.group = [group[0], group[2]]
    transaction.commit()


def add_catalog_group():
    rows = (
        {'name': u'3D Glass'},
        {'name': u'foo'},
        {'name': u'bar'},
        {'name': u'baz'},
    )
    add_fixture(CatalogGroup, rows)


def add_catalog_product():
    shoes = (
        {'name': u'Valenki'},
        {'name': u'Kamik'},
        {'name': u'Lapti'},
        {'name': u'Galoshes'},
        {'name': u'Sandals'},
    )
    music_instruments = (
        {'name': u'Balalaika'},
        {'name': u'Garmon'},
        {'name': u'Bayan'},
        {'name': u'Gypsy guitar'},
        {'name': u'Spoons'},
        {'name': u'Treshchotka'},
        {'name': u'Tambourine'},
    )
    weapon = (
        {'name': u'Shashka'},
    )
    tableware = (
        {'name': u'Granyonyi stakan'},
        {'name': u'Podstakannik'},
        {'name': u'Samovar'},
    )
    toys = (
        {'name': u'Cheburashka'},
        {'name': u'Matryoshka'},
        {'name': u'Petrushka'},
    )
    eat = (
        {'name': 'subway sub'},
        {'name': 'Borscht'},
        {'name': 'Solyanka'},
        {'name': u'Knedlík'},
        {'name': 'Manti'},
        {'name': 'Pelmeni'},
        {'name': 'Bliny'},
        {'name': 'Okroshka'},
        {'name': 'Shashlik'},
        {'name': 'Shchi'},
        {'name': 'Ukha'},
        {'name': 'Sausage'},
        {'name': u'Ciorbă'},
        {'name': u'Königsberger Klopse'},
    )
    drinks = (
        {'name': 'Kissel'},
        {'name': 'Coca-Cola'},
        {'name': 'Kvass'},
        {'name': 'Lemonade'},
        {'name': 'Tea'},
        {'name': 'Coffe'},
        {'name': 'Medovukha'},
    )
    add_fixture(CatalogProduct, shoes)
    add_fixture(CatalogProduct, music_instruments,  delete=False)
    add_fixture(CatalogProduct, weapon,             delete=False)
    add_fixture(CatalogProduct, tableware,          delete=False)
    add_fixture(CatalogProduct, toys,               delete=False)
    add_fixture(CatalogProduct, eat,                delete=False)
    add_fixture(CatalogProduct, drinks,             delete=False)


def add_widgets_position(sacrud_models):
    row = ()
    for model_name, values in sacrud_models.items():
        row += ({'widget': model_name, 'column': values.get('column', 0),
                 'position': values.get('position', 0)}, )
    add_fixture(WidgetPosition, row)


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
        {'in_menu': True,  'slug': '/',   'name': 'About company', 'visible': True, 'parent_id': None},
        {'in_menu': True,  'slug': 'we-love-gevent',  'name': u'We ♥  gevent',    'visible': True, 'parent_id': '1'},
        {'in_menu': True,  'slug': 'and-pyramid',     'name': 'And Pyramid',      'visible': True, 'parent_id': '2'},
        {'in_menu': True,  'slug': 'our-history',     'name': 'Our history',      'visible': False, 'parent_id': '1'},
        {'in_menu': True,  'slug': 'foo',             'name': 'foo',              'visible': True, 'parent_id': '4'},
        {'in_menu': True,  'slug': 'kompania-itcase', 'name': u'компания ITCase', 'visible': False, 'parent_id': '4'},
        {'in_menu': False, 'slug': 'our-strategy',    'name': 'Our strategy',     'visible': True, 'parent_id': '1'},
        {'in_menu': False, 'slug': 'wordwide',        'name': 'Wordwide',         'visible': True, 'parent_id': '7'},
        {'in_menu': True,  'slug': 'technology',      'name': 'Technology',       'visible': False, 'parent_id': '8'},
        {'in_menu': False, 'slug': 'what-we-do',      'name': 'What we do',       'visible': True,  'parent_id': '7'},
        {'in_menu': True,  'slug': 'at-a-glance',     'name': 'at a glance',      'visible': True,  'parent_id': '10'},

        {'in_menu': True,  'slug': 'foo12', 'name': 'foo12', 'visible': True, 'parent_id': None, 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo13', 'name': 'foo13', 'visible': False, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo14', 'name': 'foo14', 'visible': False, 'parent_id': '13', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo15', 'name': 'foo15', 'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo16', 'name': 'foo16', 'redirect_type': '200', 'redirect_page': '2', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo17', 'name': 'foo17', 'redirect_type': '301', 'redirect_page': '3', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo18', 'name': 'foo18', 'redirect_type': '302', 'redirect_url': 'http://ya.ru', 'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'in_menu': False, 'slug': 'foo19', 'name': 'foo19', 'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo20', 'name': 'foo20', 'visible': True, 'parent_id': '19', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo21', 'name': 'foo21', 'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'in_menu': True,  'slug': 'foo22', 'name': 'foo22', 'visible': True, 'parent_id': '21', 'tree_id': '12'},
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


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')

    # drop database
    Base.metadata.drop_all(engine)
    transaction.commit()

    # add postgres extension
    add_extension(engine,
                  # "plpythonu",
                  "hstore",
                  "uuid-ossp")

    # create database
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    add_hstore()
    add_bool()
    add_dnd()
    add_text()
    add_union()
    add_alltypes()
    add_customizing()
    add_file()
    add_mptt_pages()
    add_widgets_position(get_sacrud_models())

    # Catalog
    add_catalog_group()
    add_catalog_category()
    add_catalog_product()

    # Auth
    add_company()
    add_user({'login': 'admin', 'password': '123',
              'email': 'foo@bar.baz', 'name': 'Foo',
              'surname': 'Bar', 'middlename': 'Baz'})
