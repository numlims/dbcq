import configparser
import inspect
import os
from pathlib import Path
try:
    import pyodbc
except:
    pyodbc = None
try:
    import sqlite3
except:
    sqlite = None
def dbconnect(target=None):
    """
    """
    info = dbinfo(target)
    if info['type'] == "sqlite":
        if sqlite3 == None:
            print("error: sqlite3 package missing, please install with pip.")
            exit
        return sqlite3.connect(info['database'])
    else:
        if pyodbc == None:
            print("error: pyodbc package missing, please install with pip.")
            exit
        # print("connection string: " + _connection_string(target))
        return pyodbc.connect(_connection_string(target))
def _connection_string(target) -> str:
    """
    _connection_string returns a connection string.
    """
    info = dbinfo(target)
    connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + ';encrypt=no;'

    return connection_string
def dburi(target):
    """
    dburi returns a database uri.
    """
    info = dbinfo(target)
    uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
    return uri
def dbinfo(target):
    """
    dbinfo gets database info from .dbc file.
    """
    if not hasini():
        return None
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
def targets():
    """
    targets returns the db targets from the ini file.
    """
    ini = configparser.ConfigParser()
    ini.read(inipath())

    out = []

    for target in ini.keys():
        out.append(target)

    return out
def inipath():
    """
    inipath returns the path to the ini.
    """
    home = Path.home()
    return home / ".dbc"
def hasini():
    """
    hasini reports whether there is a .dbc ini file.
    """
    return inipath().is_file()
