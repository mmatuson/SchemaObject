#!/usr/bin/python
import unittest
from schemaobject.collections import OrderedDict

class TestOrderedDict(unittest.TestCase):

    def setUp(self):
        self.test = OrderedDict()
        self.test['name'] = "John Smith"
        self.test['location'] = "New York"

    def test_eq_dict_keys(self):
        self.assertEqual( ['name', 'location'], list(self.test.keys()) )

    def test_neq_dict_keys(self):
        self.assertNotEqual( ['location', 'name'], list(self.test.keys()) )

    def test_eq_dict_items(self):
        self.assertEqual( [('name', 'John Smith'), ('location', 'New York')], list(self.test.items()) )

    def test_neq_dict_items(self):
        self.assertNotEqual( [('location', 'New York'), ('name', 'John Smith')], list(self.test.items()) )

    def test_dict_iterkeys(self):
        for i, v in enumerate(self.test.keys()):
            if i == 0:
                self.assertEqual(v, 'name')
            if i == 1:
                self.assertEqual(v, 'location')

    def test_dict_iteritems(self):
        for i, v in enumerate(self.test.items()):
            if i == 0:
                self.assertEqual(v, ('name', 'John Smith'))
            if i == 1:
                self.assertEqual(v, ('location', 'New York'))

    def test_index(self):
        self.assertEqual(1, self.test.index("location"))
        self.assertRaises(ValueError, self.test.index, ("unknown_key",))

    def test_insert(self):
        self.assertFalse("age" in self.test)
        self.test.insert(1, ("age", 100))
        self.assertTrue(1, self.test.index("age"))
        self.assertTrue(2, self.test.index("location"))

    def test__delitem__(self):
        self.assertTrue("location" in self.test)
        del self.test['location']
        self.assertFalse("location" in self.test)