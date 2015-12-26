from car_recorder import CarRecorder
from fconfig import Fconfig

CONFIG_FILE = "config.ini"

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
    table_name = "car_info"
    name = "Ahmet"
    surname = "Cakmak"
    phone = "02163508667"
    email = "ahmet@cakmak.com"
    plate = "34AHM34"
    door = "X10"
    car = CarRecorder(name, surname, phone,
            email, plate, door, db_name)
    car.add_car(table_name)

def del_test(db_name):
    """adds person to cars database.
    :db_name: String
    """
    table_name = "car_info"
    name = "Ahmet"
    surname = "Cakmak"
    phone = "02163508667"
    email = "ahmet@cakmak.com"
    plate = "34AHM34"
    door = "X10"
    car = CarRecorder(name, surname, phone,
            email, plate, door, db_name)
    car.del_car(table_name)

if __name__ == "__main__":
    main()
