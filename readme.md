# dbcq

dbcq is a little database connection and query wrapper for python.

```
db = dbcq("<target in .dbc>")
result = db.qfad("select * from table where name = ?", "adam")
```
documentation [here](https://numlims.github.io/dbcq/).

## install

download dbcq whl from
[here](https://github.com/numlims/dbcq/releases). install whl with
pip:

```
pip install dbcq-<version>.whl
```

## db connection

in your home directory, create a file named `.dbc` and fill in the
connection info in the <> brackets like this:

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

for example:

```
[my_db]
type = mssql
database = my_db
username = hireader
password = ?hireaderpass?
server = 10.11.22.33
port = 1234
driver = /path/to/my/libmsodbcsql-18.3.so.2.1
```

if you're unsure where your home directory is, say `dbcq` to see
where dbcq looks the `.dbc` file and put it there.

to get a list of the available pyodbc driver names for `.dbc`, run

```
dbcq --drivers
```

## dev

assemble code from the .ct files with [ct](https://github.com/tnustrings/ct).

build and install:

```
make install
```

## issues

what about DEFAULT in --targets?

what about pymysql driver?