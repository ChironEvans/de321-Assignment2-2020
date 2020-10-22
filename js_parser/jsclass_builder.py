from abc import ABCMeta, abstractmethod

from js_parser.js_class import JSClass
from js_parser.jsclass_abstract_builder import JSClassAbstractBuilder


class JSClassBuilder(JSClassAbstractBuilder):
    def __init__(self, input_string):
        super().__init__(input_string)

    def add_name(self):
        self.js_class.name = self.make_analyser('class_name').find_matches(self.input_string)[0]

    def add_attributes(self):
        self.js_class.attributes = self.make_analyser('attribute').find_matches(self.input_string)

    def add_methods(self):
        self.js_class.methods = self.make_analyser('method').find_matches(self.input_string)

    def add_associations(self):
        self.js_class.associations = self.make_analyser('association').find_matches(self.input_string)
