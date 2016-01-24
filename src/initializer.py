#!/usr/bin/python
"""
Initialize script to construct
tables in database
"""
import sqlite3
from query import Query
from fconfig import Fconfig

def main():
    """creates database with tables
    """
    db_name = '../data/garage.sqlite'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    conf = Fconfig('config.ini')
    table_list = conf.get_config('tables')['name'].split()
    for table in table_list:
        fields = conf.get_table_fields(table)
        query = Query.get_create_qry(table, fields)
        cursor.execute(query)
    conn.close()

if __name__ == "__main__":
    main()



