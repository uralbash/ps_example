#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for example
"""
from sqlalchemy import (
    Text,
    String,
    Column,
    Unicode,
    Integer,
    Boolean,
    Numeric,
    UnicodeText,
)

from sacrud.position import before_insert

from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import (
    #UUID,
    HSTORE,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
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


class TestTEXT(Base):
    """
    SQLAlchemy model for demonstration work with any text type field.

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.String` field.
    :param ufoo: :class:`sqlalchemy.Unicode` field.
    :param fooText: :class:`sqlalchemy.Text` field.
    :param ufooText: :class:`sqlalchemy.UnicodeText` field.

    Usage::

        >>> params = ('blablabla', 'blablabla!', 'bla bla bla', 'blablabla')
        >>> text_obj = TestTEXT(*params)
        >>> text_obj.foo, text_obj.ufoo, text_obj.fooText, text_obj.ufooText
        ('blablabla', 'blablabla!', 'bla bla bla', 'blablabla')

    """
    __tablename__ = 'test_text'
    id = Column(Integer, primary_key=True)
    foo = Column(String)
    ufoo = Column(Unicode)
    fooText = Column(Text)
    ufooText = Column(UnicodeText)

    def __init__(self, foo, ufoo, fooText, ufooText):
        self.foo = foo
        self.ufoo = ufoo
        self.fooText = fooText
        self.ufooText = ufooText


class TestBOOL(Base):
    """
    SQLAlchemy model for demonstration :class:`sqlalchemy.Boolean` field

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.Boolean` field.

    Usage::

        >>> TestBOOL(True).foo, TestBOOL(False).foo
        (True, False)

    """
    __tablename__ = 'test_bool'
    id = Column(Integer, primary_key=True)
    foo = Column(Boolean)

    def __init__(self, foo):
        self.foo = foo


class TestDND(Base):
    """
    SQLAlchemy model for demonstration draggable field.

    :param id: standart pk.
    :param name: :class:`sqlalchemy.Unicode` field.
    :param value: :class:`sqlalchemy.Integer` field.
    :param position1: :class:`sqlalchemy.Integer` field.
    """
    __tablename__ = 'test_dnd'
    __mapper_args__ = {'order_by': 'position1'}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    value = Column(Integer)
    position1 = Column(Integer, default=0)

    def __init__(self, name, value, position1):
        self.name = name
        self.value = value
        self.position1 = position1

listen(TestDND, "before_insert", before_insert)
listen(TestDND, "before_update", before_insert)


class TestUNION(Base):
    """
    SQLAlchemy model for demonstration draggable field.

    :param id: standart pk.
    :param name: :class:`sqlalchemy.Unicode` field.
    :param foo: :class:`sqlalchemy.Boolean` field.
    :param double_cash: :class:`sqlalchemy.Numeric` field.
    """
    __tablename__ = 'test_union'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    foo = Column(Boolean)
    cash = Column(Integer)
    double_cash = Column(Numeric(10, 2))

    def __init__(self, name, foo, cash, double_cash):
        self.name = name
        self.foo = foo
        self.cash = cash
        self.double_cash = double_cash
