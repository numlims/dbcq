# dbcq

dbcq is a little database connection and query wrapper for python.

to open a database connection and get query results as a dict, put the
connection info in `db.ini`, the driver and path to `db.ini` in
`dbc.ini` and say:

```
from dbcq import *
db = dbcq("<db target>")
db.qfad("select * from table where name = ?", "adam")
```