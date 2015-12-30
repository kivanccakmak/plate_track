from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from car_recorder import CarRecorder
from fconfig import Fconfig
import sys
import os

CONFIG_FILE = 'config.ini'
CAR_TABLE = 'car_info'

class AppWin(object):
    """Application UI Class."""
    def __init__(self):
        """init function."""
        self.app = QtGui.QApplication(sys.argv)
        self.tabs = QtGui.QTabWidget()
        self.tabs.setWindowTitle('Garage App')
        self.tabs.setMinimumSize(625, 500)

        # initialize form tab and its items
        self.form_tab = QtGui.QWidget()
        self.form_layout = QtGui.QFormLayout()
        self.form_button = QtGui.QPushButton('Save', self.form_tab)
        self.form_warning = QtGui.QLabel('', self.form_tab)
        self.form_boxes = {}

        # initialize view tab and its items
        self.view_tab = QtGui.QWidget()
        self.view_table = QtGui.QTableWidget(self.view_tab)
        self.set_form_tab()
        self.set_view_tab()

        # initialize process tab and its items
        self.process_tab = QtGui.QWidget()
        self.process_layout = QtGui.QVBoxLayout()
        self.process_btn = QtGui.QPushButton('Recognize Plate')
        self.process_label = QtGui.QLabel()
        self.fopen_btn = QtGui.QPushButton('Open File')
        self.set_process_tab()

    def set_form_tab(self):
        """sets input form which would be used to
        enter new car into database.
        """
        self.add_form_input(self.form_layout, 'Name', 'name', 10, 10, 200)
        self.add_form_input(self.form_layout, 'Surname', 'surname', 10, 60, 200)
        self.add_form_input(self.form_layout, 'Phone', 'phone', 10, 110, 200)
        self.add_form_input(self.form_layout, 'E-mail', 'email', 10, 160, 200)
        self.add_form_input(self.form_layout, 'Door', 'door', 10, 210, 200)
        self.add_form_input(self.form_layout, 'Plate', 'plate', 10, 260, 200)
        self.form_warning.move(14, 330)
        self.form_button.move(485, 350)
        self.form_button.connect(self.form_button, QtCore.SIGNAL('clicked()'),
                self.form_btn_click)
        self.form_tab.setLayout(self.form_layout)
        self.tabs.addTab(self.form_tab, "New Car")

    def set_process_tab(self):
        """sets image processing tab. image would be chosen by document
        window, then openalpr would be run
        """
        self.process_layout.addWidget(self.process_label)
        self.process_layout.addWidget(self.process_btn)
        self.process_layout.addWidget(self.fopen_btn)
        self.process_tab.setLayout(self.process_layout)
        self.fopen_btn.clicked.connect(self.getfile)
        self.tabs.addTab(self.process_tab, "Process Cars")

    def getfile(self):
        fname = QtGui.QFileDialog.getOpenFileName(None, 'Open File',
                '/', 'Image Files (*.jpg *.png)')
        pixmap = QtGui.QPixmap(fname)
        pixmap = pixmap.scaled(625, 500)
        self.process_label.setPixmap(pixmap)

    def form_btn_click(self):
        """checks textboxes of form, if name, surname, door and
        plate number is provided; adds car into database
        """
        name = self.form_boxes['name'].text()
        surname = self.form_boxes['surname'].text()
        phone = self.form_boxes['phone'].text()
        email = self.form_boxes['email'].text()
        door = self.form_boxes['door'].text()
        plate = self.form_boxes['plate'].text()
        result = self.form_check(name, surname, door, plate)
        if result == True:
            conf = Fconfig(CONFIG_FILE)
            db_name = conf.get_db_name()
            car = CarRecorder(name, surname, phone,
                    email, plate, door, db_name)
            car.add_car(CAR_TABLE)
        self.set_view_tab()

    def form_check(self, name, surname, door, plate):
        """checks whether enough data provided to record
        car into database.
        :name: string
        :surname: string
        :door: string
            door number of car owner
        :plate: string
            plate of car
        """
        self.form_warning.setText('')
        if name.isEmpty():
            print 'name empty'
            self.form_warning.setText('Enter Name')
            return False
        if surname.isEmpty():
            self.form_warning.setText('Enter Surname')
            return False
        if door.isEmpty():
            self.form_warning.setText('Enter Door No')
            return False
        if plate.isEmpty():
            self.form_warning.setText('Enter Plate')
            return False
        return True

    def add_form_input(self, layout, lbl_str, box_name,
            x_pos, y_pos, dist):
        """adds label-textbox into widget.
        :layout: QtGui.QVBoxLayout
            layout to add
        :box_name: string
            object name of textbox
        :lbl_str: string
        :wdgt: QWidget
            widget to be append
        :x_pos: int
            x position
        :y_pos: int
            y position
        :dist: int
            distance in between label and input textbox
        """
        label = QtGui.QLabel(lbl_str)
        label.move(x_pos, y_pos)
        layout.addWidget(label)
        self.form_boxes[box_name] = QtGui.QLineEdit()
        self.form_boxes[box_name].move(x_pos+dist, y_pos)
        layout.addWidget(self.form_boxes[box_name])

    def set_view_tab(self):
        """sets view tab, which would be used to
        view database and delete records from database.
        """
        conf = Fconfig(CONFIG_FILE)
        db_name = conf.get_db_name()
        viewer = CarRecorder(name=None, surname=None, phone=None,
                email=None, plate=None, door=None, db_name=db_name)
        car_info = viewer.get_table_info(CAR_TABLE)
        columns = conf.get_table_fields(CAR_TABLE)
        self.view_table.setColumnCount(len(columns))
        self.view_table.setRowCount(len(car_info))
        col_str = ','.join(columns)
        self.view_table.setHorizontalHeaderLabels \
            (QtCore.QString(col_str).split(','))
        self.view_table.resize(700, 600)
        self.tabs.addTab(self.view_tab, "View Cars")
        for i in range(0, len(car_info)):
            for idx, val in enumerate(columns):
                self.view_table.setItem(i, idx, QtGui.QTableWidgetItem(
                    car_info[i][val]))

def main():
    """main function."""
    garage = AppWin()
    garage.tabs.show()
    sys.exit(garage.app.exec_())

if __name__ == '__main__':
    main()
