__author__ = 'erwin'
# import app_code.miscellaneous.BasicDataStore as ds

# This file houses some member payment logic
disc = ["Lidgeld", "MemberFee", "lidgeld", "memberfee"]

# https://nl.wikipedia.org/wiki/Genormaliseerd_rekeningstelsel/bijlage#Klasse_7._Opbrengsten

def getIBAN(member_id, action):
    '''
    Generate IBAN(?) code for person depending on action

    '''

    # select
    if action == "subscription":
        act_nr = 705 # 700-707 = omzet
    elif action == "topup":
        act_nr = 431 # promessen
    else:
        act_nr = 407 # Dubieuze debiteuren

    mod = int(str(act_nr) + str(member_id) + "1337") % 97

    code = "%d/%d/1337/%d" % (act_nr, member_id, mod)

    print code

getIBAN(32,"subscription")

# old function, redundant as bank notes are already in the system
def addbanknote(banknote):

    '''
    his function imports a banknote. Needs to be reworked to fit the specific
    strucure of the note.

    Banknote is a structured list with tuples (or lists).
    '''

    for row in banknote:
        # structure of banknode is now made up
        date = row[0]
        name = row[1] # TODO: needs to be sanitized
        amount = row[2]
        description = row[3] # TODO: needs to be sanitized
        member = Member("+++730/0003/00086+++") # TODO: Get user from DB, maybe ask for member nr in description?


        for d in disc:
            if d in description:

                if member.isfull():
                    months = amount / 20 # or a global variable instead of 20
                elif member.isreducted():
                    months = amount / 10

                member.addmonth(name, months)
                # TODO: add function to add rows to banktransactions

def addbanktransaction(row):
    # Function that checks if row already exists in bank transactions, if not, it adds it.
    date = row[0] #TODO: Again, placeholder until real bank transactions are used
    name = row[1]
    db = "sql that asks for all payments on that date"

    for line in db:
        if name in 'line.payee field':
            if disc in 'line.description':
                pass
        # add line to DB


class Member:
    """
    A class to control member payments, is probably partly redundant after
    connecting it to the database and Flask.
    """
    def __init__(self, paymentString):
        # TODO all placeholders, should be linked to DB later on

        row = ds.PGDataStore().get_user_by_payment(paymentString)

        self.id = id
        self.name = "Erwin"
        self.type = "reducted"

    def isfull(self):
        # returns true if a member pay normal fee
        if self.type is "full":
            return True
        else:
            return False

    def isreducted(self):
        # returns true if a member has a reducted fee
        if self.type is "reducted":
            return True
        else:
            return False

    def addmonth(self, months):
        # A function that adds months to the users 'member until' field in the DB

        print "Member %s added %s months and is a member until x" % (self.name, months)




banknote = [
    ["1-1-2015", "Erwin", "30","Lidgeld Erwin"],
    ["1-1-2015", "Bart", "20","Lidgeld Bart"]
]
# addbanknote(banknote)