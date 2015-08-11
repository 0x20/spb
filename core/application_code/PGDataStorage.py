from datetime import datetime
import logging
import ConfigParser
from decimal import Decimal

import psycopg2
import psycopg2.extras
from application_code import BrainDataStore


class PGDataStore(BrainDataStore.BrainDataStore):
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
            """SELECT pn.id, pn.user_id, pn.phonenumber, pn.cellphone FROM smarterspacebrain.phonenumbers pn WHERE pn.user_id=%s""",(user_id,))
        return rows

    def getbadgenumbers(self):
        numbers = []
        rows = self.runselect(
            """SELECT bn.badgenumber FROM smarterspacebrain.badgenumbers bn, smarterspacebrain.user u WHERE bn.user_id=u.id AND u.member=true""")
        return numbers

    def get_logs(self, from_ts, to_ts):
        rows = self.runselect("""SELECT to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp, system, attribute, message FROM smarterspacebrain.logs """ +
                """WHERE %s <= timestamp AND timestamp <= %s ORDER BY timestamp DESC""", (from_ts+" 00:00:00", to_ts+" 23:59:59.999"))
        return rows

    def addlog(self, system, attr, msg):
        self.runinsert(
            """INSERT INTO smarterspacebrain.logs (timestamp, system, attribute, message) VALUES (%s, %s, %s, %s)""",
            (datetime.now(), system, attr, msg))

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
            """SELECT password FROM smarterspacebrain.user WHERE username=%s""", (username,))
        if (len(rows) == 1):
            return rows[0]['password'] == password

    def get_transactions(self, from_ts, to_ts):
        rows = self.runselect("""SELECT to_char(bt.valutadatum, 'YYYY-MM-DD') as valutadatum, bt.amount, bt.currency, bt.accountnumber, bt.name, bt.message, an.user_id as userid """ +
                              """FROM smarterspacebrain.banktransactions bt LEFT OUTER JOIN smarterspacebrain.accountnumbers an ON an.accountnumber = bt.accountnumber """ +
                              """WHERE %s <= bt.valutadatum AND bt.valutadatum <= %s """ +
                              """ORDER BY bt.valutadatum DESC""", (from_ts + " 00:00:00", to_ts + " 23:59:59.999"))
        return rows

    def get_transaction_types(self, type_description):
        return self.runselect("""SELECT id FROM smarterspacebrain.banktransactiontypes WHERE description=%s""", [type_description])

    def add_transaction_type(self, type_description):
        self.runinsert("""INSERT INTO smarterspacebrain.banktransactiontypes (description) VALUES (%s)""", [type_description])
        self.logger.info("New bank transaction type: %s", type_description)
        return self.get_transaction_types(type_description)   # return the newly created ID

    def save_bank_transaction(self, bank_transaction):
        rows = self.runselect("""SELECT 1 FROM smarterspacebrain.banktransactions WHERE reference=%s""", [bank_transaction.reference])
        if (len(rows) == 1):
            self.logger.debug("Row found!")
        else:
            types = self.get_transaction_types(bank_transaction.type)
            if (len(types) == 0):
                types = self.add_transaction_type(bank_transaction.type)
            if (len(types) == 1):
                tt_id = types[0]['id']
                self.runinsert("""INSERT INTO smarterspacebrain.banktransactions (valutaDatum,transactiondate,reference,transactiontype_id,amount,""" +
                           """ currency,accountnumber,name,message,message2) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                           [datetime.strptime(bank_transaction.valutaDatum, '%d-%m-%Y'),
                            datetime.strptime(bank_transaction.date, '%d-%m-%Y'),
                            bank_transaction.reference, tt_id,
                            Decimal(bank_transaction.amount.replace('.', '').replace(',', '.')), bank_transaction.currency,
                            bank_transaction.sourceAccount, bank_transaction.name, bank_transaction.message1,
                            bank_transaction.message2]
                           )
            else:
                self.logger.warn("Transaction type not found: %s", bank_transaction.type)

    def get_gatekeeper_schedules(self):
        return self.runselect("""SELECT id, day, starttime, endtime FROM smarterspacebrain.gatekeeperschedules ORDER BY day, starttime""", [])

    def delete_schedule(self, id):
        self.runinsert("""DELETE FROM smarterspacebrain.gatekeeperschedules WHERE id=%s""", [id])

    def add_schedule(self, day, from_ts, to_ts):
        self.logger.debug("new schedule (%s, %s, %s)", [day, from_ts, to_ts])
        self.runinsert("""INSERT INTO smarterspacebrain.gatekeeperschedules (day, starttime, endtime) VALUES (%s, %s, %s)""", [day, from_ts, to_ts])

    def get_gatekeeper_whitelist(self):
        schedules = self.get_gatekeeper_schedules()
        phonenos = self.runselect("""SELECT pn.phonenumber, u.firstname, u.lastname FROM smarterspacebrain.phonenumbers pn, smarterspacebrain.user u WHERE pn.user_id=u.id AND pn.cellphone='TRUE' AND u.member=true""")
        lines = []
        for schedule in schedules:
            lines.append('* %s %s %s' % (schedule['day'], schedule['starttime'], schedule['endtime']))
        for phoneno in phonenos:
            phonenumber = phoneno['phonenumber']
            if (phonenumber.startswith("0", 0, 1)):
                phonenumber = phonenumber.replace("0", "32", 1)
            lines.append('%s %s %s' % (phonenumber, phoneno['firstname'], phoneno['lastname']))
        return lines


    # Stock management functions
    def getproducts(self, user_id):
        rows = self.runselect(
            # TODO: change query in something original
             """SELECT pn.id, pn.user_id, pn.phonenumber, pn.cellphone FROM smarterspacebrain.phonenumbers pn WHERE pn.user_id=%s""",(user_id,))
        return rows

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

