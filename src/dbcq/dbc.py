# dbc.py holds functions that give a db connection
# supported: mssql and sqlite

# functions:
# dbconnect
# dbinfo
# dburi
# _connection_string

# db interface imports are optional, so that the user can pip install only those he needs.

try:
    import pyodbc
except:
    pyodbc = None
import configparser
import inspect
import os
from pathlib import Path
try:
    import sqlite3
except:
    sqlite = None

# connection returns a database connection
def dbconnect(target=None):
    info = dbinfo(target)
    # connect differently depending on database type
    if info['type'] == "sqlite":
        return sqlite3.connect(info['database'])
    else:
        return pyodbc.connect(_connection_string(target))

# connection_string returns a connection string
def _connection_string(target) -> str:
    info = dbinfo(target)

    connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + '; encrypt=no;'

    return connection_string

# dburi returns a database uri
def dburi(target):
    info = dbinfo(target)
    
    # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    # ?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
    uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
    return uri

# dbinfo gets database info from ini file
def dbinfo(target):

    if not hasini():
        return None
    
    # we put a file named .dbcq in the home dir, so it can be read regardless from where the code is called.

    ini = configparser.ConfigParser()
    ini.read(inipath())

    info = {
        'type': ini[target]["type"],
        'database': ini[target]["database"],
        'username': ini[target]["username"] if "username" in ini[target] else None,
        'password': ini[target]["password"] if "password" in ini[target] else None,
        'server': ini[target]["server"] if "server" in ini[target] else None,
        'port': ini[target]["port"] if "port" in ini[target] else None,
        'driver': ini[target]["driver"] if "driver" in ini[target] else None
    }
    
    return info

# inipath returns the path to the ini
def inipath():
    home = Path.home()
    return home / ".dbcq"

# hasini reports whether there is a .dbcq ini file
def hasini():
    return inipath().is_file()
