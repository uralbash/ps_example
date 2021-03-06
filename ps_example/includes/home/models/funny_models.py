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
import os
import uuid

import deform
from pyramid_sqlalchemy import BaseObject
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, Numeric, String, Text,
                        Unicode, UnicodeText)
from sqlalchemy.orm import relationship

from pyramid_elfinder.models import ElfinderString
from sacrud.exttype import ChoiceType, FileStore, GUID, SlugType

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                         'static')


class TestDeform(BaseObject):
    __tablename__ = "test_deform"

    id = Column(Integer, primary_key=True)
    filestore = Column(FileStore(path="/static/uploaded/",
                                 abspath=os.path.join(file_path, 'uploaded')))
    filestore2 = Column(FileStore(path="/static/uploaded/",
                                  abspath=os.path.join(file_path, 'uploaded')))
    filestore3 = Column(FileStore(path="/static/uploaded/",
                                  abspath=os.path.join(file_path, 'uploaded')))

    TEST_CHOICES = (
        ('200', 'OK (200)'),
        ('301', 'Moved Permanently (301)'),
        ('302', 'Moved Temporarily (302)'),
    )

    choice = Column(ChoiceType(choices=TEST_CHOICES))
    guid = Column(GUID(), default=uuid.uuid4)
    enum = Column(Enum(u'IPv6', u'IPv4', name=u"ip_type"))

    elfinder = Column(ElfinderString,
                      info={"verbose_name": u'Проверка Elfinder', })

    foo = Column(String)
    slug = Column(SlugType('foo', False))


class TestFile(BaseObject):

    """
    SQLAlchemy model for demonstration file field.
    """
    __tablename__ = 'test_file'

    id = Column(Integer, primary_key=True)
    image = Column(FileStore(path="/static/uploaded/",
                             abspath=os.path.join(file_path, 'uploaded')))

    def __init__(self, image, id=None):
        self.id = id
        self.image = image

    def __repr__(self):
        return self.image


class TestTEXT(BaseObject):

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
    __mapper_args__ = {'order_by': 'id'}

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

    # SACRUD
    verbose_name = 'test_text and pagination'


class TestBOOL(BaseObject):

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


class TestUNION(BaseObject):

    """
    SQLAlchemy model for demonstration union field.

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

    def __repr__(self):
        return self.name


class TestAllTypes(BaseObject):

    """
    SQLAlchemy model for demonstration all types field.
    """
    __tablename__ = 'test_all_types'

    TEST_CHOICES = {'val_1': 'val_1', 'val_2': 'val_2', 'val_3': 'val_3',
                    'val_4': 'val_4', 'val_5': 'val_5', 'val_6': 'val_6'}

    col_pk = Column(Integer, primary_key=True)
    col_bigint = Column(BigInteger)
    col_boolean = Column(Boolean)
    col_date_time = Column(Date)
    col_date = Column(DateTime)
    col_date2 = Column(DateTime)
    col_enum = Column(Enum(u'IPv6', u'IPv4', name=u"ip_type"))
    col_choice = Column(ChoiceType(choices=TEST_CHOICES.items()),
                        info={"verbose_name": u'Проверка select', })
    col_float = Column(Float)

    # http://sqlalchemy.readthedocs.org/en/latest/orm/relationships.html?highlight=remote_side#adjacency-list-relationships
    fk_test_alltypes = Column(Integer, ForeignKey('test_all_types.col_pk'))
    fk_test_union = Column(Integer, ForeignKey('test_union.id'))
    testalltypes = relationship('TestAllTypes')
    testunion = relationship('TestUNION')

    col_elfinder = Column(ElfinderString,
                          info={"verbose_name": u'Проверка Elfinder', })

    col_guid = Column(GUID(), default=uuid.uuid4)
    col_integer = Column(Integer)

    col_numeric = Column(Numeric(10, 2))
    col_string = Column(String)
    col_text = Column(Text)
    col_unicode = Column(Unicode)
    col_unicode_text = Column(UnicodeText)

    def __repr__(self):
        return self.col_pk


class TestCustomizing(BaseObject):
    __tablename__ = "test_customizing"

    id = Column(Integer, primary_key=True)
    name = Column(String,
                  info={"description": "put there name"})
    date = Column(Date,
                  info={"colanderalchemy": {'title': 'date JQuery-ui'}})
    name_ru = Column(String,
                     info={"colanderalchemy": {'title': u'Название'}})
    name_fr = Column(String,
                     info={"colanderalchemy": {'title': u'nom'}})
    name_bg = Column(String,
                     info={"colanderalchemy": {'title': u'Име'}})
    name_cze = Column(String,
                      info={"colanderalchemy": {'title': u'název'}})
    description = Column(
        Text,
        info={"colanderalchemy": {
            'widget': deform.widget.TextAreaWidget(
                css_class='tinymce content')}})
    description2 = Column(
        Text,
        info={"colanderalchemy": {
            'widget': deform.widget.TextAreaWidget(css_class='tinymce')}})

    visible = Column(Boolean)
    in_menu = Column(Boolean, info={"verbose_name": u'menu?',
                                    "description": "Added this page in menu"})
    in_banner = Column(Boolean, info={"verbose_name": u'on banner?', })

    # SACRUD
    verbose_name = u'Customizing table'
    sacrud_list_col = [name, name_ru, name_cze]
    sacrud_detail_col = [('name space', [name, name_ru, name_bg,
                                         name_fr, name_cze]
                          ),
                         ('description', [description, date,
                                          in_menu, visible, in_banner,
                                          description2])
                         ]
