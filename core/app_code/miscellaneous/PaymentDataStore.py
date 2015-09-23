import datetime
from app_code.miscellaneous.BasicDataStore import BasicDataStore


class PaymentDataStore(BasicDataStore):

    def get_user_by_payment(self, paymentString):
        rows = self.runselect("""SELECT id, firstname, lastname, memberType
        FROM smarterspacebrain.user WHERE paymentString is %s """, (paymentString))
        return rows

