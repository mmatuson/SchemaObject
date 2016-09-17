#!/usr/bin/python
import re
import unittest
import schemaobject


class TestForeignKeySchema(unittest.TestCase):

    def setUp(self):
        self.database_url = "mysql://root:root@localhost:3306/"
        self.schema = schemaobject.SchemaObject(self.database_url + 'sakila', charset='utf8')
        self.fk = self.schema.selected.tables['rental'].foreign_keys

    def test_fk_exists(self):
        self.assertTrue("fk_rental_customer" in list(self.fk.keys()))

    def test_fk_not_exists(self):
        self.assertFalse("fk_foobar" in list(self.fk.keys()))

    def test_fk_name(self):
        self.assertEqual("fk_rental_customer", self.fk['fk_rental_customer'].name)

    def test_fk_symbol(self):
        self.assertEqual("fk_rental_customer", self.fk['fk_rental_customer'].symbol)

    def test_fk_table_name(self):
        self.assertEqual("rental", self.fk['fk_rental_customer'].table_name)

    def test_fk_table_schema(self):
        self.assertEqual("sakila", self.fk['fk_rental_customer'].table_schema)

    def test_fk_columns(self):
        self.assertEqual(['customer_id'], self.fk['fk_rental_customer'].columns)

    def test_fk_referenced_table_name(self):
        self.assertEqual("customer", self.fk['fk_rental_customer'].referenced_table_name)

    def test_fk_referenced_table_schema(self):
        self.assertEqual("sakila", self.fk['fk_rental_customer'].referenced_table_schema)

    def test_fk_referenced_columns(self):
        self.assertEqual(['customer_id'], self.fk['fk_rental_customer'].referenced_columns)

    def test_fk_match_option(self):
        self.assertEqual(None, self.fk['fk_rental_customer'].match_option)

    def test_fk_update_rule(self):
        self.assertEqual("CASCADE", self.fk['fk_rental_customer'].update_rule)

    def test_fk_delete_rule(self):
        self.assertEqual("RESTRICT", self.fk['fk_rental_customer'].delete_rule)

    def test_format_referenced_col_with_length(self):
        self.assertEqual('`fk_rental_customer`(11)', schemaobject.foreignkey.ForeignKeySchema._format_referenced_col('fk_rental_customer', 11))

    def test_format_referenced_col_without_length(self):
        self.assertEqual('`fk_rental_customer`', schemaobject.foreignkey.ForeignKeySchema._format_referenced_col('fk_rental_customer', 0))
        self.assertEqual('`fk_rental_customer`', schemaobject.foreignkey.ForeignKeySchema._format_referenced_col('fk_rental_customer', None))

    def test_fk_drop(self):
        self.assertEqual(self.fk['fk_rental_customer'].drop(), "DROP FOREIGN KEY `fk_rental_customer`")

    def test_fk_create(self):
        self.assertEqual(self.fk['fk_rental_customer'].create(),
                        "ADD CONSTRAINT `fk_rental_customer` FOREIGN KEY `fk_rental_customer` (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE")

    def test_fk_eq(self):
        self.assertEqual(self.fk['fk_rental_customer'], self.fk['fk_rental_customer'])

    def test_fk_neq(self):
        self.assertNotEqual(self.fk['fk_rental_customer'], self.fk['fk_rental_inventory'])

    # def test_fk_reference_opts_update_and_delete(self):
    #     table_def = """CREATE TABLE `child` (
    #         `id` int(11) DEFAULT NULL,
    #         `parent_id` int(11) DEFAULT NULL,
    #         KEY `par_ind` (`parent_id`),
    #         CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`)
    #         REFERENCES `parent` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
    #         CONSTRAINT `child_ibfk_2` FOREIGN KEY (`parent_id`)
    #         REFERENCES `parent` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT )
    #         ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_danish_ci COMMENT='hello world';"""
    #
    #     matches = re.search(REGEX_FK_REFERENCE_OPTIONS % 'child_ibfk_1', table_def,  re.X)
    #     self.assertTrue(matches)
    #     self.assertTrue(matches.group('on_delete'))
    #     self.assertTrue(matches.group('on_update'))
    #     self.assertEqual(matches.group('on_delete'), 'SET NULL')
    #     self.assertEqual(matches.group('on_update'), 'CASCADE')
    #
    #     matches = re.search(REGEX_FK_REFERENCE_OPTIONS % 'child_ibfk_1', table_def,  re.X)
    #     self.assertTrue(matches)
    #     self.assertTrue(matches.group('on_delete'))
    #     self.assertTrue(matches.group('on_update'))
    #     self.assertEqual(matches.group('on_delete'), 'RESTRICT')
    #     self.assertEqual(matches.group('on_update'), 'RESTRICT')
    #
    # def test_fk_reference_opts_delete(self):
    #     table_def = """CREATE TABLE `child` (
    #         `id` int(11) DEFAULT NULL,
    #         `parent_id` int(11) DEFAULT NULL,
    #         KEY `par_ind` (`parent_id`),
    #         CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parent` (`id`) ON DELETE SET NULL )
    #         ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_danish_ci COMMENT='hello world';"""
    #
    #     matches = re.search(REGEX_FK_REFERENCE_OPTIONS % 'child_ibfk_1', table_def,  re.X)
    #     self.assertTrue(matches)
    #     self.assertTrue(matches.group('on_delete'))
    #     self.assertTrue(not matches.group('on_update'))
    #     self.assertEqual(matches.group('on_delete'), 'SET NULL')
    #
    # def test_fk_reference_opts_update(self):
    #     table_def = """CREATE TABLE `child` (
    #         `id` int(11) DEFAULT NULL,
    #         `parent_id` int(11) DEFAULT NULL,
    #         KEY `par_ind` (`parent_id`),
    #         CONSTRAINT `child_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parent` (`id`) ON UPDATE CASCADE )
    #         ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_danish_ci COMMENT='hello world';"""
    #
    #     matches = re.search(REGEX_FK_REFERENCE_OPTIONS % 'child_ibfk_1', table_def,  re.X)
    #     self.assertTrue(matches)
    #     self.assertTrue(not matches.group('on_delete'))
    #     self.assertTrue(matches.group('on_update'))
    #     self.assertEqual(matches.group('on_update'), 'CASCADE')