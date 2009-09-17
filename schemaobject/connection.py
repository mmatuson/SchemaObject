import MySQLdb
import re

REGEX_RFC1738 = re.compile(r'''
            (?P<protocol>\w+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>[^/]*))?
            @)?
            (?:
                (?P<host>[^/:]*)
                (?::(?P<port>[^/]*))?
            )?
            (?:/(?P<database>.*))?
            ''', re.X)


def parse_database_url(url):
    matches = REGEX_RFC1738.match(url)
    result = {}

    if matches:
        if matches.group('username'):
            result['user'] = matches.group('username')

        if matches.group('password'):
            result['passwd'] = matches.group('password')

        if matches.group('database'):
            result['db'] = matches.group('database')

        if matches.group('host'):
            result['host'] = matches.group('host')

        try:
            result['port'] = int(matches.group('port'))
        except (TypeError, ValueError):
            pass

    return result


class DatabaseConnection(object):
    """A lightweight wrapper around MySQLdb DB-API"""

    def __init__(self, connection_url):

        if not "mysql://" in connection_url.lower():
            raise TypeError("Connection protocol must be MySQL!")

        self._kwargs = parse_database_url(connection_url)
        self._db = None

        self.db = self._kwargs.get('db', None)
        self.host = self._kwargs.get('host', 'localhost')
        self.port = self._kwargs.get('port', 3306)
        self.user = self._kwargs.get('user', None)
        self.connect()

    @property
    def version(self):
        result = self.execute("SELECT VERSION() as version")
        return result[0]['version']

    def execute(self, sql, values=None):
        cursor = self._db.cursor()
        cursor.execute(sql, values)

        if not cursor.rowcount:
            return None

        fields = [field[0] for field in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        return  [dict(zip(fields, row)) for row in rows]

    def connect(self):
        """Connect to the databse"""
        self._db = MySQLdb.connect(**self._kwargs)

    def close(self):
        """Close the database connection."""
        if self._db is not None:
            self._db.close()

    def __del__(self):
        self.close()

# Alias MySQL exception
DatabaseError = MySQLdb.Error
