# Code by Chiron
import os
from cmd import Cmd
from PIL import Image
from js_parser.jsparser import JSParser
from mongo_cursor import MongoCursor


class ParserCLI(Cmd):
    def __init__(self, new_parser, new_mongo):
        Cmd.__init__(self, new_parser)
        self.prompt = ">>> "
        self.js_parser = new_parser
        self.m_cursor = new_mongo

    def do_help(self, *args):
        with open('help.txt', 'r') as help_file:
            for line in help_file.readlines():
                print(line)

    def do_analyse(self, target=''):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""
        if target != '':
            self.js_parser.set_target(target)
        result = self.js_parser.run_regex()
        if result:

            result = self.js_parser.write_dotfile()
            print(result)
            if result:
                print('Analysis complete')
                print('Rendering PNG')
                self.do_renderpng()
            else:
                print('Unable to write to dot file')

        if not result:
            print('Invalid file/dir provided')

    def do_analyse_loaded(self, *args):
        if self.js_parser.write_dotfile():
            print('Successfully analysed loaded data')
        else:
            print('No data loaded')

    def do_renderpng(self, *args):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""
        if self.js_parser is None:
            self.js_parser = JSParser()

        if self.js_parser.render_png():
            print('Rendering PNG')
            im = Image.open(r'output\\classes.dot.png')
            im.show()
        else:
            print('DOT file not present')

    def do_save(self, args):
        """Saves loaded analysis, takes 2 arguments of the name and place to save the file. p for pickle,
        mdb for MongoDB,
        sdb for MySQL DB.
        Name argument optional.
        Example: save mdb filename"""
        target = None
        name = 'default'
        args = args.split(' ')
        if len(args) > 0:
            target = args[0]
        if len(args) > 1:
            name = args[1]

        print('running save command')
        if target is not None:
            if target == 'mdb':
                if os.path.isfile('output\\classes.dot'):
                    with open("output\\classes.dot", "r") as read_target:
                        save_string = read_target.readlines()
                    if save_string is not None:
                        if self.m_cursor is None:
                            self.m_cursor = MongoCursor()
                        if not self.m_cursor.connection():
                            print("Server connection error timed out")
                        else:
                            if self.m_cursor.add_entry(name, save_string):
                                print(f'Saved to MongoDB as {name}')
                else:
                    print("file to be saved does not exist, please analyse a file first")

            if target == 'sdb':
                # SQL Code by Liam
                print('Not yet Implemented')
                pass

            if target == 'p':
                conditions_valid = False
                if self.js_parser.check_self():
                    if self.js_parser.pickle_self(name):
                        print(f'saved successfully to {name}.p file')
                        conditions_valid = True
                    else:
                        # Doesn't use conditions_false var as the conditions were met but there was an issue with
                        # the pickler itself
                        print('Pickling process failed')
                else:
                    conditions_valid = False

                if not conditions_valid:
                    print('No data available to save')
        else:
            print("Error: Incorrect or no argument given")

    def do_load(self, args):
        """Saves loaded analysis, takes 2 arguments of the name and place to load the file from. p for pickle,
                mdb for MongoDB,
                sdb for MySQL DB"
                Name argument optional.
                Example: load mdb filename"""
        target = None
        name = 'default'
        args = args.split(' ')
        if len(args) > 0:
            target = args[0]
        if len(args) > 1:
            name = args[1]

        if target is not None:
            if target == 'mdb':
                if not self.m_cursor.connection():
                    print("Server connection error timed out")
                else:
                    m_result = self.m_cursor.fetch_entry(name)
                    if m_result:
                        print(f'{name} entry successfully loaded')
                        with open("output\\classes.dot", "w+") as dot_target:
                            for line in m_result['data']:
                                dot_target.write(line)
                    else:
                        print(f'Entry {name} not found.')

            if target == 'sdb':
                # SQL Code by Liam
                # Do SQL things
                print('Not yet Implemented')
                pass
            if target == 'p':
                if self.js_parser.load_pickle(name):
                    print(f'Data successfully loaded from {name}.p')
                else:
                    print(f'Data could not be loaded from {name}.p')
        else:
            print("Error: No argument given")
