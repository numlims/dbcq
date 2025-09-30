from dbcq._dbc import *
import sys
class dbcq:
    def __init__(self, target):
        if not hasini():
            msg = f"""dbcq: {dbcq.inipath()} not found. please create the file and fill in:
[<target name>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
driver = <driver>"""
            print(msg)
            raise Exception("no .dbc file")
        self.target = target
        if target:
            self.info = dbinfo(target)
    def hasini():
        return _dbc.hasini()
    def inipath():
        return _dbc.inipath()
    def targets():
        return _dbc.targets()
    def query(self, query, *values):
        with dbconnect(target=self.target) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            conn.commit()
    def qfa(self, query, *values):
        with dbconnect(target=self.target) as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            rows = cursor.fetchall()
            conn.commit()

            return rows
    def qfad(self, query, *values):
        if self.info["type"] == "mssql":
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
        elif self.info["type"] == "sqlite":
            with dbconnect(target=self.target) as conn:
                cursor = conn.cursor()
                cursor.row_factory = sqlite3.Row
                cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
                rows = cursor.fetchall()
                conn.commit()

                dicts = [dict(row) for row in rows]
                return dicts
        else:
              print(f"db type {self.info['type']} is currently not supported.")
    def info(self):
        return self.info
    def _row_to_dict(self, row):
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))
