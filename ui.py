from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from src.car_recorder import CarRecorder
from src.fconfig import Fconfig
from src.fconfig import parse_dict 
from src.fconfig import parse_dict_arr
from src.plate_reader import PlateRead
import sys
import os
import ast

CONFIG_FILE = 'src/config.ini'
CAR_TABLE = 'car_info'

class AppWin(object):
    """Application UI Class."""
    def __init__(self):
        """init function."""
        self.conf = Fconfig(CONFIG_FILE)
        max_x = int(self.conf.get_config('tabs')['max_x'])
        max_y = int(self.conf.get_config('tabs')['max_y'])
        title = self.conf.get_config('tabs')['title']

        self.app = QtGui.QApplication(sys.argv)
        self.tabs = QtGui.QTabWidget()
        self.tabs.setWindowTitle(title)
        self.tabs.setMinimumSize(max_x, max_y)

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
        self.file_dialog = QtGui.QFileDialog()
        self.process_content = QtGui.QTextEdit()
        self.plate_img_path = ''
        self.set_process_tab()

    def set_form_tab(self):
        """sets input form which would be used to
        enter new car into database.
        """
        elements = self.conf.get_config('form')['elements']
        x_pos = int(self.conf.get_config('form')['elem_x_init'])
        y_pos = int(self.conf.get_config('form')['elem_y_init'])
        y_incr = int(self.conf.get_config('form')['y_dist'])
        warn_x_pos = int(self.conf.get_config('form')['warning_x'])
        warn_y_pos = int(self.conf.get_config('form')['warning_y'])
        btn_x_pos = int(self.conf.get_config('form')['button_x'])
        btn_y_pos = int(self.conf.get_config('form')['button_y'])

        elem_list = parse_dict_arr(elements)

        for elem in elem_list:
            key = elem.keys()[0]
            val = elem.values()[0]
            self.add_form_input(val, key, x_pos, y_pos)
            y_pos += y_incr

        self.form_warning.move(warn_x_pos, warn_y_pos)
        self.form_button.move(btn_x_pos, btn_y_pos)
        self.form_button.connect(self.form_button,
                QtCore.SIGNAL('clicked()'), self.form_btn_click)
        self.form_tab.setLayout(self.form_layout)
        self.tabs.addTab(self.form_tab, "New Car")

    def set_process_tab(self):
        """sets image processing tab. image would be chosen by document
        window, then openalpr would be run
        """
        max_x = int(self.conf.get_config('process')['content_max_x'])
        max_y = int(self.conf.get_config('process')['content_max_y'])
        self.process_layout.addWidget(self.process_label)
        self.process_layout.addWidget(self.process_btn)
        self.process_layout.addWidget(self.fopen_btn)
        self.process_content.setMaximumSize(max_x, max_y)
        self.process_content.setReadOnly(True)
        self.process_layout.addWidget(self.process_content)
        self.process_tab.setLayout(self.process_layout)
        self.fopen_btn.clicked.connect(self.getfile)
        self.process_btn.clicked.connect(self.read_plate)
        self.tabs.addTab(self.process_tab, "Process Cars")

    def getfile(self):
        """ opens file browser and pixmap. on process button click,
        trigs plate reading.
        """
        fname = self.file_dialog.getOpenFileName(None, 'Open File',
                '/', 'Image Files (*.jpg *.png)')
        self.plate_img_path = str(fname)
        pixmap = QtGui.QPixmap(fname)
        pixmap = pixmap.scaled(625, 500)
        self.process_label.setPixmap(pixmap)

    def read_plate(self):
        """ reads plate and returns result to content
        """
        plate = PlateRead(self.plate_img_path, CONFIG_FILE)
        self.process_content.setText('')
        status, result = plate.plate_check()
        print "result: {}".format(result)
        if status:
            self.process_content.setStyleSheet("QTextEdit {color:green}")
            self.print_dict_res(result)
        else:
            self.process_content.setStyleSheet("QTextEdit {color:red}")
            if str(result['plate']) == 'NoN':
                self.process_content.insertPlainText('Read Failed')
            else:
                self.process_content.insertPlainText('Not in Garage\n')
                self.print_dict_res(result)

    def print_dict_res(self, dict_res):
        """ prints output in a key: val format to content
        :dict_res: dictionary
        """
        msg = '{key}: {val}'
        msg_val = ''
        for key in dict_res.keys():
            msg_val = msg.format(key=key,
                    val=dict_res[key])
            msg_val += '\n'
            self.process_content.insertPlainText(msg_val)


    def form_btn_click(self):
        """checks textboxes of form, if name, surname, door and
        plate number is provided; adds car into database
        """
        elem_list = {}
        keys = self.form_boxes.keys()
        for key in keys:
            elem_list[key] = self.form_boxes[key].text()
        result = self.form_check(elem_list)
        if result == True:
            conf = Fconfig(CONFIG_FILE)
            db_name = conf.get_db_name()
            car = CarRecorder(elem_list, db_name)
            car.add_car(CAR_TABLE)
        self.set_view_tab()

    def form_check(self, elem_list):
        """checks whether enough data provided to record
        car into database.
        :elem_list: dict
            collected from form boxes
        :return: bool
            if all filled True, otherwise False
        """
        warn_str = 'Enter {field}'
        self.form_warning.setText('')
        for key in elem_list.keys():
            val = elem_list[key]
            if val.isEmpty():
                warn_str = warn_str.format(field=key)
                self.form_warning.setText(warn_str)
                return False
        return True

    def add_form_input(self, lbl_str, box_name, x_pos, y_pos):
        """adds label-textbox into widget.
        :box_name: string
            object name of textbox
        :lbl_str: string
        :wdgt: QWidget
            widget to be append
        :x_pos: int
            x position
        :y_pos: int
            y position
        """
        label = QtGui.QLabel(lbl_str)
        label.move(x_pos, y_pos)
        self.form_layout.addWidget(label)
        self.form_layout.addWidget(label)
        self.form_boxes[box_name] = QtGui.QLineEdit()
        self.form_boxes[box_name].move(x_pos, y_pos)
        self.form_layout.addWidget(self.form_boxes[box_name])

    def set_view_tab(self):
        """sets view tab, which would be used to
        view database and delete records from database.
        """
        x_size = \
            int(self.conf.get_config('view')['table_size_x'])
        y_size = \
            int(self.conf.get_config('view')['table_size_y'])
        db_name = self.conf.get_db_name()
        viewer = CarRecorder(credentials={}, db_name=db_name)
        car_info = viewer.get_table_info(CAR_TABLE)
        columns = self.conf.get_table_fields(CAR_TABLE)
        self.view_table.setColumnCount(len(columns))
        self.view_table.setRowCount(len(car_info))
        col_str = ','.join(columns)
        self.view_table.setHorizontalHeaderLabels \
            (QtCore.QString(col_str).split(','))
        self.view_table.resize(x_size, y_size)
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
