# Code by Chiron
import sys
from cmd import Cmd
from jsparser import JSParser
from PIL import Image


class ParserCLI(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "
        self.js_parser = JSParser()

    def do_analyse(self, target='input\\'):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""
        print("t:" + target)
        if target != '':
            self.js_parser = JSParser(target)

        result = self.js_parser.run_regex()
        if result:
            result = self.js_parser.write_dotfile()
            if result:
                print('Analysis complete')
                print('Rendering PNG')
                self.do_renderpng()

        if not result:
            print('Invalid file provided')

    def do_renderpng(self, *args):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""
        if self.js_parser.render_png():
            im = Image.open(r'output\\classes.dot.png')
            im.show()
        else:
            print('DOT file not present')

    def do_save(self, target=None):
        if target is not None:
            if target == 'mdb':
                # Do mongo things
                pass
            if target == 'sdb':
                # Do SQL things
                pass
            if target == 'p':
                # Pickle it
                pass
        else:
            print("Error: No argument given")

    def do_load(selfself, target=None):
        if target is not None:
            if target == 'mdb':
                # Do mongo things
                pass
            if target == 'sdb':
                # Do SQL things
                pass
            if target == 'p':
                # Pickle it
                pass
        else:
            print("Error: No argument given")


if __name__ == "__main__":
    cli = ParserCLI()
    cli.cmdloop()


