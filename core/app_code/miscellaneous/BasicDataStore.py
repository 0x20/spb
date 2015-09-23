from datetime import datetime
import logging
import ConfigParser
import psycopg2
import psycopg2.extras

# BasicDataStore is a base class that implements a couple of common database access methods for all
# modules:
# - run a SELECT query (which returns an array of rows)
# - run an INSERT/UPDATE/DELETE query (which returns nothing)
class BasicDataStore(object):

    conn_string = ""
    logger = None

    def __init__(self):
        super(BasicDataStore, self).__init__()
        self.logger = logging.getLogger('pg_ds   ')
        # Read database access configuration from file 'main.ini'
        config = ConfigParser.ConfigParser()
        config.read("main.ini")
        self.conn_string = "host='" + config.get('DatabaseConfig', 'host') + "' dbname='" + config.get('DatabaseConfig',
                                                                                                       'dbname') + "' " \
                                                                                                                   "user='" + config.get(
            'DatabaseConfig', 'user') + "' password='" + config.get('DatabaseConfig', 'password') + "'"
        self.logger.debug("Connection string: %s", self.conn_string)

    def runselect(self, query, values = None):
        rows = []
        try:
            self.logger.debug("Select query [%s]", query)
            conn = psycopg2.connect(self.conn_string)
            #cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query, values)
            rows = cur.fetchall()
        except StandardError as e:
            print e.message
        return rows

    def runinsert(self, query, values):
        try:
            self.logger.debug("Insert query [%s]", query)
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query, values)
            conn.commit()
        except StandardError as e:
            print e.message

