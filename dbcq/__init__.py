# __init__.py was generated from init.ct. 
# if you edit __init__.py, run `ct -tc __init__.py` afterwards to update init.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files init.ct __init__.py

# # init
# 
# dbcq holds functions for db connection and querying.  1``//__init__.py:
# import.  8``/import:
import cnf
# imports for dbconnect.  16``/import
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
# import.  18``/import
from contextlib import closing
#``8
class dbcq:
    # add a config template.  9``/var:
    cnftemplate = """[<target name>]
    type = <mssql|sqlite>
    database = <database name>
    username = <user name>
    password = <password>
    server = <ip address>
    port = <port>
    driver = <driver>
    """
    #``9
    # __init__ loads the ini and remembers the target.
    # 
    # throws a `TargetException`.  2``/init:
    def __init__(self, target:str=None):
        # get the ini.  3.``
        self.conf = cnf.cnf(path="dbcq.ini", roots=[cnf.system, cnf.user], fmt="ini", make=self.cnftemplate, company="numlims")
        self.ini = self.conf.conf  # todo call makeload() here?
        # set the target.  4``
        if target is not None:
            self.set_target(target)
        #``3
    #``2
    # set_target sets the target.  5``/set_target:
    def set_target(self, target):
        # check that there's a target and that it's in the ini.  6.``
        if target == None or target == "":
            raise TargetException("please specify a db target from: " + str(self.targets()))
        if target not in self.targets():
            raise TargetException(f"target {target} not known. please specify a db target from: " + str(self.targets()))
        # get the database info for the target.  7``
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
        #``6
    #``5
    # targets gives the db targets from .dbc ini file.  10``/targets:
    def targets(self):
        out = []
    
        for target in self.ini.keys():
            out.append(target)
    
        return out
    #``10
    # info returns the database info for the current target.  11``/info:
    def info(self):
        return self._info
    #``11
    # dbconnect returns a database connection for the current target.  12``/dbconnect:
    def dbconnect(self):
        # connect differently depending on database type.  13.``
        info = self._info
        if info['type'] == "sqlite":
            # for sqlite. is the package installed?  14``./sqlite:
            if sqlite3 == None:
                print("error: sqlite3 package missing, please install with pip.")
                exit
            return sqlite3.connect(info['database'])
            #``14
        else:
            # else go with pyodbc for now.  15``../else:
            if pyodbc == None:
                print("error: pyodbc package missing, please install with pip.")
                exit
            # print("connection string: " + self.connection_string(self._info))
            return pyodbc.connect(self.connection_string(self._info))
            #``15
        #``13
    #``12
    # query executes query with optional values.  17``/query:
    def query(self, query, *values):
        with closing(self.dbconnect()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            conn.commit()
    #``17
    # qfa (query-fetch-all) executes a query with optional values and returns
    # the results.  19``/qfa:
    def qfa(self, query, *values):
        with closing(self.dbconnect()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            rows = cursor.fetchall()
            conn.commit()

            return rows
    #``19
    # qfad (query-fetch-all-dict) returns the query results as an array of dicts,
    # e.g. for json parsing.  20``/qfad:
    def qfad(self, query, *values):
        if self._info["type"] == "mssql":
            # for mssql, fold in the cursor description of the row.  21``./mssql:
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
            #``21
        elif self._info["type"] == "sqlite":
            # for sqlite, use row factory. from https://stackoverflow.com/a/41920171  22``../sqlite:
            with closing(self.dbconnect()) as conn:
                cursor = self.conn.cursor()
                cursor.row_factory = sqlite3.Row
                cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
                rows = cursor.fetchall()
                conn.commit()

                dicts = [dict(row) for row in rows]
                return dicts
            #``22
        else:
            # else, say not supported.  23``../else:
              print(f"db type {self._info['type']} is currently not supported.")
            #``23
    #``20

    # connection_string returns a connection string from info.  27``/connection_string:
    @staticmethod
    def connection_string(info) -> str:
        # put together the connection string with params from info and return.  28.``
        connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + ';encrypt=no;'
    
        return connection_string
        #``28
    #``27
    # dburi returns a database uri from info.  29``/dburi:
    @staticmethod
    def dburi(info):
        # put together the uri with params from the info and return.
        # 
        # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85  30.``
        uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
        return uri
        #``30
    #``29
    
    # dbinfo gets the database info for target from ini.  24``/_dbinfo:
    @staticmethod
    def _dbinfo(ini, target):
        # fill the info from the ini and return.  25.``
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
        #``25
    #``24
    # _row_to_dict turns pyodbc-rows to dict:  26``/_row_to_dict:
    def _row_to_dict(self, row):
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))
    #``26

# TargetException is thrown when the target is missing.  31``/TargetException:
class TargetException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#``31
#``1
