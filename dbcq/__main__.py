# automatically generated, DON'T EDIT. please edit main.ct from where this file stems.
import cnf
import sys
from dbcq import dbcq
from dbcq import TargetException
import simplejson as json
import argparse
import csv

try:
    import pyodbc
except:
    pyodbc = None
def main():
    """
     main runs a query and returns the result. it also accepts command line
     flags for showing drivers and db targets.
    """
    parser = argparse.ArgumentParser(description="connect to a database")
    parser.add_argument("target", nargs="?", help="a target name in .dbc file")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    parser.add_argument("--targets", action="store_true", help="show targets", required=False)
    parser.add_argument("--drivers", action="store_true", help="show pyodbc drivers", required=False)
    parser.add_argument("--csv", help="csv output to file or stdout", default=None, const=True, nargs="?") # default: if no --csv flag is passed, const: if --csv is passed without arg
    parser.add_argument("-D", help="csv output delimiter, default comma")    
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
    res = db.qfad(query)
    if len(res) == 0:
        return 0
    if args.csv is not None:
        with open(args.csv, "w") as f:
            delim = args.D
            if delim is None:
                delim = ","
            writer = csv.DictWriter(f, fieldnames=res[0].keys(), delimiter=delim)
            writer.writeheader()
            for row in res:
                writer.writerow(row)
    else:
        print(json.dumps(res, default=str))
    return 0
sys.exit(main())
