# Code by Chiron
import os
import sys
from cmd import Cmd
from jsparser import JSParser
from PIL import Image
from mongo_handler import MongoCursor


class ParserCLI(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "
        self.js_parser = None
        self.m_cursor = None

    def do_help(self, *args):
        with open('help.txt', 'r') as help_file:
            for line in help_file.readlines():
                print(line)

    def do_analyse(self, target='input\\'):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""

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

    def do_save(self, target=None, name='default'):
        """Saves loaded analysis, takes 2 arguments of the name and place to save the file. p for pickle,
        mdb for MongoDB,
        sdb for MySQL DB.
        Name argument optional.
        Example: save mdb filename"""

        if target is not None:
            if target == 'mdb':
                if os.path.isfile('output\\classes.dot'):
                    save_string = ''
                    with open("output\\classes.dot", "r") as read_target:
                        save_string = read_target

                    if self.m_cursor is None:
                        self.m_cursor = MongoCursor()
                    if not self.m_cursor.connection():
                        print("Server connection error timed out")
                    else:
                        self.m_cursor.add_entry(name, save_string)
                else:
                    print("file to be saved does not exist, please analyse a file first")

            if target == 'sdb':
                # SQL Code by Liam
                # Do SQL things
                pass
            if target == 'p':
                # Pickle it
                pass
        else:
            print("Error: No argument given")

    def do_load(self, target=None, name='default'):
        """Saves loaded analysis, takes 2 arguments of the name and place to load the file from. p for pickle, mdb for MongoDB,
                sdb for MySQL DB"
                Name argument optional.
                Example: load mdb filename"""

        if target is not None:
            if target == 'mdb':
                if self.m_cursor is None:
                    m_cursor = MongoCursor()
                if not self.m_cursor.connection():
                    print("Server connection error timed out")
                else:
                    m_result = self.m_cursor.fetch_entry(name)
                    if m_result:
                        print(f'{name} entry successfully loaded')
                        with open("output\\classes.dot", "w+") as dot_target:
                            dot_target.write(m_result['data'])
                    else:
                        print(f'Entry {name} not found.')

            if target == 'sdb':
                # SQL Code by Liam
                # Do SQL things
                pass
            if target == 'p':
                # Pickle it
                pass
        else:
            print("Error: No argument given")

if __name__ == '__main__':
    cli = ParserCLI()
    cli.cmdloop()