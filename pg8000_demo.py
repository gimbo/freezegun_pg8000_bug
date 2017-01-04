#!/usr/bin/env python

"""Demonstrate freezegun/pg8000 bad interaction, directly.

Expects the existence of a database called 'foo' with one table 'foo' with one
date-type column called 'when', i.e.:

    $ psql -U postgres foo
    psql (9.6.1)
    Type "help" for help.

    foo=# \d foo
        Table "public.foo"
     Column | Type | Modifiers
    --------+------+-----------
     when   | date |

(Can be created using, e.g., sqlalchemy_demo.py)

Attempts to insert a date entry into that table, within a freezegun context; at
time of writing that results in the following exception:

    Traceback (most recent call last):
      File "/home/gimbo/.virtualenvs/sqlwtf/lib/python3.5/site-packages/pg8000/core.py", line 1849, in make_params
        params.append(self.py_types[typ])
    KeyError: <class 'freezegun.api.FakeDate'>

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "/home/gimbo/.virtualenvs/sqlwtf/lib/python3.5/site-packages/pg8000/core.py", line 1852, in make_params
        params.append(self.inspect_funcs[typ](value))
    KeyError: <class 'freezegun.api.FakeDate'>

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "./pg8000_demo.py", line 57, in <module>
        cursor.execute('INSERT INTO foo (when) VALUES (%s)', (today,))
      File "/home/gimbo/.virtualenvs/sqlwtf/lib/python3.5/site-packages/pg8000/core.py", line 906, in execute
        self._c.execute(self, operation, args)
      File "/home/gimbo/.virtualenvs/sqlwtf/lib/python3.5/site-packages/pg8000/core.py", line 1887, in execute
        params = self.make_params(args)
      File "/home/gimbo/.virtualenvs/sqlwtf/lib/python3.5/site-packages/pg8000/core.py", line 1855, in make_params
        "type " + str(e) + "not mapped to pg type")
    pg8000.core.NotSupportedError: type <class 'freezegun.api.FakeDate'>not mapped to pg type

"""

import datetime

from freezegun import freeze_time
import pg8000

conn = pg8000.connect(user='postgres', database='foo')
cursor = conn.cursor()
with freeze_time('2016-12-25'):
    today = datetime.date.today()
cursor.execute('INSERT INTO foo (when) VALUES (%s)', (today,))
