#!/usr/bin/python
import unittest
import schemaobject

class TestColumnSchema(unittest.TestCase):
    def setUp(self):
        self.db = schemaobject.SchemaObject(self.database_url + 'sakila')
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

    def test_column_null(self):
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `last_name`",
                        self.db.tables['customer'].columns['email'].define(after='last_name'))

    def test_column_not_null(self):
        self.db.tables['customer'].columns['email'].null = True
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `last_name`",
                        self.db.tables['customer'].columns['email'].define(after='last_name'))

    def tes_column_default(self):
        self.assertEqual("`active` TINYINT(1) NOT NULL DEFAULT 1 CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `address_id`",
                        self.db.tables['customer'].columns['active'].define(after='address_id'))

    def test_column_no_default(self):
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `last_name`",
                        self.db.tables['customer'].columns['email'].define(after='last_name'))

    def test_column_extra(self):
        self.assertEqual("`customer_id` SMALLINT(5) UNSIGNED NOT NULL auto_increment FIRST",
                    self.db.tables['customer'].columns['customer_id'].define())

    def test_column_no_extra(self):
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `last_name`",
                         self.db.tables['customer'].columns['email'].define(after='last_name'))

    def test_column_comment(self):
        self.db.tables['customer'].columns['email'].comment = "email address field"
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT 'email address field' AFTER `last_name`",
                         self.db.tables['customer'].columns['email'].define(after='last_name', with_comment=True))

    def test_column_no_comment(self):
        self.db.tables['customer'].columns['email'].comment = "email address field"
        self.assertEqual("`email` VARCHAR(50) NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `last_name`",
                         self.db.tables['customer'].columns['email'].define(after='last_name', with_comment=False))

    def test_column_no_collate(self):
        self.assertEqual("`customer_id` SMALLINT(5) UNSIGNED NOT NULL auto_increment FIRST",
                         self.db.tables['customer'].columns['customer_id'].define())

    def test_column_after(self):
        self.assertEqual("`last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `first_name`",
                         self.db.tables['customer'].columns['last_name'].define(after='first_name'))

    def test_column_first(self):
        self.assertEqual("`last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci FIRST",
                         self.db.tables['customer'].columns['last_name'].define(after=None))

    def test_create_column(self):
        self.assertEqual("ADD COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `first_name`",
                         self.db.tables['customer'].columns['last_name'].create(after='first_name'))

    def test_create_column_with_comment(self):
        self.db.tables['customer'].columns['last_name'].comment = "hello"
        self.assertEqual("ADD COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT 'hello' AFTER `first_name`",
                      self.db.tables['customer'].columns['last_name'].create(after='first_name', with_comment=True))
        self.db.tables['customer'].columns['last_name'] = ''

    def test_modify_column(self):
        self.assertEqual("MODIFY COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci AFTER `first_name`",
                         self.db.tables['customer'].columns['last_name'].modify(after='first_name'))

    def test_modify_column_with_comment(self):
        self.db.tables['customer'].columns['last_name'].comment = "hello"
        self.assertEqual("MODIFY COLUMN `last_name` VARCHAR(45) NOT NULL CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT 'hello' AFTER `first_name`",
                      self.db.tables['customer'].columns['last_name'].modify(after='first_name', with_comment=True))
        self.db.tables['customer'].columns['last_name'] = ''

    def test_column_drop(self):
        self.assertEqual("DROP COLUMN `last_name`",
                         self.db.tables['customer'].columns['last_name'].drop())

if __name__ == "__main__":
    from test_all import get_database_url
    TestColumnSchema.database_url = get_database_url()
    unittest.main()