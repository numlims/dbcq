# __init__.py was generated from init.ct. 
# if you edit __init__.py, run `ct -tc __init__.py` afterwards to update init.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files init.ct __init__.py

# dbcq holds functions for db connection and querying.  1``//__init__.py:
# import.  6``/import:
import cnf
# imports for dbconnect.  14``/import
try:
    import pyodbc
except:
    pyodbc = None
    
import sqlite3
# the pyodbc import is optional here although it is required in
# pyproject.toml, but this could maybe be a pattern for other dbc
# packages that the user could install with pip.
# 
# sqlite3 is part of the python installation.
#``=
# import.  16``/import
from contextlib import closing
#``6
class dbcq:
    # add a config template.  7``/var:
    cnftemplate = """[<target name>]
    type = <mssql|sqlite>
    database = <database name>
    username = <user name>
    password = <password>
    server = <ip address>
    port = <port>
    driver = <driver>
    """
    #``7
    # __init__ loads the ini and remembers the target.
    # 
    # throws a `TargetException`.  2``/init:
    def __init__(self, target:str):
        # get the ini.  3.``
        self.ini = cnf.makeload(path="dbcq.ini", roots=[cnf.system, cnf.home], fmt="ini", make=self.cnftemplate, company="numlims")
        # check that there's a target and that it's in the ini.  4``
        if target == None or target == "":
            raise TargetException("please specify a db target from: " + str(self.targets()))
        if target not in self.targets():
            raise TargetException(f"target {target} not known. please specify a db target from: " + str(self.targets()))
        # get the database info for the target.  5``
        self.target = target
        if target:
            self._info = self._dbinfo(self.ini, target)
        # don't open a connection here that is used in all methods, cause when
        # the methods are called simultaneously (for example from api endpoints)
        # it gives a 'connection is busy with results for another command'
        # error.
        # 
        # maybe use the connection like this:
        # 
        # with closing(self.dbconnect()) as conn:
        #   crs = conn.cursor()
        #   crs.execute("my query")
        # 
        # with calls conn.commit() after the with block, but not crs.close() nor
        # conn.close(). see https://stackoverflow.com/a/3783252 and
        # https://github.com/mkleehammer/pyodbc/issues/43   the closing() call should close the connection.  https://github.com/mkleehammer/pyodbc/wiki/Connection#context-manager
        #``=
        #``3
    #``2
    # targets gives the db targets from .dbc ini file.  8``/targets:
    def targets(self):
        out = []
    
        for target in self.ini.keys():
            out.append(target)
    
        return out
    #``8
    # info returns the database info for the current target.  9``/info:
    def info(self):
        return self._info
    #``9
    # dbconnect returns a database connection for the current target.  10``/dbconnect:
    def dbconnect(self):
        # connect differently depending on database type.  11.``
        info = self._info
        if info['type'] == "sqlite":
            # for sqlite. is the package installed?  12``./sqlite:
            if sqlite3 == None:
                print("error: sqlite3 package missing, please install with pip.")
                exit
            return sqlite3.connect(info['database'])
            #``12
        else:
            # else go with pyodbc for now.  13``../else:
            if pyodbc == None:
                print("error: pyodbc package missing, please install with pip.")
                exit
            # print("connection string: " + self.connection_string(self._info))
            return pyodbc.connect(self.connection_string(self._info))
            #``13
        #``11
    #``10
    # query executes query with optional values.  15``/query:
    def query(self, query, *values):
        with closing(self.dbconnect()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            conn.commit()
    #``15
    # qfa (query-fetch-all) executes a query with optional values and returns
    # the results.  17``/qfa:
    def qfa(self, query, *values):
        with closing(self.dbconnect()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            rows = cursor.fetchall()
            conn.commit()

            return rows
    #``17
    # qfad (query-fetch-all-dict) returns the query results as an array of dicts,
    # e.g. for json parsing.  18``/qfad:
    def qfad(self, query, *values):
        if self._info["type"] == "mssql":
            # for mssql, fold in the cursor description of the row.  19``./mssql:
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
            #``19
        elif self._info["type"] == "sqlite":
            # for sqlite, use row factory. from https://stackoverflow.com/a/41920171  20``../sqlite:
            with closing(self.dbconnect()) as conn:
                cursor = self.conn.cursor()
                cursor.row_factory = sqlite3.Row
                cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
                rows = cursor.fetchall()
                conn.commit()

                dicts = [dict(row) for row in rows]
                return dicts
            #``20
        else:
            # else, say not supported.  21``../else:
              print(f"db type {self._info['type']} is currently not supported.")
            #``21
    #``18

    # connection_string returns a connection string from info.  25``/connection_string:
    @staticmethod
    def connection_string(info) -> str:
        # put together the connection string with params from info and return.  26.``
        connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + ';encrypt=no;'
    
        return connection_string
        #``26
    #``25
    # dburi returns a database uri from info.  27``/dburi:
    @staticmethod
    def dburi(info):
        # put together the uri with params from the info and return.
        # 
        # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85  28.``
        uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
        return uri
        #``28
    #``27
    
    # dbinfo gets the database info for target from ini.  22``/_dbinfo:
    @staticmethod
    def _dbinfo(ini, target):
        # fill the info from the ini and return.  23.``
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
        #``23
    #``22
    # _row_to_dict turns pyodbc-rows to dict:  24``/_row_to_dict:
    def _row_to_dict(self, row):
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))
    #``24

# TargetException is thrown when the target is missing.  29``/TargetException:
class TargetException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#``29
#``1
