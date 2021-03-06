from app_code.miscellaneous.BasicDataStore import BasicDataStore


# Inherit actual database connection code from BasicDataStore
class AccessDataStore(BasicDataStore):

    def getgsmnumbers(self):
        numbers = []
        rows = self.runselect(
            """SELECT pn.phonenumber FROM smarterspacebrain.phonenumbers pn, smarterspacebrain.user u WHERE pn.user_id=u.id AND pn.cellphone='TRUE' AND u.member=true""")
        for row in rows:
            numbers.append(row['phonenumber'])
        return numbers

    def getbadgenumbers(self):
        numbers = []
        rows = self.runselect(
            """SELECT bn.badgenumber FROM smarterspacebrain.badgenumbers bn, smarterspacebrain.user u WHERE bn.user_id=u.id AND u.member=true""")
        for row in rows:
            numbers.append(row['badgenumber'])
        return numbers

    def get_badgereader_whitelist(self):
        badgenos = self.runselect(
            """SELECT bn.badgenumber, u.firstname, u.lastname FROM smarterspacebrain.badgenumbers bn, smarterspacebrain.user u WHERE bn.user_id=u.id AND u.member=true""")
        lines = []
        for badgeno in badgenos:
            bn = badgeno['badgenumber']
            lines.append('%s %s %s' % (badgeno['badgenumber'], badgeno['firstname'], badgeno['lastname']))
        return lines

    def get_gatekeeper_schedules(self):
        return self.runselect("""SELECT id, day, starttime, endtime FROM smarterspacebrain.gatekeeperschedules ORDER BY day, starttime""", [])

    def delete_schedule(self, id):
        self.runinsert("""DELETE FROM smarterspacebrain.gatekeeperschedules WHERE id=%s""", [id])

    def add_schedule(self, day, from_ts, to_ts):
        self.logger.debug("new schedule (%s, %s, %s)", [day, from_ts, to_ts])
        self.runinsert("""INSERT INTO smarterspacebrain.gatekeeperschedules (day, starttime, endtime) VALUES (%s, %s, %s)""", [day, from_ts, to_ts])

    def get_gatekeeper_whitelist(self):
        schedules = self.get_gatekeeper_schedules()
        phonenos = self.runselect("""SELECT pn.phonenumber, u.firstname, u.lastname, u.nick FROM smarterspacebrain.phonenumbers pn, smarterspacebrain.user u WHERE pn.user_id=u.id AND pn.cellphone='TRUE' AND u.member=true""")
        lines = []
        for schedule in schedules:
            lines.append('* %s %s %s' % (schedule['day'], schedule['starttime'], schedule['endtime']))
        for phoneno in phonenos:
            phonenumber = phoneno['phonenumber']
            if (phonenumber.startswith("0", 0, 1)):
                phonenumber = phonenumber.replace("0", "32", 1)
            name = phoneno['firstname'] + " " + phoneno['lastname']
            if ((phoneno['nick'] is not None) and (phoneno['nick'] != '')):
                name = phoneno['nick']
            lines.append('%s %s' % (phonenumber, name))
        return lines

