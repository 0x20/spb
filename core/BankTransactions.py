#!bin/python
import csv
import BankTransaction
from PGDataStorage import PGDataStore

storage = PGDataStore()


class BankTransactions(object):

    def read(self, fileName):
        with open(fileName, 'rb') as csvfile:
            rowreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in rowreader:
                bt = BankTransaction.BankTransaction()
                if (len(row) >= 9):
                    bt.valutaDatum = row[0]
                    bt.reference = row[1]
                    bt.type = row[2]
                    bt.amount = row[3]
                    bt.currency = row[4]
                    bt.date = row[5]
                    bt.sourceAccount = row[6]
                    bt.name = row[7]
                    bt.message1 = row[8]
                    bt.message2 = row[9]
                    storage.save_bank_transaction(bt)


if __name__ == '__main__':
    bt = BankTransactions()
    bt.read('testdata/2014-12-21_20:48:35_20141009_20141216_BE15973004306430.csv')
