# dbquery.py holds these functions:
# query
# qfa: query fetch all
# qfad: query fetch all dict
# row_to_dict

from dbc import *
import pyodbc

# query executes query with optional values
def query(query, *values, target=None):
    conn = connection(target=target)
    cursor = conn.cursor()
    cursor.execute(query, *values)
    conn.commit()
    conn.close()

# qfa executes query with optional values and returns results
def qfa(query, *values, target=None):
    conn = connection(target=target)
    cursor = conn.cursor()
    cursor.execute(query, *values)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    return rows

# qfad returns query result as array of dicts, e.g. for json parsing
def qfad(query, *values, target=None):
    rows = qfa(query, *values, target=target)
    dicts = [row_to_dict(row) for row in rows]
    return dicts

# row_to_dict turns row to dict
def row_to_dict(row):
    # lowercase column names
    columns = [tup[0].lower() for tup in row.cursor_description]
    # use column names as dict keys
    return dict(zip([c for c in columns], row))

