import cnf
try:
    import pyodbc
except:
    pyodbc = None
    
import sqlite3
class dbcq:
    cnftemplate = """[<target name>]
    type = <mssql|sqlite>
    database = <database name>
    username = <user name>
    password = <password>
    server = <ip address>
    port = <port>
    driver = <driver>
    """
    def __init__(self, target:str):
        """
        __init__ opens a db connection to a target from .dbc.
        
        throws a `TargetException`.
        """
        self.ini = cnf.makeload(path=".dbc", root=cnf.home, fmt="ini", make=self.cnftemplate)
        if target == None or target == "":
            raise TargetException("please specify a db target from: " + str(self.targets()))
        if target not in self.targets():
            raise TargetException(f"target {target} not known. please specify a db target from: " + str(self.targets()))
        self.target = target
        if target:
            self.info = self._dbinfo(self.ini, target)
    def targets(self):
        """
        targets gives the db targets from .dbc ini file.
        """
        out = []
    
        for target in self.ini.keys():
            out.append(target)
    
        return out
    def info(self):
        """
        info returns the database info for the current target.
        """
        return self.info
    def dbconnect(self):
        """
        dbconnect returns a database connection for the current target.
        """
        info = self.info
        if info['type'] == "sqlite":
            if sqlite3 == None:
                print("error: sqlite3 package missing, please install with pip.")
                exit
            return sqlite3.connect(info['database'])
        else:
            if pyodbc == None:
                print("error: pyodbc package missing, please install with pip.")
                exit
            # print("connection string: " + self.connection_string(self.info))
            return pyodbc.connect(self.connection_string(self.info))
    def query(self, query, *values):
        """
        query executes query with optional values.
        """
        with self.dbconnect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            conn.commit()
    def qfa(self, query, *values):
        """
        qfa (query-fetch-all) executes a query with optional values and returns
        the results.
        """
        with self.dbconnect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, *values)
            rows = cursor.fetchall()
            conn.commit()

            return rows
    def qfad(self, query, *values):
        """
        qfad (query-fetch-all-dict) returns the query results as an array of dicts,
        e.g. for json parsing.
        """
        if self.info["type"] == "mssql":
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
        elif self.info["type"] == "sqlite":
            with self.dbconnect() as conn:
                cursor = conn.cursor()
                cursor.row_factory = sqlite3.Row
                cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
                rows = cursor.fetchall()
                conn.commit()

                dicts = [dict(row) for row in rows]
                return dicts
        else:
              print(f"db type {self.info['type']} is currently not supported.")

    @staticmethod
    def connection_string(info) -> str:
        """
        connection_string returns a connection string from info.
        """
        connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + ';encrypt=no;'
    
        return connection_string
    @staticmethod
    def dburi(info):
        """
        dburi returns a database uri from info.
        """
        uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
        return uri
    
    @staticmethod
    def _dbinfo(ini, target):
        """
        """
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
    def _row_to_dict(self, row):
        """
        _row_to_dict turns pyodbc-rows to dict:
        """
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))

class TargetException(Exception):
    def __init__(self, message:str):
        """
        """
        super().__init__(message)
