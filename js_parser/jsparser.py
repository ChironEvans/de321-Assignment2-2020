# Code by Chiron Evans
import os
from os import getcwd, path, walk, environ, pathsep, remove
from re import findall, sub, split, search, compile
from js_parser.pickler import Pickler
from graphviz import render


class JSParser:
    def __init__(self):
        self.target = f'{getcwd()}\\input\\'
        self.js_classnames = []
        self.js_attributes = {}
        self.js_assocs = {}
        self.js_methods = {}

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

            # Remove all comment blocks
            js_input = sub("/\*(.|\n)*\*/", '', js_input)
            js_input = sub("#.*", '', js_input)
            js_classname_raw = findall("class\s\w{3,}", js_input)

            for match in js_classname_raw:
                classname = search("class\s\w{3,}", match)
                s = classname.start()
                e = classname.end()
                classname = classname.string[s:e]
                classname = classname.split(" ")[1]
                if classname not in self.js_classnames:
                    self.js_classnames.append(classname)

            # Add in a large random string so that regex can split by class without removing the keyword
            js_file_for_split = sub("class\s", "filjjndfs789er45jkngdrijouerga890e4jndrclass ", js_input)
            js_file_split = split("filjjndfs789er45jkngdrijouerga890e4jndr", js_file_for_split)
            bad_sectors = []
            # Exit function if no valid classes found
            if len(self.js_classnames) == 0:
                return False
            i = 0
            while i < len(js_file_split):
                if len(js_file_split[i]) > 5:
                    if js_file_split[i][0] + js_file_split[i][1] + js_file_split[i][2] + js_file_split[i][3] + \
                            js_file_split[i][4] == "class":

                        classname = search("class\s\w{3,}", js_file_split[i])
                        s = classname.start()
                        e = classname.end()
                        classname = classname.string[s:e]
                        classname = classname.split(" ")[1]

                        js_attributes_raw = findall("this.\w+", js_file_split[i])
                        js_attributes_cleaned = set([])
                        for attr in js_attributes_raw:
                            js_attributes_cleaned.add(attr.replace('this.', ''))
                        self.js_attributes[classname] = js_attributes_cleaned

                        js_methods_raw = findall("\n\s{2}\w{2,}\s\(.*\)", js_file_split[i])
                        js_methods_cleaned = set([])
                        for method in js_methods_raw:
                            js_methods_cleaned.add(method.strip("\n  "))
                        self.js_methods[classname] = js_methods_cleaned

                        associations_raw = findall("new\s\w{3,}\(", js_file_split[i])
                        associations_cleaned = set([])
                        for assoc in associations_raw:
                            associations_cleaned.add(assoc.replace("new ", '').replace("(", ''))
                        self.js_assocs[classname] = associations_cleaned

                    else:
                        # Add sections of code that are not classes to list to be removed
                        bad_sectors.append(i)
                i += 1

            for bad_sector in bad_sectors:
                js_file_split.remove(js_file_split[bad_sector])
        return True

    def write_dotfile(self):
        """Writes stored information from object fields to a .dot file and renders it to a .png, takes no arguments."""
        if self.check_self():
            with open(f"{getcwd()}\\output\\classes.dot", "w") as dot_target:
                dot_target.write('digraph "classes_test" {\ncharset="utf-8"\nrankdir=BT\n')
                class_num = 0
                class_index = {}
                while class_num < len(self.js_classnames):
                    class_name = self.js_classnames[class_num]
                    class_attrs = self.js_attributes[class_name]
                    class_methods = self.js_methods[class_name]
                    class_index[class_name] = class_num
                    output_string = f'"{class_num}" [label="' + '{' + f'{class_name}|'

                    for attr in class_attrs:
                        output_string += f'{attr}\\l'

                    output_string += '|'

                    for method in class_methods:
                        output_string += f'{method}\\l'

                    output_string += '}", shape="record"];\n'
                    dot_target.write(output_string)
                    class_num += 1

                for primary in class_index:
                    class_assocs = self.js_assocs[primary]
                    for assoc in class_assocs:
                        if assoc in class_index:
                            assoc_index = class_index[assoc]
                            dot_target.write(
                                f'"{class_index[primary]}" -> "{assoc_index}" [arrowhead="empty", arrowtail="none"];\n')

                dot_target.write("}\n")
            if self.render_png():
                return True
            else:
                return False
        return False

    @staticmethod
    def render_png():
        """Renders a PNG file from the DOT file, takes no arguments. Must have graphviz inside of the program directory or in
        the system PATH."""
        # Convert a .dot file to .png
        # TODO Un-hardcode this
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
        if len(self.js_classnames) > 0:
            return True
        return False

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
