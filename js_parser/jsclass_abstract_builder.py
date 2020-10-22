from abc import ABCMeta, abstractmethod

from js_parser.file_splitter import Splitter
from js_parser.js_class import JSClass
from js_parser.searcher import Searcher


class JSClassAbstractBuilder(metaclass=ABCMeta):
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

    def make_analyser(self, type):
        if type == 'class_name':
            return Searcher("class\s\w{3,}",  "class ")
        if type == 'attribute':
            return Searcher("this.\w+", "this.")
        if type == 'method':
            return Searcher("\n\s{2}\w{2,}\s\(.*\)", "\n  ")
        if type == 'association':
            return Searcher("new\s\w{3,}", "new ")
        else:
            return None
