#!/usr/bin/python
import unittest
import schemaobject
from tests.config import DATABASE_URL

class TestColumnSchema(unittest.TestCase):
    def setUp(self):
        self.db = schemaobject.SchemaObject(DATABASE_URL + 'sakila')
        self.db = self.db.selected
        
    def test_column_count(self):
        self.assertEqual(9, len(self.db.tables['customer'].columns))

    def test_columns(self):
        self.assertEqual(self.db.tables['customer'].columns.keys(), 
                        ['customer_id', 'store_id', 'first_name', 'last_name',
                         'email', 'address_id', 'active', 'create_date', 'last_update'])
              
    def test_column_field(self):
        self.assertEqual("store_id", self.db.tables['customer'].columns['store_id'].field)

    def test_column_type(self):
        self.assertEqual("VARCHAR(50)", self.db.tables['customer'].columns['email'].type)

    def test_column_charset(self):
        self.assertEqual("utf8", self.db.tables['customer'].columns['last_name'].charset)

    def test_column_collation(self):
        self.assertEqual("utf8_general_ci", self.db.tables['customer'].columns['last_name'].collation)
        
    def test_column_null(self):
        self.assertTrue(self.db.tables['customer'].columns['email'].null)

    def test_column_not_null(self):
        self.assertFalse(self.db.tables['customer'].columns['active'].null)

    def test_column_key(self):
        self.assertEqual('PRI', self.db.tables['customer'].columns['customer_id'].key)

    def test_column_default(self):
        self.assertEqual("CURRENT_TIMESTAMP", self.db.tables['customer'].columns['last_update'].default)

    def test_column_extra(self):
        self.assertEqual('auto_increment', self.db.tables['customer'].columns['customer_id'].extra)

    def test_column_comment(self):
        self.assertEqual('', self.db.tables['customer'].columns['store_id'].comment)
    
    def test_columns_eq(self):
        self.assertEqual(self.db.tables['customer'].columns['store_id'], 
                         self.db.tables['customer'].columns['store_id'])

    def test_columns_neq(self):
        self.assertNotEqual(self.db.tables['customer'].columns['store_id'],
                            self.db.tables['customer'].columns['last_name'])

    def create_column_null(self):
        self.assertEqual("ADD COLUMN `email` VARCHAR(50) NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `last_name`", 
                        self.db.tables['customer'].columns['email'].create(after='last_name'))

    def create_column_not_null(self):
        self.assertEqual("ADD COLUMN `active` TINYINT(1) NOT NULL DEFAULT 1 CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `address_id`", 
                        self.db.tables['customer'].columns['active'].create(after='address_id'))

    def create_column_default(self):
        self.assertEqual("ADD COLUMN `active` TINYINT(1) NOT NULL DEFAULT 1 CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `address_id`", 
                        self.db.tables['customer'].columns['active'].create(after='address_id'))

    def create_column_no_default(self):
        self.assertEqual("ADD COLUMN `email` VARCHAR(50) NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `last_name`", 
                        self.db.tables['customer'].columns['email'].create(after='last_name'))

    def create_column_extra(self):
        self.assertEqual("ADD COLUMN `customer_id` SMALLINT(5) unsigned NOT NULL auto_increment FIRST", 
                    self.db.tables['customer'].columns['customer_id'].create())

    def create_column_no_extra(self):
        self.assertEqual("ADD COLUMN `email` VARCHAR(50) NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `last_name`", 
                         self.db.tables['customer'].columns['email'].create(after='last_name'))
        
    def create_column_no_collate(self):
        self.assertEqual("ADD COLUMN `customer_id` SMALLINT(5) unsigned NOT NULL auto_increment FIRST", 
                         self.db.tables['customer'].columns['customer_id'].create())
                    
    def create_column_after(self):
        self.assertEqual("ADD COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `first_name`", 
                         self.db.tables['customer'].columns['last_name'].create(after='first_name') )

    def create_column_first(self):
        self.assertEqual("ADD COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci FIRST", 
                         self.db.tables['customer'].columns['last_name'].create(after=None) )

    def modify_column(self):
        self.assertEqual("MODIFY COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET=utf8 COLLATE=utf8_general_ci AFTER `first_name`", 
                         self.db.tables['customer'].columns['last_name'].create(after='first_name') )

    def test_column_drop(self):
        self.assertEqual("DROP COLUMN `last_name`", 
                         self.db.tables['customer'].columns['last_name'].drop())
             
if __name__ == "__main__":
    unittest.main()