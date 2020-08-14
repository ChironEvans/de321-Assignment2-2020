# Code by Chiron Evans
import pickle


class Pickler:
    def __init__(self, pickle_name='last_pickle'):
        self.name = pickle_name
        self.filename = f'{self.name}.p'

    def preserve(self, an_object):
        self.cucumber = an_object
        pickle.dump(self.cucumber, open(self.filename, "wb"))

    def load(self):
        self.cucumber = pickle.load(open(self.filename, "rb"))
