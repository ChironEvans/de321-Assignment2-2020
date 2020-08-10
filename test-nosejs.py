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

        js_file__for_split = re.sub("class\s", "filjjndfs789er45jkngdrijouerga890e4jndrclass ", js_input)
        js_file_split = re.split("filjjndfs789er45jkngdrijouerga890e4jndr", js_file__for_split)
        js_attributes = {}
        for i in js_file_split:
            if i[0] + i[1] + i[2] + i[3] + i[4] != "class":
                js_file_split.remove(i)
            else:
                classname = re.search("class\s\w{3,}", i)
                s = classname.start()
                e = classname.end()
                classname = classname.string[s:e]
                classname = classname.split(" ")[1]
                js_attributes[classname] = re.findall("this.\w{1,}", i)

        print(js_file_split)
        print(js_classnames)
        print(js_attributes)


if __name__ == '__main__':
    # run_nosejs('js_test\\')
    # run_dukpy('js_test\\tripMain.ts')
    # run_js2py('tripList')
    run_regex('tripList')


