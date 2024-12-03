# __main__ is dbcq's cmd line client

import sys
from dbcq import dbcq
import simplejson as json
import argparse

# main runs a query and returns the result.
# it can also display a help message with place to put the .dbcq file 
def main():

    # abort if no ini file. do this before the argparse else argparse swallows it (even if this blocks dbcq -h)
    if not dbcq.hasini():
        msg = f"""no .dbc file found. please create it at {dbcq.inipath()} and put in the connection info:
[<target name>]
type = <mssql|sqlite>
database = <database name>
username = <user name>
password = <password>
server = <ip address>
port = <port>
driver = <driver>
        """
        print(msg)
        exit()

    # parse arguments
    parser = argparse.ArgumentParser(description="connect to a database")
    parser.add_argument("target", help="a target name in .dbc file")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    args = parser.parse_args()

    # get database
    target = args.target

    # start dbcq
    db = dbcq(target)

    # get query
    query = args.query

    # if file given, take query from file
    if args.f is not None:
        query = open(args.f, "r").read()

    # query and print result
    # print(jsonpickle.encode(db.qfad(query)))
    # jsonpickle puts decimals in wrappers.
    # could our db output give simpler types?
    # for now like this

    print(json.dumps(db.qfad(query), default=str))


sys.exit(main())
