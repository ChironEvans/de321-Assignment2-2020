# Code by Chiron
import os
from js_parser.jsparser import JSParser
from PIL import Image
from mongo_cursor import MongoCursor


class ParserController():
    def __init__(self, new_parser, new_mongo):
        self.js_parser = new_parser
        self.m_cursor = new_mongo

    def help(self):
        return_string = ''
        with open('help.txt', 'r') as help_file:
            for line in help_file.readlines():
                return_string +=(line)
        return return_string

    def analyse(self, target=''):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""
        if target != '':
            self.js_parser.set_target(target)
        result = self.js_parser.run_regex()
        if result:
            result = self.js_parser.write_dotfile()
            if result:
                return('Analysis complete')
            else:
                return('Unable to write to dot file')
        return('Invalid file/dir provided')

    def analyse_loaded(self, args):
        if self.js_parser.write_dotfile():
            return('Successfully analysed loaded data')
        else:
            return('No data loaded')

    def renderpng(self, args):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""
        if self.js_parser is None:
            self.js_parser = JSParser()

        if self.js_parser.render_png():
            im = Image.open(r'output\\classes.dot.png')
            im.show()
            return('PNG successfully rendered')
        else:
            return('DOT file not present')

    def save(self, target, name='default'):
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
                        save_string = read_target.readlines()

                    if self.m_cursor is None:
                        self.m_cursor = MongoCursor()
                    if not self.m_cursor.connection():
                        return("Server connection error timed out")
                    else:
                        if self.m_cursor.add_entry(name, save_string):
                            return(f'Saved to MongoDB as {name}')
                else:
                    return("file to be saved does not exist, please analyse a file first")

            if target == 'sdb':
                # SQL Code by Liam
                pass

            if target == 'p':
                conditions_valid = False
                if self.js_parser.check_self():
                    if self.js_parser.pickle_self():
                        return(f'saved successfully to {name}.p file')
                    else:
                        # Doesn't use conditions_false var as the conditions were met but there was an issue with
                        # the pickler itself
                        return('Pickling process failed')
                else:
                    conditions_valid = False

                if not conditions_valid:
                    return('No data available to save')
        return("Error: Incorrect or no argument given")

    def load(self, target, name='default'):
        """Saves loaded analysis, takes 2 arguments of the name and place to load the file from. p for pickle, mdb for MongoDB,
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
                pass
            if target == 'p':
                # Pickle it
                pass
        else:
            print("Error: No argument given")


if __name__ == '__main__':
    cli = ParserCLI()
    cli.cmdloop()