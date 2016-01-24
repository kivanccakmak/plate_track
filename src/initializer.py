import sqlite3
from query import Query
from fconfig import Fconfig

CONFIG_FILE = "config.ini"

class Initialize:

    @staticmethod
    def init_db(fname):
        """
        creates database and tables with respect
        to config.ini
        """
        conf = Fconfig(fname)
        table_list = conf.get_config('tables')['name'].split()
        db_name = \
            conf.get_config('database')['name'].split()[0]

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        for table in table_list:
            fields = conf.get_table_fields(table)
            query = Query.get_create_qry(table, fields)
            cursor.execute(query)
        conn.close()

def main():
    """creates database with tables
    """
    Initialize.init_db(CONFIG_FILE)

if __name__ == "__main__":
    main()



