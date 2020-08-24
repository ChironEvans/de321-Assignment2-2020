from os import getcwd, path, walk, environ, pathsep
import re
from re import sub, findall, search, split
from js_parser.pickler import Pickler
from graphviz import render


class JSParser:

    def __init__(self):
        self.target = f'{os.getcwd()}\\input\\'
        self.js_classnames = []
        self.js_attributes = {}
        self.js_assocs = {}
        self.js_methods = {}
        self.file_depth = 0
        self.max_depth = 4

    def set_target(self, target):
        """Sets the directory or file as the target of analysis, one argument required, the path to target file or
        dir. Returns True if successful, False if an invalid target it given"""
        if target is not None and target != '':
            self.target = target
            return True
        return False

    def run_regex(self, reg_target=None):
        """Begins the process of analysing a file or directory of JS files. No arguments taken. Files must be inside
        parent directory, not nested within folders"""
        if reg_target is None:
            reg_target = self.target

        if os.path.isdir(reg_target):
            self.file_depth += 1
            for root, dirs, files in os.walk(reg_target):
                for name in files:
                    if name.endswith('.js'):
                        print('running file from dir')
                        self.analyse_file(os.path.join(root, name))
        elif os.path.isfile(reg_target):
            if reg_target.endswith('.js'):
                self.analyse_file(reg_target)
            else:
                print("target no js file")
                return False
        else:
            print('target not dir or file')
            return False
        return True

    def analyse_file(self, file):
        """Analyses a single JS file, called by the run_regex command , should not be called directly
        """
        print("running analysis")
        print("File: " + file)
        js_input = ''
        with open(file) as js_file:
            for line in js_file.readlines():
                js_input += line

            # Remove all comment blocks
            js_input = re.sub("\/\*(.|\n)*\*\/", '', js_input)
            js_input = re.sub("#.*", '', js_input)
            js_classname_raw = re.findall("class\s\w{3,}", js_input)

            for match in js_classname_raw:
                classname = re.search("class\s\w{3,}", match)
                s = classname.start()
                e = classname.end()
                classname = classname.string[s:e]
                classname = classname.split(" ")[1]
                if classname not in self.js_classnames:
                    self.js_classnames.append(classname)

            # Add in a large random string so that regex can split by class without removing the keyword
            js_file_for_split = re.sub("class\s", "filjjndfs789er45jkngdrijouerga890e4jndrclass ", js_input)
            js_file_split = re.split("filjjndfs789er45jkngdrijouerga890e4jndr", js_file_for_split)
            bad_sectors = []

            i = 0
            while i < len(js_file_split):
                if len(js_file_split[i]) > 5:
                    if js_file_split[i][0] + js_file_split[i][1] + js_file_split[i][2] + js_file_split[i][3] + \
                            js_file_split[i][4] == "class":

                        classname = re.search("class\s\w{3,}", js_file_split[i])
                        s = classname.start()
                        e = classname.end()
                        classname = classname.string[s:e]
                        classname = classname.split(" ")[1]

                        js_attributes_raw = re.findall("this.\w{1,}", js_file_split[i])
                        js_attributes_cleaned = set([])
                        for attr in js_attributes_raw:
                            js_attributes_cleaned.add(attr.replace('this.', ''))
                        self.js_attributes[classname] = js_attributes_cleaned

                        js_methods_raw = re.findall("\n\s{2}\w{2,}\s\(.*\)", js_file_split[i])
                        js_methods_cleaned = set([])
                        for method in js_methods_raw:
                            js_methods_cleaned.add(method.strip("\n  "))
                        self.js_methods[classname] = js_methods_cleaned

                        associations_raw = re.findall("new\s\w{3,}\(", js_file_split[i])
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
        """Writes stored information to a .dot file and renders it to a .png, no arguments needed"""
        if self.check_self():
            with open(f"{os.getcwd()}\\output\\classes.dot", "w+") as dot_target:
                dot_target.write('digraph "classes_test" {\ncharset="utf-8"\nrankdir=BT\n')
                class_num = 0
                class_index = {}
                for js_class in self.js_classnames:
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

    def render_png(self):
        """Renders a PNG file from the DOT file, called by the write_dotfile command, should not be called directly"""
        # Convert a .dot file to .png
        os.environ["PATH"] += os.pathsep + 'graphviz-2.38-win32/release/bin/'
        if os.path.isfile(f'{os.getcwd()}\\output\\classes.dot'):
            render('dot', 'png', f'{os.getcwd()}\\output\\classes.dot')
            return True
        else:
            return False

    def check_self(self):
        if len(self.js_classnames) > 0:
            return True
        return False

    def pickle_self(self, name='last_pickle'):
        pickler = Pickler(name)
        pickler.preserve(self.__dict__)
        return True

    def load_pickle(self, name='last_pickle'):
        pickler = Pickler(name)
        if self.__dict__.update(pickler.load()) is not False:
            if self.check_self():
                return True
        return False


if __name__ == '__main__':
    js_test = JSParser()
    js_test.run_regex()
    js_test.write_dotfile()
