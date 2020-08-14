"""
This is a cmd demo
"""

from cmd import Cmd


class TestQuitter(Cmd):
    """
    single command processor example
    """
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "
        self.my_name = "unknown"

    def do_name(self, the_name):
        if the_name:
            self.my_name = the_name
        print(self.my_name)

    def do_greet(self, the_name):
        """
        Syntax: greet [the_name]
        Greet the named person
        :param the_name: a string representing a person's name
        :return: None
        """
        if the_name:
            print("Hello " + the_name)
        else:
            print("Hello " + self.my_name)

    def do_quit(self, line):
        print("Quitting ......")
        return True

    def help_quit(self):
        print("\n".join(['Quit from my CMD', ':return: True']))

    do_q = do_quit


if __name__ == "__main__":
    quitter = TestQuitter()
    quitter.cmdloop()