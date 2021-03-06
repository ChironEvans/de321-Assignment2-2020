# Code by Chiron Evans
import io
import unittest.mock
import parser_cli
<<<<<<< HEAD
=======
import parser_controller
>>>>>>> view_implement


class TestCLI(unittest.TestCase):
    def setUp(self):
<<<<<<< HEAD
        self.cli = parser_cli.ParserCLI(None, None)
=======
        self.cli = parser_cli.ParserCLI(parser_controller.ParserController(None, None))
>>>>>>> view_implement

    def test_prompt(self):
        self.assertEqual(">>> ", self.cli.prompt)

<<<<<<< HEAD
    def test_js_parser(self):
        self.assertEqual(None, self.cli.js_parser)

    def test_m_cursor(self):
        self.assertEqual(None, self.cli.m_cursor)

=======
>>>>>>> view_implement
    def test_showhelp_exists(self):
        self.assertTrue("do_showhelp" in dir(self.cli))

    def test_do_analyse_exists(self):
        self.assertTrue("do_analyse" in dir(self.cli))

    def test_do_analyse_loaded_exists(self):
        self.assertTrue("do_analyse_loaded" in dir(self.cli))

    def test_do_renderpng_exists(self):
        self.assertTrue("do_renderpng" in dir(self.cli))

    def test_do_save_exists(self):
        self.assertTrue("do_save" in dir(self.cli))

    def test_do_load_exists(self):
        self.assertTrue("do_load" in dir(self.cli))

    def test_do_remove_exists(self):
        self.assertTrue("do_remove" in dir(self.cli))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_help(self, arg, expected_output, mock_stdout):
        self.cli.do_showhelp(arg)
        self.assertEqual(expected_output.strip('\n'), mock_stdout.getvalue().strip('\n'))

    def test_showhelp_no_args(self):
        expected_out = ''
        with open('help.txt', 'r') as help_file:
            for line in help_file.readlines():
                expected_out += line
        self.assert_stdout_help(None, expected_out)

    def test_help_do_showhelp(self):
        help_str = 'Show the helpfile'
        self.assertEqual(help_str, self.cli.do_showhelp.__doc__)

    def test_help_do_analyse(self):
        help_str = 'Analyses a JS file or directory of JS files, takes 1 optional argument or a directory or file ' \
                   'location'
        self.assertEqual(help_str, self.cli.do_analyse.__doc__)

    def test_help_do_analyse_loaded(self):
        help_str = 'Runs analysis on loaded pickle data, only writes to DOT file, renderpng command must be run ' \
                   'afterwards\n        to receive image output'
        self.assertEqual(help_str, self.cli.do_analyse_loaded.__doc__)

    def test_help_do_renderpng(self):
        help_str = 'Renders a PNG from a DOT file generated by the program if one is present, takes no arguments'
        self.assertEqual(help_str, self.cli.do_renderpng.__doc__)

    def test_help_do_save(self):
        help_str = 'Saves loaded analysis, takes 2 arguments of the name and place to save the file. p for pickle,\n' \
                   '        mdb for MongoDB,\n' \
                   '        sdb for MySQL DB.\n' \
                   '        Name argument optional.\n' \
                   '        Example: save mdb filename'
        self.assertEqual(help_str, self.cli.do_save.__doc__)

    def test_help_do_load(self):
        help_str = 'Loads saved analysis, takes 2 arguments of the name and place to load the file from. p for ' \
                   'pickle,\n' \
                   '                mdb for MongoDB,\n' \
                   '                sdb for MySQL DB\n' \
                   '                Name argument optional.\n' \
                   '                Example: load mdb filename'
        self.assertEqual(help_str, self.cli.do_load.__doc__)

    def test_help_do_remove(self):
        help_str = 'Deletes saved analysis, takes 2 arguments of the name and place to load the file from. p for ' \
                   'pickle,\n' \
                   '                mdb for MongoDB,\n' \
                   '                sdb for MySQL DB\n' \
                   '                Name argument optional.\n' \
                   '                Example: load mdb filename'
        self.assertEqual(help_str, self.cli.do_remove.__doc__)

    def test_help_exit(self):
        help_str = 'Exits the program\n' \
                   '        return: true'
        self.assertEqual(help_str, self.cli.do_exit.__doc__)

    def test_exit(self):
        self.assertEqual(True, self.cli.do_exit())


if __name__ == '__main__':
    unittest.main()
