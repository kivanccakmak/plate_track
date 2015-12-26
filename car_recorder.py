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



