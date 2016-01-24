class Query:

    """returns sql queries to manipulate tables."""

    @staticmethod
    def get_create_qry(tbl_name, fields):
        """returns table create query.
        :tbl_name: str
            table to be created into db
        :fields: str array
            fields in table
        :returns: str
            create query
        """
        query = 'CREATE TABLE [{tbl}] {fields}'
        column_str = ''
        for idx, val in enumerate(fields):
            if idx == 0:
                column_str += val
            else:
                column_str += ',' + val
        column_str = '(' + column_str + ')'
        query = query.format(tbl=tbl_name,
                fields=column_str)
        return query

    @staticmethod
    def get_add_qry(info, table_name):
        """returns sql insert query.
        :table_name: str
        :info: dict
            keywords(str) are columns
            values(str) are values
            to be inserted into tables
            info = {'col1': 'val1', 'col2': 'val2'}
        :returns: str
            insert query
        """
        query = ''
        vals = ''
        cols = ''
        column_names = info.keys()
        for idx, name in enumerate(column_names):
            if idx == 0:
                vals += '"' + info[name] + '"'
                cols += '"' + name + '"'
            else:
                vals += ',' + '"' + info[name] + '"'
                cols += ',' + '"' + name + '"'
        query = 'INSERT INTO [{tbl}] ({cols}) VALUES ({vals})'
        query = query.format(tbl=table_name,
                cols=cols,
                vals=vals)
        return query

    @staticmethod
    def get_delete_qry(info, table_name):
        """returns sql delete query with respect.
        assumes that info dict contains single key
        :info: dict
        :table_name: str
        :returns: str
        """
        key = info.keys()[0]
        val = info[key]
        query = 'DELETE FROM [{tbl}] WHERE' +\
                ' ' + '"{key}"="{val}"'
        query = query.format(
                tbl=table_name,
                key=key,
                val=val
                )
        return query
