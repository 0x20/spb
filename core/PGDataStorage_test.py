#!bin/python

from application_code.PGDataStorage import PGDataStore

s = PGDataStore()

types = s.get_transaction_types("Uw interest berekening")
print(len(types))
print(types[0]['id'])