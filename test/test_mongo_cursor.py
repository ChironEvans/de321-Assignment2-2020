import unittest
import mongo_cursor
import asyncio


class TestMongoCursor(unittest.TestCase):
    def setUp(self):
        self.mcursor = mongo_cursor.MongoCursor()

    def test_add_entry_invalid(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.add_entry(None))
        self.assertFalse(actual_return)

    def test_add_entry_valid(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.add_entry('test1'))
        self.assertTrue(actual_return)

    def test_add_entry_blank_name(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.add_entry(' '))
        self.assertTrue(actual_return)

    def test_add_entry_valid_name(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.add_entry('test2', 'unittest2'))
        self.assertTrue(actual_return)

    def test_fetch_entry_invalid(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.fetch_entry(None))
        self.assertFalse(actual_return)

    def test_fetch_entry_valid(self):
        loop2 = asyncio.get_event_loop()
        loop2.run_until_complete(self.mcursor.add_entry('test'))
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.fetch_entry())
        self.assertTrue(actual_return)

    def test_fetch_entry_valid_name(self):
        loop2 = asyncio.get_event_loop()
        loop2.run_until_complete(self.mcursor.add_entry('test2', 'unittest2'))
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.fetch_entry('unittest2'))
        self.assertTrue(actual_return)

    def test_delete_entry_invalid(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.delete_entry(None))
        self.assertFalse(actual_return)

    def test_delete_entry_valid(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.delete_entry())
        self.assertTrue(actual_return)

    def test_delete_entry_valid_name(self):
        loop = asyncio.get_event_loop()
        actual_return = loop.run_until_complete(self.mcursor.delete_entry('unittest2'))
        self.assertTrue(actual_return)


if __name__ == '__main__':
    unittest.main()
