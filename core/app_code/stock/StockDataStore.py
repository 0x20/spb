import datetime
from app_code.miscellaneous.BasicDataStore import BasicDataStore


class StockDataStore(BasicDataStore):

    # Stock management functions
    def getproducts(self, user_id):
        rows = self.runselect(
            # TODO: change query in something original
             """SELECT pn.id, pn.user_id, pn.phonenumber, pn.cellphone FROM smarterspacebrain.phonenumbers pn WHERE pn.user_id=%s""",(user_id,))
        return rows

