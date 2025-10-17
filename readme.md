# dbcq

dbcq is a little database connection and query wrapper for python.

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

## db connection

run `dbcq` to create a config file `.dbc` in your home directory:

```
$ dbcq
dbcq: please edit /your/home/.dbc, then run again.
```

fill in the connection info in `.dbc`, for example:

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

to get a list of the available pyodbc driver names for `.dbc`, run

```
dbcq --drivers
```

## dev

to generate the code from the .ct files get [ct](https://github.com/tnustrings/ct).

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