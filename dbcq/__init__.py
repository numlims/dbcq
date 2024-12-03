"""
dbcq holds functions for db connection and querying
"""

from dbcq._dbc import *
import sys

class dbcq:

    "dbcq opens a db connection to a target from .dbc"
    def __init__(self, target):
        self.target = target
        self.info = dbinfo(target)

    def hasini():
        "hasini returns whether there is a .dbc ini file in the home"
        return dbc.hasini()
    
    def inipath():
        "inipath gives the path where dbcq looks for the .dbc ini file (usually in the home)"

        return dbc.inipath()
    
    def query(self, query, *values):
        "query executes query with optional values"

        conn = dbconnect(target=self.target)
        cursor = conn.cursor()
        cursor.execute(query, *values)
        conn.commit()
        conn.close()


    def qfa(self, query, *values):
        "qfa executes query with optional values and returns results"
            
        conn = dbconnect(target=self.target)
        cursor = conn.cursor()
        cursor.execute(query, *values)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        return rows

    def qfad(self, query, *values):
        "qfad returns query result as array of dicts, e.g. for json parsing"

        # for mssql, fold in cursor description of row
        if self.info["type"] == "mssql":
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
        elif self.info["type"] == "sqlite":
            # for sqlite, use row factory
            # from https://stackoverflow.com/a/41920171
            conn = dbconnect(target=self.target)
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
            rows = cursor.fetchall()
            conn.commit()
            conn.close()

            dicts = [dict(row) for row in rows]
            return dicts

    def info(self):
        "info returns database info"

        return self.info
    

    def _row_to_dict(self, row):
        "_row_to_dict turns pyodbc-rows to dict"
            
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))


