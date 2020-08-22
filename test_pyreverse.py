# Code by Chiron Evans  
import subprocess
import os
from graphviz import render


def run_pyreverse(name):
    """run pyreverse"""
    print(subprocess.Popen(f"pyreverse -o dot -p {name} {os.getcwd()}", shell=True, stdout=subprocess.PIPE).stdout.read())
    # Convert a .dot file to .png
    os.environ["PATH"] += os.pathsep + 'graphviz-2.38-win32/release/bin/'
    render('dot', 'png', f'{name}_classes.dot')


if __name__ == '__main__':
    run_pyreverse('classes')
