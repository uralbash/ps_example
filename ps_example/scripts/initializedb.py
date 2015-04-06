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
import logging
import os
import sys

import sqlalchemy
import transaction
from alembic import command
from alembic.config import Config
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from pyramid_sqlalchemy import Session as DBSession
from sqlalchemy import engine_from_config

from pyramid_sacrud.security import permissions
from sacrud_common.db import Fixture, add_extension

from ..includes.auth.models import (Group, GroupPermission, User, UserGroup,
                                    UserPermission)
# from ..includes.home.models.funny_models import (TestAllTypes, TestBOOL,
#                                                  TestCustomizing, TestFile,
#                                                  TestTEXT, TestUNION)
# from ..includes.home.models.postgres import TestHSTORE
from ..includes.pages.models import MPTTPages

logger = logging.getLogger(__name__)

here = os.path.dirname(os.path.realpath(__file__))
fixtures_dir = os.path.join(here, 'fixtures')
fixture = Fixture(DBSession, path=fixtures_dir)
fixtures = (
    {'model': MPTTPages,
     'fixtures': "mptt_pages.json"},
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def create_tables(DBSession):
    # DROP ALL EXIST TABLE
    meta = sqlalchemy.MetaData(DBSession.bind.engine)
    meta.reflect()
    meta.drop_all()

    # CREATE Log and alembic_version TABLE
    # move_it_in_alembic_in_futures = (Models...)
    # for model in move_it_in_alembic_in_futures:
    #     model.__table__.create(checkfirst=True, bind=DBSession.bind.engine)
    DBSession.bind.engine.execute(
        """CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL);
        """)


def add_user(user):
    new_user = User(id=100500, user_name=user['login'], email=user['email'])
    new_user.regenerate_security_code()
    new_user.set_password(user['password'])
    new_user.name = user['name']
    new_user.surname = user['surname']
    new_user.middlename = user['middlename']
    new_user.type_id = 1
    new_user.company_id = 1
    new_user.is_superuser = True
    DBSession.add(new_user)
    DBSession.flush()
    transaction.commit()


def add_admin_permission():
    admin_permissions = []
    for permission in permissions:
        admin_permissions.append({'user_id': '100500',
                                  'perm_name': permission})
    fixture.add(UserPermission, admin_permissions)


def add_group_permissions():
    PERMISSION_HOME = 'home'
    # Add groups
    groups = ({'group_name': PERMISSION_HOME, 'member_count': 100,
               'description': "Home page accsess"},)
    fixture.add(Group, groups)
    # Add groups to user
    user_group = ({'user_id': 100500, 'group_id': 1},)
    fixture.add(UserGroup, user_group)
    # Add permission to group
    group_permissions = ({'perm_name': PERMISSION_HOME, 'group_id': 1},)
    fixture.add(GroupPermission, group_permissions)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])

    # settings
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    # recreate database
    create_tables(DBSession)
    alembic_cfg = Config(config_uri)
    command.upgrade(alembic_cfg, "head")

    # add postgres extension
    dialect = engine.dialect.name
    if dialect == 'postgresql':
        if not add_extension(engine, "hstore", "uuid-ossp"):
            logger.warn("You have not SUPERUSER role for Postgres!")
            logger.warn("Extensions passed...")
        from ..includes.home.models.postgres import Base as BasePostgres
        from ..includes.catalog.models import Base as BaseCatalog
        BasePostgres.metadata.create_all(engine)
        BaseCatalog.metadata.create_all(engine)

    def add_fixtures(fixtures):
        for item in fixtures:
            fixture.add(**item)
            transaction.commit()

    # fill database
    add_fixtures(fixtures)
    add_user({'login': 'admin', 'password': '123',
              'email': 'arkadiy@bk.ru', 'name': u'Владимир',
              'surname': u'Хонин', 'middlename': u'Андреевич'})
    add_admin_permission()
    add_group_permissions()
