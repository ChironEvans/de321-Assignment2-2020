from js_parser.jsclass_abstract_builder import JSClassAbstractBuilder


class JSClassBuilder(JSClassAbstractBuilder):
    def __init__(self, input_string):
        super().__init__(input_string)

    def add_name(self):
        class_name = self.make_analyser('class_name').find_matches(self.input_string)
        if class_name is not None:
            self.js_class.name = class_name[0]
        else:
            self.js_class.name = None

    def add_attributes(self):
        self.js_class.attributes = self.make_analyser('attribute').find_matches(self.input_string)

    def add_methods(self):
        self.js_class.methods = self.make_analyser('method').find_matches(self.input_string)

    def add_associations(self):
        self.js_class.associations = self.make_analyser('association').find_matches(self.input_string)
