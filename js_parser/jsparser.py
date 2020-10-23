# Code by Chiron Evans
import os
from abc import ABC
from os import getcwd, path, walk, environ, pathsep, remove
from re import compile

from js_parser.AnalyserFactoryMethod import AnalyserFactoryMethod
from js_parser.splitter import Splitter
from js_parser.jsclass_builder import JSClassBuilder
from js_parser.jsclass_director import JSClassDirector
from js_parser.pickler import Pickler
from graphviz import render


class JSParser(AnalyserFactoryMethod, ABC):
    def __init__(self):
        self.target = f'{getcwd()}\\input\\'
        self.js_classnames = []
        self.js_classes = []

    def set_target(self, target):
        """Sets the directory or file as the target of analysis, one argument required, the path to target file or
        dir. Returns True if successful, False if an invalid target is given"""
        if target is not None and target.strip(' ') != '':
            self.target = target
            return True
        return False

    def run_regex(self, reg_target=None):
        """Begins the process of analysing a file or directory of JS files. No arguments taken. Files must be inside
        parent directory, not nested within folders"""
        if reg_target is None:
            reg_target = self.target
        if path.isdir(reg_target):
            for root, dirs, files in walk(reg_target):
                for name in files:
                    if name.endswith('.js'):
                        self.analyse_file(path.join(root, name))
        elif path.isfile(reg_target):
            if reg_target.endswith('.js'):
                self.analyse_file(reg_target)
            else:
                return False
        else:
            return False
        if len(self.js_classnames) == 0:
            return False
        return True

    def analyse_file(self, file):
        """Analyses a single JS file, called by the run_regex command , should not be called directly
        """
        js_input = ''
        with open(file) as js_file:
            for line in js_file.readlines():
                js_input += line

        js_chunks = self.make_analyser('splitter_class').find_matches(js_input)
        if js_chunks is None:
            return False
        my_director = JSClassDirector()
        for chunk in js_chunks:
            new_builder = JSClassBuilder(chunk)
            my_director.set_builder(new_builder)
            my_director.build_class()
            new_js_class = my_director.builder.js_class
            if new_js_class.name is not None:
                self.js_classes.append(new_js_class)
                self.js_classnames.append(new_js_class.name)
        if len(self.js_classes) == 0:
            return False
        return True

    def write_dotfile(self):
        """Writes stored information from object fields to a .dot file and renders it to a .png, takes no arguments."""
        if self.check_self():
            with open(f"{getcwd()}\\output\\classes.dot", "w") as dot_target:
                dot_target.write('digraph "classes_test" {\ncharset="utf-8"\nrankdir=BT\n')
                class_num = 0
                while class_num < len(self.js_classes):
                    class_name = self.js_classes[class_num].name
                    class_attrs = self.js_classes[class_num].attributes
                    class_methods = self.js_classes[class_num].methods
                    output_string = f'"{class_num}" [label="' + '{' + f'{class_name}|'

                    for attr in class_attrs:
                        output_string += f'{attr}\\l'

                    output_string += '|'

                    for method in class_methods:
                        output_string += f'{method}\\l'

                    output_string += '}", shape="record"];\n'
                    dot_target.write(output_string)
                    class_num += 1

                for js_class in self.js_classes:
                    class_assocs = js_class.associations
                    for assoc in class_assocs:
                        if assoc in self.js_classnames:
                            assoc_index = self.js_classnames.index(assoc)
                            dot_target.write(
                                f'"{self.js_classnames.index(js_class.name)}" -> "{assoc_index}" '
                                f'[arrowhead="empty", arrowtail="none"];\n')

                dot_target.write("}\n")
            if self.render_png():
                return True
            else:
                return False
        return False

    @staticmethod
    def render_png():
        """Renders a PNG file from the DOT file, takes no arguments. Must have graphviz inside of the program directory
        or in the system PATH."""
        # Convert a .dot file to .png
        rootdir = getcwd()
        regex = compile('graphviz.*')

        for root, dirs, files in os.walk(rootdir):
            for adir in dirs:
                if regex.match(adir):
                    environ["PATH"] += pathsep + path.join(adir, 'release/bin/')

        if path.isfile(f'{getcwd()}\\output\\classes.dot'):
            render('dot', 'png', f'{getcwd()}\\output\\classes.dot')
            return True
        else:
            return False

    def check_self(self):
        """Checks if data is present inside the object. Takes no aarguments"""
        if len(self.js_classes) > 0:
            return True
        return False

    def make_analyser(self, analyser_type):
        if analyser_type == 'splitter_class':
            return Splitter("class\s", "class ")

    def pickle_self(self, name='default'):
        """Save object data to pickle file. Takes one optional argument of name"""
        if self.check_self():
            pickler = Pickler(name)
            pickler.preserve(self.__dict__)
            return True
        return False

    def load_pickle(self, name='default'):
        """Load object data from pickle file. Takes one optional argument of name"""
        pickler = Pickler(name)
        if pickler.load() is not False:
            self.__dict__.update(pickler.load())
            if self.check_self():
                return True
        return False

    @staticmethod
    def delete_pickle(name='default'):
        """Deleted a pickled file. Takes one optional argument of name."""
        if path.isfile(f'{name}.p'):
            remove(f'{name}.p')
            return True
        return False

