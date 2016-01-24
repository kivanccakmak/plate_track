#!/usr/bin/python
"""
OpenAlpr Using and DataBase Connecting
Module
"""
import subprocess
import sys
from car_recorder import CarRecorder
from fconfig import Fconfig

ALPR_INDEX = {}
ALPR_INDEX['plate'] = 1
ALPR_INDEX['confidence'] = -1

class PlateRead(object):

    """Plate Reader Class. Process image
    file and returns plate with confidence
    level"""

    def __init__(self, img_path, conf_path):
        """Initializer function
        :img_path: str
            path of image to process
        :conf_path: str
            path to config file which contains
            hard-coded parts
        """
        self.img_path = img_path
        self.result = []
        self.conf = Fconfig(conf_path)

    def openalpr_run(self):
        """runs openalpr and returns results in array.
        :file_path: str
            file path to read
        :returns: array
            [[plate, confidence], [], ...]
        """
        plate = ''
        confidence = ''
        alpr_cmd = self.conf.get_config('CMD')['run']
        alpr_cmd = alpr_cmd.format(plate_img=self.img_path)
        print alpr_cmd
        proc = subprocess.Popen([alpr_cmd], \
                stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out_lines = out.split('\n')
        for idx, line in enumerate(out_lines):
            if idx != 0 and idx != len(out_lines) - 1:
                plate = line.split()[ALPR_INDEX['plate']]
                confidence = line.split()[ALPR_INDEX['confidence']]
                self.result.append(
                        {'conf': confidence, 'plate': plate}
                        )
        return self.result

    def plate_check(self):
        """
        returns: bool
            whether plate exist in database
        returns: arr
            openalr estimates
        """
        result = self.openalpr_run()
        result_info = {}
        if len(result) == 0:
            result_info['conf'] = '0'
            result_info['plate'] = 'NoN'
            return False, result_info

        for val in result:
            state, plate = PlateRead.tr_plate_check(str(val['plate']))
            if state:
                rows = self.db_check(plate)
            else:
                rows = []
            if len(rows) != 0:
                result_info = rows[0]
                return True, result_info
        result_info = result[0]
        return False, result_info

    @staticmethod
    def tr_plate_check(plate):
        """Turkey's plate number in format of.
        int(2 char) string(varies) int(varies)
        :plate: string
        :returns: bool
            whether plate is valid for Turkey
        :returns: str
            fixed plate number
        """
        plate = list(plate)
        if str(plate[0]) == 'O':
            plate[0] = '0'
        if str(plate[1]) == 'O':
            plate[1] = '0'
        try:
            val = int(plate[0])
        except ValueError:
            return False, ''
        try:
            val = int(plate[1])
        except ValueError:
            return False, ''

        i = 2
        str_end = -1
        while i < len(plate) and str_end == -1:
            try:
                val = int(str(plate[i]))
                str_end = i
            except ValueError:
                pass
            i += 1

        for i in range(str_end, len(plate)):
            if plate[i] == 'O':
                plate[i] = '0'
            else:
                try:
                    val = int(plate[i])
                except ValueError:
                    return False, ''
        return True, ''.join(plate)

    def db_check(self, plate):
        """ checks database to seek plate.
        :plate: str
            plate number
        """
        db_name = ''
        db_name = self.conf.get_db_name()
        records = CarRecorder({}, db_name)
        rows = records.get_plate_records(plate, 'car_info')
        return rows

def main():
    """runs open alpr with system call,
    prints output."""
    img_path = '/home/kivi/Downloads/plaka.jpg'
    conf_path = 'config.ini'
    conf = Fconfig(conf_path)
    alpr_cmd = conf.get_config('CMD')['run']
    alpr_cmd = alpr_cmd.format(plate_img=img_path)
    reader = PlateRead(img_path, conf_path)
    result = reader.openalpr_run()
    print result

if __name__ == "__main__":
    main()
