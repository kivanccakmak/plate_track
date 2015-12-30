from car_recorder import CarRecorder
from fconfig import Fconfig

CONFIG_FILE = "config.ini"
TABLE_NAME = 'car_info'
CREDENTIALS = {}
CREDENTIALS['name'] = 'Osman'
CREDENTIALS['surname'] = 'Osman'
CREDENTIALS['phone'] = '123'
CREDENTIALS['plate'] = '34OSM34'
CREDENTIALS['door'] = 'X10'
CREDENTIALS['email'] = 'osman@osman.com'

def main():
    """runs unit test procedure.
    """
    conf = Fconfig(CONFIG_FILE)
    db_name = conf.get_db_name()
    print "adding to database"
    add_test(db_name)
    print "removing from database"
    del_test(db_name)

def add_test(db_name):
    """adds car into database.
    :db_name: String
    """
    car = CarRecorder(CREDENTIALS, db_name)
    car.add_car(TABLE_NAME)

def del_test(db_name):
    """adds person to cars database.
    :db_name: String
    """
    car = CarRecorder(CREDENTIALS, db_name)
    car.del_car(TABLE_NAME)

if __name__ == "__main__":
    main()
