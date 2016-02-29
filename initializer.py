#!/usr/bin/python
"""
Initialize script to construct
tables in database
"""
import sqlite3
from src.query import Query
from src.fconfig import Fconfig
import sys

def main(db_name):
    """creates database with tables
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    conf = Fconfig('src/config.ini')
    table_list = conf.get_config('tables')['name'].split()
    for table in table_list:
        fields = conf.get_table_fields(table)
        query = Query.get_create_qry(table, fields)
        cursor.execute(query)
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "illegal usage"
        print "{} db_name"
        sys.exit()
    main(sys.argv[1])



