import datetime
from app_code.miscellaneous.BasicDataStore import BasicDataStore


class LogDataStore(BasicDataStore):

    def get_logs(self, from_ts, to_ts):
        rows = self.runselect("""SELECT to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp, system, attribute, message FROM smarterspacebrain.logs """ +
                """WHERE %s <= timestamp AND timestamp <= %s ORDER BY timestamp DESC""", (from_ts+" 00:00:00", to_ts+" 23:59:59.999"))
        return rows

    def addlog(self, system, attr, msg):
        self.runinsert(
            """INSERT INTO smarterspacebrain.logs (timestamp, system, attribute, message) VALUES (%s, %s, %s, %s)""",
            (datetime.now(), system, attr, msg))
