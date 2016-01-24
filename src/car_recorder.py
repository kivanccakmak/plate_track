#!/usr/bin/python
"""
Searching and Manipulating
SQL Database
"""
import sqlite3
import ConfigParser
import collections
from query import Query

class CarRecorder(object):

    """Sets and Gets car information in database"""

    def __init__(self, credentials, db_name):
        """initiate car object which has contact info
        :credentials: dict
            contains meta-data from form input
        :db_name: str
            relative path of database
        """
        self.info = {}
        for key in credentials.keys():
            self.info[key] = credentials[key]
        self._conn = sqlite3.connect(db_name)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def add_car(self, table_name):
        """Record car information into database.
        :table_name: str
        """
        query = Query.get_add_qry(self.info, table_name)
        print query
        self._cursor.execute(query)
        self._conn.commit()

    def del_car(self, table_name):
        """Deletes car entry from database
        by using plate.
        :table_name: str
        """
        info = {'plate':self.info['plate']} # hard-coded
        query = Query.get_delete_qry(info, table_name)
        print query
        self._cursor.execute(query)
        self._conn.commit()

    def get_table_info(self, table_name):
        """returns table info in raw factory.
        :table_name: str
        :returns: sqlite3.Row object
            contains array of dict which represents
            all entries in table
        """
        query = 'SELECT * FROM [{tbl}]'.format(
                tbl=table_name)
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        return rows

    def get_plate_records(self, plate, table_name):
        """Checks whether plate exist in database
        or not
        :plate: str
            plate number of car
        :table_name: str
            car information table in database
        :returns: dict
            car relevant information in database
        """
        query = 'SELECT * FROM [{tbl}] WHERE' + ' ' +\
                '"plate"="{str}"' # hard-coded
        query = query.format(tbl=table_name, str=plate)
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        return rows

