# Code by Chiron
import os
from cmd import Cmd
from parser_controller import ParserController
from PIL import Image
from mongo_cursor import MongoCursor


class ParserCLI(Cmd):
    def __init__(self, new_controller):
        Cmd.__init__(self, new_controller)
        self.prompt = ">>> "
        self.controller = new_controller

    def do_showhelp(self, *args):
        """Show the helpfile"""
        print(self.controller.help())

    def do_analyse(self, target=''):
        """Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file location"""
        print(self.controller.analyse(target))

    def do_analyse_loaded(self, args):
        """Runs analysis on loaded pickle data, only writes to DOT file, renderpng command must be run afterwards
        to receive image output"""
        print(self.controller.analyse_loaded())

    def do_renderpng(self, args):
        """Renders a PNG from a generated DOT file, if one is present, takes no arguments"""
        print(self.controller.renderpng())

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

        if target is not None:
            print(self.controller.load(target, name))
        else:
            print('No Argument Entered')

    def do_load(self, args):
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
            print(self.controller.load(target, name))
        else:
            print('No Argument Entered')

    def do_remove(self, args):
        """Deletes saved analysis, takes 2 arguments of the name and place to load the file from. p for pickle,
                mdb for MongoDB,
                sdb for MySQL DB
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
            print(self.controller.remove(target, name))
        else:
            print('No Argument Entered')

    @staticmethod
    def do_exit(*args):
        """Exits the program
        return: true"""
        return True


if __name__ == '__main__':
    cli = ParserCLI()
    cli.cmdloop()
