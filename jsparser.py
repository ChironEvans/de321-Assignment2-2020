import os
import re
import subprocess
from re import findall, sub, split
from os import path, listdir

from graphviz import render


class JSParser:

    def __init__(self, target='input\\'):
        self.target = target
        self.js_classnames = []
        self.js_attributes = {}
        self.js_assocs = {}
        self.js_methods = {}

    def run_regex(self):
        """Begins the process of analysing a file or directory of JS files. No arguments taken"""
        print("self.target: " + self.target)
        if os.path.isdir(self.target):
            for file in os.listdir(self.target):
                if file.endswith('.js'):
                    print("running file from dir")
                    self.analyse_file(self.target + '\\' + file)

        elif os.path.isfile(self.target):
            if self.target.endswith('.js'):
                self.analyse_file(self.target)
            else:
                print("target no js file")
                return False
        else:
            print(self.target)
            print('else triggered')
            return False
        return True

    def analyse_file(self, file):
        """Analyses a single JS file, called by the run_regex command on initializaiton, should not be called directly
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
                    bad_sectors.append(i)
                i += 1
            for bad_sector in bad_sectors:
                js_file_split.remove(js_file_split[bad_sector])

        return True

    def write_dotfile(self):
        """Writes stored information to a .dot file and renders it to a .png, no arguments needed"""
        with open("output\\classes.dot", "w+") as dot_target:
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


    def render_png(self):
        """Renders a PNG file from the DOT file, called by the write_dotfile command, should not be called directly"""
        # Convert a .dot file to .png
        os.environ["PATH"] += os.pathsep + 'graphviz-2.38-win32/release/bin/'
        if os.path.isfile('output\\classes.dot'):
            render('dot', 'png', 'output\\classes.dot')
            return True
        else:
            return False


if __name__ == '__main__':
    js_test = JSParser()
    js_test.run_regex()
    js_test.write_dotfile()
