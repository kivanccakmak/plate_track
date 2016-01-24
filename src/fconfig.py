import ConfigParser
import collections
import ast

def parse_dict(str_val):
    """Parses dict str from .ini file.
    :str_val: str
        '{'key1':'val1'}\n{'key2':'val2'}'
    :returns: dictionary
        {'key1':'val1', 'key2':'val2'}
    """
    elem_list = {}
    current = {}
    elements = str_val.split()
    for elem in elements:
        current = ast.literal_eval(elem)
        key = current.keys()[0]
        val = current.values()[0]
        elem_list[key] = val
    return elem_list

def parse_dict_arr(str_val):
    """Parses dict array str from .ini file.
    :str_val: str
        '{'key1':'val1'}\n{'key2':'val2'}'
    :returns: arr
        contains dictionaries as follows
        [{'key1':'val1'}, {'key2':'val2'}]
    """
    elem_arr = []
    elements = str_val.split()
    for elem in elements:
        elem_arr.append(ast.literal_eval(elem))
    return elem_arr

class Fconfig(object):

    """Hard Coded Configuration Parser. """

    def __init__(self, fname):
        """initiate config file
        :fname: str
            file name of config file
        """
        self._fname = fname

    def get_config(self, section_name):
        """Gets configuration from given section in config.ini.
        :section_name: str
            Name of the section
        :returns: dict
        """
        config_map = collections.OrderedDict()
        parser = ConfigParser.SafeConfigParser()
        parser.read(self._fname)

        for name, value in parser.items(section_name):
            config_map[name] = value

        return config_map

    def get_table_fields(self, table):
        """get field list of table
        :table: str
        :returns: arr
            contains strings
        """
        field_map = self.get_config('field_map')[table]
        field_map = field_map.split(',')
        field_info = self.get_config(field_map[0])[field_map[1]]
        field_info = parse_dict(field_info).keys()
        return field_info

    def get_db_name(self):
        """get relative path of database
        :returns: str
        """
        db_info = self.get_config('database')
        db_name = db_info['name']
        return db_name

