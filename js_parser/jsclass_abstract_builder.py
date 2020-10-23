from abc import abstractmethod

from js_parser.AnalyserFactoryMethod import AnalyserFactoryMethod
from js_parser.searcher import Searcher
from js_parser.js_class import JSClass


class JSClassAbstractBuilder(AnalyserFactoryMethod):
    def __init__(self, input_string):
        self.js_class = JSClass()
        self.input_string = input_string

    @abstractmethod
    def add_name(self):
        pass

    @abstractmethod
    def add_attributes(self):
        pass

    @abstractmethod
    def add_methods(self):
        pass

    @abstractmethod
    def add_associations(self):
        pass

    def make_analyser(self, analyser_type):
        if analyser_type == 'class_name':
            return Searcher("class\s\w{3,}",  "class ")
        if analyser_type == 'attribute':
            return Searcher("this.\w+", "this.")
        if analyser_type == 'method':
            return Searcher("\n\s{2}\w{2,}\s\(.*\)", "\n  ")
        if analyser_type == 'association':
            return Searcher("new\s\w{3,}", "new ")
        else:
            return None
