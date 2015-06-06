import logging
from os import walk, rename
from BankTransactions import BankTransactions

logger = logging.getLogger('csv loader')


class BankTransactionLoader(object):

    def __init__(self, path, archivepath):
        self.path = path
        self.archivepath = archivepath

    def check_files(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        for filename in f:
            self.csv_file_loader(filename)

    def csv_file_loader(self, filename):
        logger.info("Loading bank CSV file [" + filename + "]")
        full_name = self.path + '/' + filename
        full_new_name = self.archivepath + '/' + filename
        # Move transaction file to archive
        rename(full_name, full_new_name)
        # Load transactions into database
        bt = BankTransactions()
        bt.read(full_new_name)

