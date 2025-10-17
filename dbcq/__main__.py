import cnf
import sys
from dbcq import dbcq
from dbcq import TargetException
import simplejson as json
import argparse

try:
    import pyodbc
except:
    pyodbc = None
def main():
    """
    main runs a query and returns the result. it can also display a help message with place to put the .dbcq file .
    """
    parser = argparse.ArgumentParser(description="connect to a database")
    parser.add_argument("target", nargs="?", help="a target name in .dbc file")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    parser.add_argument("--targets", action="store_true", help="show targets", required=False)
    parser.add_argument("--drivers", action="store_true", help="show pyodbc drivers", required=False)    
    args = parser.parse_args()
    try:
        db = dbcq(args.target)
    except cnf.MakeCnfException as e:
        print("dbcq: " + str(e))
        return 1
    except TargetException as e: # is this referencable from other packages?
        print("dbcq: " + str(e))
        return 1
    query = args.query
    if args.f is not None:
        with open(args.f, "r") as f:
            query = f.read()
    if args.targets is True:
        for t in dbcq.targets():
            print(t)
        return 0
    if args.drivers is True:
        if pyodbc is not None:
            print(pyodbc.drivers())
        return 0
    print(json.dumps(db.qfad(query), default=str))
    return 0
sys.exit(main())
