# Code by Chiron Evans
import unittest
from js_parser.jsparser import JSParser
from os import getcwd, path, remove


class TestJSParser(unittest.TestCase):
    def setUp(self):
        self.parser = JSParser()

    def test__init(self):
        self.assertTrue(self.parser.target != '')
        self.assertEqual(self.parser.js_classnames, [])
        self.assertEqual(self.parser.js_attributes, {})
        self.assertEqual(self.parser.js_assocs, {})
        self.assertEqual(self.parser.js_methods, {})

    def test_self_check_invalid(self):
        self.assertFalse(self.parser.check_self())

    def test_set_target_valid(self):
        new_target = f'{getcwd()}\\test_jsparser\\'
        expected_return = True
        self.parser.set_target(new_target)
        self.assertEqual(new_target, self.parser.target)
        self.assertTrue(expected_return)

    def test_set_target_invalid(self):
        new_target = ''
        expected_return = False
        actual_return = self.parser.set_target(new_target)
        self.assertNotEqual(new_target, self.parser.target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_no_target(self):
        expected_return = True
        actual_return = self.parser.run_regex()
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_bad_target(self):
        target = f'{getcwd()}\\input\\notAFile.js'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_target_file(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_bad_file(self):
        target = f'{getcwd()}\\input\\badList.js'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_empty_file(self):
        target = f'{getcwd()}\\input\\empty.js'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_target_dir(self):
        target = f'{getcwd()}\\input\\'
        expected_return = True
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_run_regex_empty_dir(self):
        target = f'{getcwd()}\\input\\nested_empty\\'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_analyse_classnames(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_classnames = ['Trip']
        actual_return = self.parser.run_regex(target)
        actual_classnames = self.parser.js_classnames
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_classnames, actual_classnames)
        self.assertTrue(type(self.parser.js_classnames) is list)

    """def test_analyse_classnames_new(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_classnames = 'Trip'
        actual_return = self.parser.run_regex(target)
        actual_classnames = self.parser.js_classes[0].name
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_classnames, actual_classnames)"""

    def test_analyse_attributes(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_attrs = {'Trip': {'id', 'distance', 'time', 'duration'}}
        actual_return = self.parser.run_regex(target)
        actual_attrs = self.parser.js_attributes
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_attrs, actual_attrs)
        self.assertTrue(type(self.parser.js_attributes) is dict)
        self.assertTrue(type(self.parser.js_attributes['Trip']) is set)

    """"def test_analyse_attributes_new(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_attrs = ['id', 'distance', 'time', 'duration']
        actual_return = self.parser.run_regex(target)
        actual_attrs = self.parser.js_classes[0].attributes
        self.assertCountEqual(expected_attrs, actual_attrs)
        self.assertEqual(expected_return, actual_return)"""

    def test_analyse_methods(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_methods = {'Trip': {'constructor (tripID, tripTime, tripDistance, tripDuration)'}}
        actual_return = self.parser.run_regex(target)
        actual_methods = self.parser.js_methods
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_methods, actual_methods)
        self.assertTrue(type(self.parser.js_methods) is dict)
        self.assertTrue(type(self.parser.js_methods['Trip']) is set)

    """def test_analyse_methods_new(self):
        target = f'{getcwd()}\\input\\nested\\trip.js'
        expected_return = True
        expected_methods = ['constructor (tripID, tripTime, tripDistance, tripDuration)']
        actual_return = self.parser.run_regex(target)
        actual_methods = self.parser.js_classes[0].methods
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_methods, actual_methods)"""

    def test_analyse_association(self):
        target = f'{getcwd()}\\input\\tripList.js'
        expected_return = True
        expected_assocs = {'TripList': {'Trip', 'Date'}}
        actual_return = self.parser.run_regex(target)
        actual_assocs = self.parser.js_assocs
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_assocs, actual_assocs)
        self.assertTrue(type(self.parser.js_assocs) is dict)
        self.assertTrue(type(self.parser.js_assocs['TripList']) is set)

    """def test_analyse_association_new(self):
        target = f'{getcwd()}\\input\\tripList.js'
        expected_return = True
        expected_assocs = ['Date', 'Trip']
        actual_return = self.parser.run_regex(target)
        actual_assocs = self.parser.js_classes[0].associations
        self.assertCountEqual(expected_assocs, actual_assocs)
        self.assertEqual(expected_return, actual_return)"""

    def test_self_check_valid(self):
        target = f'{getcwd()}\\input\\tripList.js'
        expected_return = True
        self.parser.run_regex(target)
        actual_return = self.parser.check_self()
        self.assertEqual(expected_return, actual_return)

    def test_write_dotfile_blank(self):
        expected_return = False
        actual_return = self.parser.write_dotfile()
        self.assertEqual(expected_return, actual_return)

    def test_write_dotfile_valid(self):
        expected_return = True
        target = f'{getcwd()}\\input\\tripList.js'
        self.parser.run_regex(target)
        actual_return = self.parser.write_dotfile()
        self.assertEqual(expected_return, actual_return)

    def test_render_png_valid(self):
        expected_return = True
        target = f'{getcwd()}\\input\\tripList.js'
        self.parser.run_regex(target)
        self.parser.write_dotfile()
        actual_return = self.parser.render_png()
        file_exists = path.isfile(f'{getcwd()}\\output\\classes.dot.png')
        self.assertEqual(expected_return, actual_return)
        self.assertTrue(file_exists)

    def test_pickle_self_invalid(self):
        expected_return = False
        actual_return = self.parser.pickle_self()
        self.assertEqual(expected_return, actual_return)

    def test_pickle_self_valid(self):
        expected_return = True
        target = f'{getcwd()}\\input\\tripList.js'
        self.parser.run_regex(target)
        actual_return = self.parser.pickle_self()
        file_exists = path.isfile(f'{getcwd()}\\default.p')
        self.assertEqual(expected_return, actual_return)
        self.assertTrue(file_exists)

    def test_pickle_self_valid_name(self):
        expected_return = True
        target = f'{getcwd()}\\input\\tripList.js'
        self.parser.run_regex(target)
        actual_return = self.parser.pickle_self('test_jsparser')
        file_exists = path.isfile(f'{getcwd()}\\test_jsparser.p')
        self.assertEqual(expected_return, actual_return)
        self.assertTrue(file_exists)

    def test_delete_pickle_valid(self):
        if not path.isfile(f'{getcwd()}\\default.p'):
            target = f'{getcwd()}\\input\\tripList.js'
            self.parser.run_regex(target)
            self.parser.pickle_self()
        expected_return = True
        actual_return = self.parser.delete_pickle()

        file_exists = path.isfile(f'{getcwd()}\\default.p')
        self.assertEqual(expected_return, actual_return)
        self.assertFalse(file_exists)

    def test_delete_pickle_invalid(self):
        if path.isfile(f'{getcwd()}\\default.p'):
            remove(f'{getcwd()}\\default.p')
            self.assertFalse(path.isfile(f'{getcwd()}\\default.p'))
        expected_return = False
        actual_return = self.parser.delete_pickle()
        self.assertEqual(expected_return, actual_return)

    def test_delete_pickle_valid_name(self):
        if not path.isfile(f'{getcwd()}\\test_jsparser.p'):
            target = f'{getcwd()}\\input\\tripList.js'
            self.parser.run_regex(target)
            self.parser.pickle_self('test_jsparser')
        expected_return = True
        actual_return = self.parser.delete_pickle('test_jsparser')

        file_exists = path.isfile(f'{getcwd()}\\test_jsparser.p')
        self.assertEqual(expected_return, actual_return)
        self.assertFalse(file_exists)

    def test_load_pickle_valid(self):
        if not path.isfile(f'{getcwd()}\\default.p'):
            target = f'{getcwd()}\\input\\tripList.js'
            self.parser.run_regex(target)
            self.parser.pickle_self('default')
            self.assertTrue(path.isfile('default.p'))

        expected_return = True
        actual_return = self.parser.load_pickle()
        self.assertEqual(expected_return, actual_return)
        self.assertTrue(self.parser.check_self())

    def test_load_pickle_invalid(self):
        if path.isfile(f'{getcwd()}\\default.p'):
            remove(f'{getcwd()}\\default.p')
            self.assertFalse(path.isfile(f'{getcwd()}\\default.p'))

        expected_return = False
        actual_return = self.parser.load_pickle()
        self.assertEqual(expected_return, actual_return)
        self.assertFalse(self.parser.check_self())

    def test_load_pickle_valid_name(self):
        if not path.isfile(f'{getcwd()}\\test_jsparser.p'):
            target = f'{getcwd()}\\input\\tripList.js'
            self.parser.run_regex(target)
            self.parser.pickle_self('test_jsparser')
            self.assertTrue(path.isfile('test.p'))

        expected_return = True
        actual_return = self.parser.load_pickle('test_jsparser')
        self.assertEqual(expected_return, actual_return)
        self.assertTrue(self.parser.check_self())

    def test_non_js_file_root(self):
        target = f'{getcwd()}\\input\\notAJSFile.txt'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_non_js_file_nested(self):
        target = f'{getcwd()}\\input\\nested\\notjs\\notAJSFile.txt'
        expected_return = False
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_js_dupe_class(self):
        target = f'{getcwd()}\\input\\dupeclass.js'
        expected_return = True
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_js_dual_class(self):
        target = f'{getcwd()}\\input\\dualclass.js'
        expected_return = True
        actual_return = self.parser.run_regex(target)
        self.assertEqual(expected_return, actual_return)

    def test_analyse_func_empty_file(self):
        target = f'{getcwd()}\\input\\empty.js'
        expected_return = False
        actual_return = self.parser.analyse_file(target)
        self.assertEqual(expected_return, actual_return)


if __name__ == '__main__':
    unittest.main()
