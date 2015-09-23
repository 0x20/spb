import datetime
from app_code.miscellaneous.BasicDataStore import BasicDataStore


class LoginDataStore(BasicDataStore):

    def login(self, username, password):
        rows = self.runselect(
            """SELECT password FROM smarterspacebrain.user WHERE username=%s""", (username,))
        if (len(rows) == 1):
            return rows[0]['password'] == password

