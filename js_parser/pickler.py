# Code by Chiron Evans
from pickle import dump, load
from os import path


class Pickler:
    def __init__(self, pickle_name='last_pickle'):
        self.name = pickle_name
        self.filename = f'{self.name}.p'

    def preserve(self, an_object):
        with open(self.filename, 'w+') as f:
            pickle.dump(an_object, f, 2)

    def load(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                return pickle.load(f)
        return False
