from abc import ABCMeta, abstractmethod


class AnalyserFactoryMethod(metaclass=ABCMeta):
    @abstractmethod
    def make_analyser(self, analyser_type):
        raise NotImplementedError()
