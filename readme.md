# dbcq

database connect and query for python.

```
db = dbcq("my_db")
result = db.qfad("select * from table where name = ?", "adam")
```

api doc [here](https://numlims.github.io/dbcq/).

## install

download dbcq whl from
[here](https://github.com/numlims/dbcq/releases). install whl with
pip:

```
pip install dbcq-<version>.whl
```

reference from your `pyproject.toml`, e.g.:

```
dependencies = [
  "dbcq @ git+https://github.com/numlims/dbcq.git"
]
```

## db connection

run `dbcq` once to create a stub config file:

```
$ dbcq
dbcq: stub config file created at /home/user/.config/dbcq.ini, please edit.
you can leave the config file there or move it to:
/etc/dbcq.ini
```

edit `dbcq.ini` to fill in the connection info, for example:

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

in this example, `my_db` would then be used to connect to the db:

```
dbcq("my_db")
```

to get a list of the available pyodbc driver names for `dbcq.ini`, run

```
dbcq --drivers
```

## dev

edit [`dbcq/main.ct`](./dbcq/main.ct) and [`dbcq/init.ct`](./dbcq/init.ct).

generate the code from ct with [ct](https://github.com/tnustrings/ct) or [ct for vscode](https://marketplace.visualstudio.com/items?itemName=tnustrings.codetext).

build and install:

```
make install
```

test:

```
make test
```


generate api doc:

```
make doc
```


## issues

what about DEFAULT in --targets?

what about pymysql driver?