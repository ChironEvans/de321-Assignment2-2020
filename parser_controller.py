# Code by Chiron
from os import path
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
                return(self.renderpng())
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
                if path.isfile('output\\classes.dot'):
                    with open("output\\classes.dot", "r") as read_target:
                        save_string = read_target.readlines()
                    if save_string is not None:
                        if self.m_cursor is None:
                            self.m_cursor = MongoCursor()
                        if not self.m_cursor.connection():
                            return("Server connection error timed out")
                        else:
                            if self.m_cursor.add_entry(save_string, name):
                                return(f'Saved to MongoDB as {name}')
                else:
                    return("file to be saved does not exist, please analyse a file first")

            elif target == 'sdb':
                # SQL Code by Liam
                return('Not yet Implemented')
                pass

            elif target == 'p':
                conditions_valid = False
                if self.js_parser.check_self():
                    if self.js_parser.pickle_self(name):
                        return(f'saved successfully to {name}.p file')
                        conditions_valid = True
                    else:
                        # Doesn't use conditions_false var as the conditions were met but there was an issue with
                        # the pickler itself
                        return('Pickling process failed')
                else:
                    conditions_valid = False

                if not conditions_valid:
                    return('No data available to save')
            else:
                return("Error: Incorrect argument given")
        else:
            return("Error: Incorrect or no argument given")

    def load(self, target, name='default'):
        """Saves loaded analysis, takes 2 arguments of the name and place to load the file from. p for pickle, mdb for MongoDB,
                sdb for MySQL DB"
                Name argument optional.
                Example: load mdb filename"""

        if target is not None:
            if target == 'mdb':
                if not self.m_cursor.connection():
                    return("Server connection error timed out")
                else:
                    m_result = self.m_cursor.fetch_entry(name)
                    if m_result:
                        with open("output\\classes.dot", "w+") as dot_target:
                            for line in m_result['data']:
                                dot_target.write(line)
                        return(f'{name} entry successfully loaded')
                    else:
                        return(f'Entry {name} not found.')
            elif target == 'sdb':
                # SQL Code by Liam
                # Do SQL things
                return('Not yet Implemented')
                pass
            elif target == 'p':
                if self.js_parser.load_pickle(name):
                    return(f'Data successfully loaded from {name}.p')
                else:
                    return(f'Data could not be loaded from {name}.p')
            else:
                return("Error: Incorrect argument given")
        else:
            return("Error: No argument given")

    def do_remove(self, target=None, name='default'):
        """Deletes saved analysis, takes 2 arguments of the name and place to load the file from. p for pickle,
                mdb for MongoDB,
                sdb for MySQL DB
                Name argument optional.
                Example: load mdb filename"""

        if target is not None:
            if target == 'mdb':
                if not self.m_cursor.connection():
                    return("Server connection error timed out")
                else:
                    m_result = self.m_cursor.delete_entry(name)
                    if m_result:
                        return(f'{name} entry successfully deleted')
                    else:
                        return(f'Entry {name} not found.')
            elif target == 'sdb':
                # SQL Code by Liam
                # Do SQL things
                return('Not yet Implemented')
                pass
            elif target == 'p':
                if self.js_parser.load_pickle(name):
                    return(f'Successfully deleted {name}.p')
                else:
                    return(f'{name}.p could not be found')
            else:
                return("Error: Incorrect argument given")
        else:
            return("Error: No argument given")