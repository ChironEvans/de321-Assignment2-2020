import sys
from cmd import Cmd
from jsparser import JSParser
from PIL import Image


class Quitter(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "
        self.js_parser = JSParser()

    def do_onlyanalyse(self, target='input\\'):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""
        print("t:" + target)
        if target != '':
            self.js_parser = JSParser(target)

        result = self.js_parser.run_regex()
        if result:
            result = self.js_parser.write_dotfile()
            if result:
                print('Analysis complete')

        if not result:
            print('Invalid file provided')

    def do_renderpng(self):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""
        if self.js_parser.render_png():
            im = Image.open(r'output\\classes.dot.png')
            im.show()
        else:
            print('DOT file not present')


if __name__ == "__main__":
    quitter = Quitter()
    quitter.cmdloop()


