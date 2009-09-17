#!/usr/bin/python

import unittest
import schemaobject
from tests.config import DATABASE_URL

class TestSchema(unittest.TestCase):
  def setUp(self):
    self.db = schemaobject.SchemaObject(DATABASE_URL + 'sakila')
    self.db2 = schemaobject.SchemaObject(DATABASE_URL)

  def test_database_version(self):
    assert self.db.version == "5.1.30"

  def test_port(self):
    assert self.db.port == 3306

  def test_host(self):
    assert self.db.host == "localhost"

  def test_user(self):
    assert self.db.user == "mitch"

  def test_selected_databse(self):
    assert self.db.selected.name == "sakila"

  def test_no_selected_databse(self):
    assert self.db2.selected == None
    
  def test_database_count_with_selected_databse(self):
    assert len(self.db.databases) == 1

  def test_database_count_without_selected_databse(self):
    print len(self.db2.databases)
    assert len(self.db2.databases) == 14
    
if __name__ == "__main__":
    unittest.main()