# __main__.py was generated from main.ct. 
# if you edit __main__.py, run `ct -tc __main__.py` afterwards to update main.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files main.ct __main__.py

# # main
# 
# __main__ is dbcq's cmd line client.  1``//__main__.py:
# the imports.
# 
# pyodbc shouldn't need a try anymore, cause it's listed as dependency
# in pyproject.toml.  17``/import:
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
#``17
# main runs a query and returns the result. it also accepts command line
# flags for showing drivers and db targets.  2``/main:
def main():
    # make a dbcq instance here, so that its cnf can talk to argparse, set the dbcq target later.
    # 
    # silently exit if the conf file was just created and needs editing.  3.``
    try:
        db = dbcq()
    except cnf.MakeCnfException as e:
        print("dbcq: " + str(e))
        return 1
    # parse arguments.  4``
    parser = argparse.ArgumentParser(description="connect to a database")
    parser.add_argument("target", nargs="?", help="a target name in .dbc file")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    parser.add_argument("--targets", action="store_true", help="show targets", required=False)
    parser.add_argument("--drivers", action="store_true", help="show pyodbc drivers", required=False)
    parser.add_argument("--csv", help="csv output to file or stdout", default=None, const=True, nargs="?") # default: if no --csv flag is passed, const: if --csv is passed without arg
    parser.add_argument("-D", help="csv output delimiter, default comma")
    # add version and config flags.  5``
    versionflag.flag(parser, "dbcq")
    db.conf.addflags(parser)
    # parse the arguments.  6``
    args = parser.parse_args()
    # see if dbcq's config handles the args.  7``
    if db.conf.handleflag(args):
        return 1
    # show targets if needed and exit.  8``
    if args.targets is True:
        for t in db.targets():
            print(t)
        return 0
    # show drivers if needed and exit.  9``
    if args.drivers is True:
        if pyodbc is not None:
            print(pyodbc.drivers())
        return 0
    # try to set the target.  10``
    try:
        db.set_target(args.target)
    except TargetException as e: # is this referencable from other packages?
        print("dbcq: " + str(e))
        return 1
    # get the query. if file given, take query from file.  11``
    query = args.query
    if args.f is not None:
        with open(args.f, "r") as f:
            query = f.read()
    # query and output the result as json or csv.  12``
    res = db.qfad(query)
    if len(res) == 0:
        return 0
    if args.csv is not None:
        # output csv. if no filename was given, args.csv is True, which prints
        # to stdout. (todo do differently?)  13``./csv:
        with open(args.csv, "w") as f:
            # make a writer, use the keys from the first row as header.  14.``
            delim = args.D
            if delim is None:
                delim = ","
            writer = csv.DictWriter(f, fieldnames=res[0].keys(), delimiter=delim)
            # write the header and the rows.  15``
            writer.writeheader()
            for row in res:
                writer.writerow(row)
            #``14
        #``13
    else:
        # print the json.  16``/main/json:
        print(json.dumps(res, default=str))
        #``16
    return 0
    #``3
#``2
sys.exit(main())
#``1
