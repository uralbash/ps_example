from sqlalchemy import (
    Text,
    String,
    Column,
    Unicode,
    Integer,
    Boolean,
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
    __tablename__ = 'test_hstore'
    id = Column(Integer, primary_key=True)
    foo = Column(MutableDict.as_mutable(HSTORE),
                 nullable=False, unique=True)

    def __init__(self, foo):
        self.foo = foo


class TestTEXT(Base):
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
    __tablename__ = 'test_bool'
    id = Column(Integer, primary_key=True)
    foo = Column(Boolean)

    def __init__(self, foo):
        self.foo = foo


class TestDND(Base):
    __tablename__ = 'test_dnd'
    __mapper_args__ = {'order_by': 'position'}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    value = Column(Integer)
    position = Column(Integer, default=0)

    def __init__(self, name, value, position):
        self.name = name
        self.value = value
        self.position = position

listen(TestDND, "before_insert", before_insert)
listen(TestDND, "before_update", before_insert)
