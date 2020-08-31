# Code by Chiron Evans
from pickle import load, dump
from os import path


class Pickler:
    def __init__(self, pickle_name='last_pickle'):
        self.name = pickle_name
        self.filename = f'{self.name}.p'

    def preserve(self, an_object):
        with open(self.filename, 'wb') as f:
            dump(an_object, f, 2)

    def load(self):
        if path.isfile(self.filename):
            with open(self.filename, 'rb') as f:
                return load(f)
        return False
