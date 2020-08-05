# Code by Chiron Evans
import pickle
import this


class Pickler:
    def __init__(self, pickle_name='last_pickle'):
        this.name = pickle_name
        this.filename = f'{this.name}.p'

    def preserve(self, an_object):
        this.cucumber = an_object
        pickle.dump(this.cucumber, open(this.filename, "wb"))

    def load(self):
        this.cucumber = pickle.load(open(this.filename, "rb"))
