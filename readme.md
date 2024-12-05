# dbcq

dbcq is a little database connection and query wrapper for python.

```
db = dbcq("<target in .dbc>")
db.qfad("select * from table where name = ?", "adam")
```

## install

download dbcq whl from
[here](https://github.com/numlims/dbcq/releases). install whl with
pip:

```
pip install dbcq-<version>.whl
```

copy the `.dbc` file to your home directory and fill in the connection info.

```
[<db target name used in code>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
driver = <path to db driver if needed>
```

if you're unsure where your home directory is, say `dbcq` to see
where dbcq looks the `.dbc` file and put it there.

install the database connector with pip (for mssql install pyodbc, for
sqlite install sqlite3):

```
pip install pyodbc
pip install sqlite3
```

## documentation

documentation [here](https://numlims.github.io/dbcq/).

