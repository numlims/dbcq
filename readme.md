# dbcq

dbcq is a little database connection and query wrapper for python.

put the connection info in `db.ini`:

```
[<db target name used in code>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
```

place the db.ini somewhere where it isn't accidentally shared
with the rest of your code.

put the driver and path to db.ini in `dbc.ini`:

```
[db]
ini = <path to your db.ini>
[driver]
mssql = <path to your mssql driver>
```

place the `dbc.ini` in the root directory of your code.

then say in code:

```
from dbcq import dbcq
db = dbcq("<db target in db.ini>")
db.qfad("select * from table where name = ?", "adam")
```

if you use mssql install pyodbc, if you use sqlite install sqlite3:

```
pip install pyodbc
pip install sqlite3
```

## next

maybe look for connection info in ~/.dbcq.ini and accept it as path

$ dbcq -help

your home directory seems to be /my/home. please put a file named
.dbcq.ini there with the connection info

[<db target name used in code>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
driver = <driver>