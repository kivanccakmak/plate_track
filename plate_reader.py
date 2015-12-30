import subprocess
from car_recorder import CarRecorder
from fconfig import Fconfig

ALPR_INDEX = {}
ALPR_INDEX['plate'] = 1
ALPR_INDEX['confidence'] = -1

FILE_PATH = '/home/kivi/Downloads/plaka.jpg'
CMD = 'alpr -c eu {plate_img}'
CONFIG_FILE = 'config.ini'

def tr_plate_check(plate):
    """Turkey's plate number in format of.
    int(2 char) string(varies) int(varies)
    :plate: string
    :returns: bool and string
        bool -> whether plate is valid for Turkey
        string -> fixed plate number
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
        print "i: {}".format(i)
        print "plate[i]: {}".format(str(plate[i]))
        try:
            val = int(str(plate[i]))
            print "val: {}".format(val)
            str_end = i
        except ValueError:
            print "value error"
        i += 1

    print "str_end: {}".format(str_end)
    for i in range(str_end, len(plate)):
        print "i: {}".format(i)
        if plate[i] == 'O':
            plate[i] = '0'
        else:
            try:
                val = int(plate[i])
            except ValueError:
                return False, ''
    return True, ''.join(plate)

def db_check(plate):
    """ checks database to seek plate.
    :plate: string
        plate number
    """
    conf = Fconfig(CONFIG_FILE)
    db_name = conf.get_db_name()
    records = CarRecorder({}, db_name)
    rows = records.get_plate_records(plate, 'car_info')
    return rows

class PlateRead(object):

    """Plate Reader Class. Process image
    file and returns plate with confidence
    level"""

    def __init__(self, file_path):
        """Initializer function """
        self.file_path = file_path
        self.result = []

    def openalpr_run(self):
        """runs openalpr and returns results in array.
        :file_path: file path to read
        :returns: array
            [[plate, confidence], [], ...]
        """
        plate = ''
        confidence = ''
        alpr_cmd = CMD.format(plate_img=self.file_path)
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
        result = self.openalpr_run()
        print result
        result_info = {}
        if len(result) == 0:
            result_info['conf'] = '0'
            result_info['plate'] = 'NoN'
            return False, result_info

        result_info = {}
        for val in result:
            state, plate = tr_plate_check(str(val['plate']))
            if state:
                rows = db_check(plate)
            else:
                rows = []
            if len(rows) != 0:
                result_info = rows
                return True, result_info
        result_info = result[0]
        return False, result_info

def main():
    """runs open alpr with system call,
    prints output."""
    reader = PlateRead(FILE_PATH)
    result = reader.openalpr_run()
    print result

if __name__ == "__main__":
    main()
