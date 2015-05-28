
class BankTransaction(object):

    def _setValutaDatum(self, valutaDatum=None):
        self._valutaDatum = valutaDatum

    def _getValutaDatum(self):
        return self._valutaDatum

    def _setReference(self, reference=None):
        self._reference = reference

    def _getReference(self):
        return self._reference

    def _setType(self, type=None):
        self._type = type

    def _getType(self):
        return self._type

    def _setAmount(self, amount=None):
        self._amount = amount

    def _getAmount(self):
        return self._amount

    def _setCurrency(self, currency=None):
        self._currency = currency

    def _getCurrency(self):
        return self._currency

    def _setDate(self, date=None):
        self._date = date

    def _getDate(self):
        return self._date

    def _setSourceAccount(self, sourceAccount=None):
        self._sourceAccount = sourceAccount

    def _getSourceAccount(self):
        return self._sourceAccount

    def _setName (self, name=None):
        self._name = name

    def _getName(self):
        return self._name

    def _setMessage1(self, message1=None):
        self._message1 = message1

    def _getMessage1(self):
        return self._message1

    def _setMessage2(self, message2=None):
        self._message2 = message2

    def _getMessage2(self):
        return self._message2


    valutaDatum = property(_getValutaDatum, _setValutaDatum)
    reference = property(_getReference, _setReference)
    type = property(_getType, _setType)
    amount = property(_getAmount, _setAmount)
    currency = property(_getCurrency, _setCurrency)
    date = property(_getDate, _setDate)
    sourceAccount = property(_getSourceAccount, _setSourceAccount)
    name = property(_getName, _setName)
    message1 = property(_getMessage1, _setMessage1)
    message2 = property(_getMessage2, _setMessage2)
