from app_code.miscellaneous.BasicDataStore import BasicDataStore


class UsersDataStore(BasicDataStore):

    def getusers(self):
        rows = self.runselect(
            """SELECT u.id as id, u.firstname as firstname, u.lastname, u.nick, u.city, u.country, u.member FROM smarterspacebrain.user u ORDER BY u.lastname, u.firstname""")
        return rows

    def updateuser(self, id, firstname, lastname, nickname, member):
        if (id == "-1"):
            self.runinsert(
                """INSERT INTO smarterspacebrain.user (firstname, lastname, nick, city, country, member) VALUES (%s, %s, %s, '', '', %s)""",
                (firstname, lastname, nickname, member))
        else:
            self.runinsert(
                """UPDATE smarterspacebrain.user SET firstname=%s, lastname=%s, nick=%s, member=%s WHERE id=%s""",
                (firstname, lastname, nickname, member, id))

    def deleteuser(self, id):
        self.runinsert(
            """DELETE FROM smarterspacebrain.phonenumbers WHERE user_id=%s""", [id])
        self.runinsert(
            """DELETE FROM smarterspacebrain.user WHERE id=%s""", [id])

    def getphonenumbers(self, user_id):
        rows = self.runselect(
            """SELECT pn.id, pn.user_id, pn.phonenumber, pn.cellphone FROM smarterspacebrain.phonenumbers pn WHERE pn.user_id=%s""",(user_id,))
        return rows

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

