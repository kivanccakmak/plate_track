import subprocess

ALPR_INDEX = {}
ALPR_INDEX['plate'] = 1
ALPR_INDEX['confidence'] = -1

FILE_PATH = '/home/kivi/Downloads/plaka.jpg'
CMD = 'alpr -c eu {plate_img}'

class PlateRead(object):

    """Plate Reader Class. Process image
    file and returns plate with confidence
    level"""

    def __init__(self, file_path):
        """Initializer function """
        self.file_path = file_path

    def openalpr_run(self):
        """runs openalpr and returns results in array.
        :file_path: file path to read
        :returns: array
            [[plate, confidence], [], ...]
        """
        result = []
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
                result.append({'conf': confidence, 'plate': plate})
        return result

def main():
    """runs open alpr with system call,
    prints output."""
    reader = PlateRead(FILE_PATH)
    result = reader.openalpr_run()
    print result

if __name__ == "__main__":
    main()
