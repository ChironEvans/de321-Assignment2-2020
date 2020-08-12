# Code by Chiron Evans
import os
import subprocess
import dukpy
import js2py
import re


def run_nosejs(path):
    # command args that disable the unittest portion of the conversion are broken...bleh
    os.environ["PATH"] += os.pathsep + 'jsl-0.3.0'
    # print(subprocess.Popen(f"nosetests --with-javascript --no-javascript-tests {path}", shell=True,
    #                      stdout=subprocess.PIPE).stdout.read())


def run_dukpy(file):
    # Only works on typescript...bleh
    js_input = ''
    with open(file) as js_file:
        for line in js_file.readlines():
            js_input += line
    print(dukpy.typescript_compile(js_input))


def run_js2py(file):
    # Translates Es6 to es5 then python...bleh
    # js2py.translate_file(f'js_test\\{file}.js', f'js_test\\{file}.py')
    js_input = ''
    with open(f'js_test\\{file}.js') as js_file:
        for line in js_file.readlines():
            js_input += line
    print(js2py.eval_js6(js_input))


def run_regex(file):
    js_input = ''
    with open(f'js_test\\{file}.js') as js_file:
        for line in js_file.readlines():
            js_input += line
        js_classname_raw = re.findall("class\s\w{3,}", js_input)
        js_classnames = []
        for match in js_classname_raw:
            classname = re.search("class\s\w{3,}", match)
            s = classname.start()
            e = classname.end()
            classname = classname.string[s:e]
            classname = classname.split(" ")[1]
            js_classnames.append(classname)

        js_file_for_split = re.sub("class\s", "filjjndfs789er45jkngdrijouerga890e4jndrclass ", js_input)
        js_file_split = re.split("filjjndfs789er45jkngdrijouerga890e4jndr", js_file_for_split)
        js_attributes = {}
        js_methods = {}
        js_assocs = {}
        bad_sectors = []
        i = 0
        while i < len(js_file_split):
            if js_file_split[i][0] + js_file_split[i][1] + js_file_split[i][2] + js_file_split[i][3] +\
                    js_file_split[i][4] == "class":
                classname = re.search("class\s\w{3,}", js_file_split[i])
                s = classname.start()
                e = classname.end()
                classname = classname.string[s:e]
                classname = classname.split(" ")[1]

                js_attributes_raw  = re.findall("this.\w{1,}", js_file_split[i])
                js_attributes_cleaned = set([])
                for attr in js_attributes_raw:
                    js_attributes_cleaned.add(attr.replace('this.', ''))
                js_attributes[classname] = js_attributes_cleaned

                js_methods_raw = re.findall("\n\s{2}\w{2,}\s\(.*\)", js_file_split[i])

                js_methods_cleaned = set([])
                for method in js_methods_raw:
                    js_methods_cleaned.add(method.strip("\n  "))
                js_methods[classname] = js_methods_cleaned

                associations_raw = re.findall("new\s\w{3,}\(", js_file_split[i])
                associations_cleaned = set([])
                for assoc in associations_raw:
                    associations_cleaned.add(assoc.reaplace("new ", '').replace("(", ''))
                js_assocs[classname] = associations_cleaned
            else:
                bad_sectors.append(i)
            i += 1
        for bad_sector in bad_sectors:
            js_file_split.remove(js_file_split[bad_sector])

        print(js_assocs)
        print(js_methods)
        print(js_classnames)
        print(js_attributes)
        write_dotfile(js_classnames, js_attributes, js_assocs, js_methods)


def write_dotfile(classnames, attributes, assocs, methods):
    with open("output\\classes.dot", "w+") as dot_target:
        dot_target.write('digraph "classes_test" {\ncharset="utf-8"\nrankdir=BT\n')
        class_num = 0
        class_index = {}
        for js_class in classnames:
            class_name = classnames[class_num]
            print(class_name)
            class_attrs = attributes[class_name]
            class_methods = methods[class_name]
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
            class_assocs = assocs[primary]
            for assoc in class_assocs:
                if assoc in class_index:
                    assoc_index = class_index[assoc]
                    dot_target.write(f'"{class_index[primary]}" -> "{assoc_index}" [arrowhead="empty", arrowtail="none"];\n')

        dot_target.write("}\n")





if __name__ == '__main__':
    # run_nosejs('js_test\\')
    # run_dukpy('js_test\\tripMain.ts')
    # run_js2py('tripList')
    run_regex('tripList')
