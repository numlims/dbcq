# dbcq

dbcq is a little database connection and query wrapper for python.

to open a database connection and get query results as a dict, put the
connection info in `db.ini`:

```
[<db target name used in code>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
```

put the driver and path to db.ini in `dbc.ini`:

```
[db]
ini = <path to your db.ini>
[driver]
mssql = <path to your mssql driver>
```

then say in code:

```
from dbcq import dbcq
db = dbcq("<db target in db.ini>")
db.qfad("select * from table where name = ?", "adam")
```

if you use mssql install pyodbc, if sqlite install sqlite3:

```
pip install pyodbc
pip install sqlite3
```

## build

say

```
python3 -m build
```