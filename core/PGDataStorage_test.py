#!bin/python

from application_code.PGDataStorage import PGDataStore

s = PGDataStore()


def find_type_test():
    print("-=-=- find_type_test -=-=-")
    types = s.get_transaction_types("Uw interest berekening")
    print(len(types))
    print(types[0]['id'])


def add_type_test():
    print("-=-=- add_type_test -=-=-")
    types = s.add_transaction_type("test")
    print(len(types))
    print(types[0]['id'])


def find_schedules_test():
    print("-=-=- find_schedules_test -=-=-")
    schedules = s.get_gatekeeper_schedules()
    for schedule in schedules:
        print('- %s %s %s %s' %(schedule['id'],schedule['day'],schedule['starttime'],schedule['endtime']))


find_type_test()
#add_type_test()
find_schedules_test()