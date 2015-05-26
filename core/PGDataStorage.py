import psycopg2
import psycopg2.extras
import datetime
import logging
import ConfigParser
from BrainDataStore import BrainDataStore


class PGDataStore(BrainDataStore):
    # public methods

    def getgsmnumbers(self):
        numbers = []
        rows = self.runselect(
            """SELECT pn.phonenumber FROM smarterspacebrain.phonenumbers pn, smarterspacebrain.user u WHERE pn.user_id=u.id AND pn.cellphone='TRUE' AND u.member=true""")
        for row in rows:
            numbers.append(row['phonenumber'])
        return numbers

    def getphonenumbers(self, user_id):
        rows = self.runselect(
            """SELECT pn.id, pn.user_id, pn.phonenumber, pn.cellphone FROM smarterspacebrain.phonenumbers pn WHERE pn.user_id=""" + user_id)
        return rows

    def getbadgenumbers(self):
        numbers = []
        rows = self.runselect(
            """SELECT bn.badgenumber FROM smarterspacebrain.badgenumbers bn, smarterspacebrain.user u WHERE bn.user_id=u.id AND u.member=true""")
        return numbers

    def get_logs(self, from_ts, to_ts):
        rows = self.runselect("""SELECT to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp, system, attribute, message FROM smarterspacebrain.logs """ +
                              """WHERE '""" + from_ts + """ 00:00:00' <= timestamp AND timestamp <= '""" + to_ts + """ 23:59:59.999' ORDER BY timestamp DESC""")
        return rows

    def addlog(self, system, attr, msg):
        self.runinsert(
            """INSERT INTO smarterspacebrain.logs (timestamp, system, attribute, message) VALUES (%s, %s, %s, %s)""",
            (datetime.datetime.now(), system, attr, msg))

    def getusers(self):
        rows = self.runselect(
            """SELECT u.id as id, u.firstname as firstname, u.lastname, u.city, u.country, u.member FROM smarterspacebrain.user u ORDER BY u.lastname, u.firstname""")
        return rows

    def updateuser(self, id, firstname, lastname, member):
        if (id == "-1"):
            self.runinsert(
                """INSERT INTO smarterspacebrain.user (firstname, lastname, city, country, member) VALUES (%s, %s, '', '', %s)""",
                (firstname, lastname, member))
        else:
            self.runinsert(
                """UPDATE smarterspacebrain.user SET firstname=%s, lastname=%s, member=%s WHERE id=%s""",
                (firstname, lastname, member, id))

    def deleteuser(self, id):
        self.runinsert(
            """DELETE FROM smarterspacebrain.phonenumbers WHERE user_id=%s""", [id])
        self.runinsert(
            """DELETE FROM smarterspacebrain.user WHERE id=%s""", [id])

    def updatephonenumber(self, id, user_id, phonenumber, cellphone):
        if (id == "-1"):
            self.runinsert(
                """INSERT INTO smarterspacebrain.phonenumbers (user_id, phonenumber, cellphone) VALUES (%s, %s, %s)""",
                (user_id, phonenumber, cellphone))
        else:
            self.runinsert(
                """UPDATE smarterspacebrain.phonenumbers SET phonenumber=%s, user_id=%s, cellphone=%s WHERE id=%s""",
                (phonenumber, user_id, cellphone, id))

    def deletephonenumber(self, id):
        self.runinsert(
            """DELETE FROM smarterspacebrain.phonenumbers WHERE id=%s""", [id])

    def setusernamepassword(self, id, username, password):
        self.runinsert(
            """UPDATE smarterspacebrain.user SET username=%s, password=%s WHERE id=%s""", [username, password, id])

    def login(self, username, password):
        rows = self.runselect(
            """SELECT password FROM smarterspacebrain.user WHERE username='""" + username + """'""")
        if (len(rows) == 1):
            return rows[0]['password'] == password

    # private helper methods

    conn_string = ""
    logger = None

    def __init__(self):
        super(PGDataStore, self).__init__()
        self.logger = logging.getLogger('pg_ds   ')
        # Read database access configuration from file 'main.ini'
        config = ConfigParser.ConfigParser()
        config.read("main.ini")
        self.conn_string = "host='" + config.get('DatabaseConfig', 'host') + "' dbname='" + config.get('DatabaseConfig',
                                                                                                       'dbname') + "' " \
                                                                                                                   "user='" + config.get(
            'DatabaseConfig', 'user') + "' password='" + config.get('DatabaseConfig', 'password') + "'"
        self.logger.debug("Connection string: %s", self.conn_string)

    def runselect(self, query):
        rows = []
        try:
            self.logger.debug("Select query [%s]", query)
            conn = psycopg2.connect(self.conn_string)
            #cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query)
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

