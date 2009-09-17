#!/usr/bin/python
import unittest
from schemaobject.collections import OrderedDict

class TestOrderedDict(unittest.TestCase):
    
    def setUp(self):
        self.test = OrderedDict()
        self.test['name'] = "John Smith"
        self.test['location'] = "New York"
        
    def test_eq_dict_keys(self):
        self.assertEqual( ['name', 'location'], self.test.keys() )

    def test_neq_dict_keys(self):
        self.assertNotEqual( ['location', 'name'], self.test.keys() )
            
    def test_eq_dict_items(self):
        self.assertEqual( [('name', 'John Smith'), ('location', 'New York')], self.test.items() )
        
    def test_neq_dict_items(self):
        self.assertNotEqual( [('location', 'New York'), ('name', 'John Smith')], self.test.items() )
            
    def test_dict_iterkeys(self):
        for i, v in enumerate(self.test.iterkeys()):
            if i == 0:
                self.assertEqual(v, 'name')
            if i == 1:
                self.assertEqual(v, 'location')
          
    def test_dict_iteritems(self):
        for i, v in enumerate(self.test.iteritems()):
            if i == 0:
                self.assertEqual(v, ('name', 'John Smith'))
            if i == 1:
                self.assertEqual(v, ('location', 'New York')) 
                
                     
if __name__ == "__main__":
    unittest.main()