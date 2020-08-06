# Code by Chiron Evans
import os
import subprocess
import dukpy
import js2py

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


if __name__ == '__main__':
    run_nosejs('js_test\\')
    run_dukpy('js_test\\tripMain.ts')
    run_js2py('tripList')


