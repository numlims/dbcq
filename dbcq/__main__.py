# __main__.py was generated from main.ct. 
# if you edit __main__.py, run `ct -tc __main__.py` afterwards to update main.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files main.ct __main__.py

# __main__ is dbcq's cmd line client.  1``//__main__.py:
# the imports.
# 
# pyodbc shouldn't need a try anymore, cause it's listed as dependency
# in pyproject.toml.  15``/import:
import cnf
import sys
from dbcq import dbcq
from dbcq import TargetException
import simplejson as json
import argparse
import csv
import versionflag

try:
    import pyodbc
except:
    pyodbc = None
#``15
# main runs a query and returns the result. it also accepts command line
# flags for showing drivers and db targets.  2``/main:
def main():
    # parse arguments.  3.``
    parser = argparse.ArgumentParser(description="connect to a database")
    parser.add_argument("target", nargs="?", help="a target name in .dbc file")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    parser.add_argument("--targets", action="store_true", help="show targets", required=False)
    parser.add_argument("--drivers", action="store_true", help="show pyodbc drivers", required=False)
    parser.add_argument("--csv", help="csv output to file or stdout", default=None, const=True, nargs="?") # default: if no --csv flag is passed, const: if --csv is passed without arg
    parser.add_argument("-D", help="csv output delimiter, default comma")
    versionflag.flag(parser, "dbcq")
    # parse the arguments.  4``
    args = parser.parse_args()
    # start dbcq, silently exit if the conf file was just created and needs editing.  5``
    try:
        db = dbcq(args.target)
    except cnf.MakeCnfException as e:
        print("dbcq: " + str(e))
        return 1
    # check that the target was there.  6``
    except TargetException as e: # is this referencable from other packages?
        print("dbcq: " + str(e))
        return 1
    # get the query. if file given, take query from file.  7``
    query = args.query
    if args.f is not None:
        with open(args.f, "r") as f:
            query = f.read()
    # show targets if needed and exit.  8``
    if args.targets is True:
        for t in dbcq.targets():
            print(t)
        return 0
    # show drivers if needed and exit.  9``
    if args.drivers is True:
        if pyodbc is not None:
            print(pyodbc.drivers())
        return 0
    # query and output the result as json or csv.  10``
    res = db.qfad(query)
    if len(res) == 0:
        return 0
    if args.csv is not None:
        # output csv. if no filename was given, args.csv is True, which prints
        # to stdout. (todo do differently?)  11``./csv:
        with open(args.csv, "w") as f:
            # make a writer, use the keys from the first row as header.  12.``
            delim = args.D
            if delim is None:
                delim = ","
            writer = csv.DictWriter(f, fieldnames=res[0].keys(), delimiter=delim)
            # write the header and the rows.  13``
            writer.writeheader()
            for row in res:
                writer.writerow(row)
            #``12
        #``11
    else:
        # print the json.  14``/main/json:
        print(json.dumps(res, default=str))
        #``14
    return 0
    #``3
#``2
sys.exit(main())
#``1
