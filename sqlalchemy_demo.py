#!/usr/bin/env python

"""Demonstrate freezegun/pg8000 bad interaction, via sqlalchemy.

Expects the existence of a database called 'foo'.

Creates a table 'foo' with one date-type column called 'when' and attempts to
insert to insert a date entry into that table, within a freezegun context; at
time of writing that results in a 'pg8000.core.NotSupportedError' exception:

"""

import datetime

from freezegun import freeze_time
from sqlalchemy import Column, create_engine, Date, MetaData, Table
from sqlalchemy.sql import select

# Insertion using pg8000 will fail under freezegun; with psycopg2 it works.
engine = create_engine('postgresql+pg8000://postgres@localhost/foo')

metadata = MetaData()
foo = Table('foo', metadata, Column('when', Date))
metadata.create_all(engine)

conn = engine.connect()

with freeze_time('2016-12-25'):
    ins = foo.insert().values(when=datetime.datetime.utcnow())
conn.execute(ins)

result = conn.execute(select([foo]))
for row in result:
    print(row)
