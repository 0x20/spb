from app_code.miscellaneous.BasicDataStore import BasicDataStore


class BankTransactionDataStore(BasicDataStore):

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
