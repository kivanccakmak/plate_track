import sqlite3
import ConfigParser
import collections
from query import Query

CONFIG_FILE = "config.ini"

class CarRecorder(object):

    """Sets and Gets car information in database"""

    def __init__(self, name, surname, phone, 
            email, plate, door, db_name):
        """initiate car object which has contact info
        :name: string
        :surname: string
        :email: string
        :phone: string
        :plate: string
        :door: string
        """
        self.info = {}
        self.info['name'] = name
        self.info['surname'] = surname
        self.info['email'] = email
        self.info['phone'] = phone
        self.info['plate'] = plate
        self.info['door'] = door
        self._conn = sqlite3.connect(db_name)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def add_car(self, table_name):
        """Record car information into database.
        :table_name: string
        """
        query = Query.get_add_qry(self.info, table_name)
        print query
        self._cursor.execute(query)
        self._conn.commit()

    def del_car(self, table_name):
        """Deletes car entry from database by using plate.
        :table_name: string
        """
        info = {'plate':self.info['plate']}
        query = Query.get_delete_qry(info, table_name)
        print query
        self._cursor.execute(query)
        self._conn.commit()

    def get_table_info(self, table_name):
        """returns table info in raw factory.
        :table_name: string
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
        :plate: string
            plate number of car
        :table_name: string
            car information table in database
        :returns: dict
            car relevant information in database
        """
        query = 'SELECT * FROM [{tbl}] WHERE' + ' ' +\
                '"plate"="{str}"'
        query = query.format(tbl=table_name, str=plate)
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        return rows






