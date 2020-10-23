
class JSClassDirector:
    def __init__(self, builder=None):
        self.builder = builder

    def set_builder(self, builder):
        self.builder = builder

    def build_class(self):
        self.builder.add_name()
        self.builder.add_attributes()
        self.builder.add_methods()
        self.builder.add_associations()
