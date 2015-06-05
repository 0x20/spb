

# Describes the API to be implemented by the storage component
class BrainDataStore(object):

    def __init__(self):
        return

    def getgsmnumbers(self):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'getgsmnumbers'.")

    def getphonenumbers(self, user_id):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'getphonenumbers'.")

    def getbadgenumbers(self):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'getbadgenumbers'.")

    def addlog(self, sys, attr, msg):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'addlog'.")

    def getusers(self):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'getusers'.")

    def updateuser(self, id, firstname, lastname, member):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'updateuser'.")

    def deleteuser(self, id, firstname, lastname, member):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'deleteuser'.")

    def updatephonenumber(self, id, user_id, phonenumber, cellphone):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'updatephonenumber'.")

    def deletephonenumber(self, id):
        raise NotImplemented("Subclasses of BrainDataStore should implement method 'deletephonenumber'.")

