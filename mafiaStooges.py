import sqlite3
import logging

def init_tables(connection):
   try:
      c = connection.cursor()
      c.execute('''create table posts (
         id integer,
         content text,
         author integer,
         constraint uniquePosts unique (id)
      );''')
      c.execute('''create table authors (
         id integer primary key autoincrement,
         name text,
         roleID integer,
         isMafia integer,
         constraint uniqueAuthors unique (name)
      );''')
      c.execute('''create table roles (
         id integer primary key autoincrement,
         roleName text,
         isEvil integer
      );''')
      c.close()
   except sqlite3.OperationalError:
      logging.info("Tables already exist")
   else:
      logging.info("Tables created")

