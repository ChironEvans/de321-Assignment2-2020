# Code by Chiron
from cmd import Cmd
from parser_cli import ParserCLI

class View(Cmd):
    def __init__():
        Cmd.__init__(self)
        self.prompt = ">>> "

    def do_help(self, *args):
    """Shows the help file for the program. No arguments"""
        with open('help.txt', 'r') as help_file:
            for line in help_file.readlines():
                print(line)

    def do_analyse(self, target=''):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""

    def do_analyse_loaded(self, args):
        """Analyses data from a loaded pickle file"""

    def do_renderpng(self, args):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""


    def do_save(self, args):
        """Saves loaded analysis, takes 2 arguments of the name and place to save the file. p for pickle,
        mdb for MongoDB,
        sdb for MySQL DB.
        Name argument optional.
        Example: save mdb filename"""

    def do_load(self, args):
        """Saves loaded analysis, takes 2 arguments of the name and place to load the file from. p for pickle, mdb for MongoDB,
                sdb for MySQL DB"
                Name argument optional.
                Example: load mdb filename"""


if __name__ == '__main__':
    cli = ParserCLI()
    cli.cmdloop()
