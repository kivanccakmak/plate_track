import ConfigParser
import collections

class Fconfig(object):

    """Docstring for Fconfig. """

    def __init__(self, fname):
        """initiate config file
        :fname: string
            file name of config file
        """
        self._fname = fname

    def get_config(self, section_name):
        """Gets configuration from given section in config.ini.
        :section_name: string
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
        :table: string
        :returns: string array
        """
        field_info = self.get_config('fields')
        fields = field_info[table].split()
        return fields

    def get_db_name(self):
        """get relative path of database
        :returns: string
        """
        db_info = self.get_config('database')
        db_name = db_info['name']
        return db_name

    def get_table_list(self):
        """get table list in database.
        :returns: string array
        """
        table_info = self.get_config('tables')
        table_list = table_info['name'].split()
        return table_list

