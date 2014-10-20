#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for postgresql example
"""
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, HSTORE, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict

Base = declarative_base()


class TestHSTORE(Base):

    """
    SQLAlchemy model for demonstration of the postgres dialect
    :class:`sqlalchemy.dialects.postgresql.HSTORE` field

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.dialects.postgresql.HSTORE` field.

    Usage::

        >>> hash = {'param1': 'foo', 'param2': 'bar'}
        >>> hstore_obj = TestHSTORE(hash)
        >>> hstore_obj.foo
        {'param2': 'bar', 'param1': 'foo'}

    """
    __tablename__ = 'test_hstore'

    id = Column(Integer, primary_key=True)
    foo = Column(MutableDict.as_mutable(HSTORE),
                 nullable=False, unique=True)

    def __init__(self, foo):
        self.foo = foo


class TestPostgresTypes(Base):

    """
    SQLAlchemy model for demonstration all types field.
    """
    __tablename__ = 'test_postgres_types'

    col_pk = Column(Integer, primary_key=True)
    col_array = Column(ARRAY(Integer, as_tuple=True))
    col_json = Column(JSON)  # for postgresql 9.3 version
    sak = Column(BYTEA, default="FF")
    col_hstore = Column(MutableDict.as_mutable(HSTORE))

    def __repr__(self):
        return self.col_pk
