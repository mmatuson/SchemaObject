from schemaobject.collections import OrderedDict


def foreign_key_schema_builder(table):
    """
    Returns a dictionary loaded with all of the foreign keys available in the table.
    ``table`` must be an instance of TableSchema.

    .. note::
      This function is automatically called for you and set to
      ``schema.databases[name].tables[name].foreign_keys`` when you create an instance of SchemaObject
    """

    conn = table.parent.parent.connection
    fkeys = OrderedDict()

    def _get_reference_rules(information_schema, table_name, constraint_name):
        """
        Returns tuple of strings (update_rule, delete_rule)
        (None,None) if constraint not found

        """
        #  select UPDATE_RULE, DELETE_RULE from information_schema.REFERENTIAL_CONSTRAINTS where CONSTRAINT_SCHEMA = 'sakila' and TABLE_NAME = 'payment' and CONSTRAINT_NAME = 'fk_payment_customer';
        sql = """
            SELECT UPDATE_RULE,
                   DELETE_RULE
            FROM information_schema.REFERENTIAL_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = '%s' and TABLE_NAME = '%s' and CONSTRAINT_NAME = '%s'
            """
        result = conn.execute(sql % (information_schema, table_name, constraint_name))
        if result:
            return result[0]['UPDATE_RULE'], result[0]['DELETE_RULE']
        else:
            return None, None

    sql = """
            SELECT K.CONSTRAINT_NAME,
                   K.TABLE_SCHEMA, K.TABLE_NAME, K.COLUMN_NAME,
                   K.REFERENCED_TABLE_SCHEMA, K.REFERENCED_TABLE_NAME, K.REFERENCED_COLUMN_NAME,
                   K.POSITION_IN_UNIQUE_CONSTRAINT
            FROM information_schema.KEY_COLUMN_USAGE K, information_schema.TABLE_CONSTRAINTS T
            WHERE K.CONSTRAINT_NAME = T.CONSTRAINT_NAME
            AND T.CONSTRAINT_TYPE = 'FOREIGN KEY'
            AND K.CONSTRAINT_SCHEMA='%s'
            AND K.TABLE_NAME='%s'
            AND K.REFERENCED_TABLE_NAME is not null
            """
    constraints = conn.execute(sql % (table.parent.name, table.name))

    if not constraints:
        return fkeys

    for fk in constraints:
        n = fk['CONSTRAINT_NAME']

        if n not in fkeys:
            fk_item = ForeignKeySchema(name=n, parent=table)
            fk_item.symbol = n
            fk_item.table_schema = fk['TABLE_SCHEMA']
            fk_item.table_name = fk['TABLE_NAME']
            fk_item.referenced_table_schema = fk['REFERENCED_TABLE_SCHEMA']
            fk_item.referenced_table_name = fk['REFERENCED_TABLE_NAME']
            fk_item.update_rule, fk_item.delete_rule = _get_reference_rules(fk_item.table_schema,
                                                                            fk_item.table_name, fk_item.symbol)
            fkeys[n] = fk_item

        # POSITION_IN_UNIQUE_CONSTRAINT may be None
        pos = fk['POSITION_IN_UNIQUE_CONSTRAINT'] or 0

        # columns for this fk
        if fk['COLUMN_NAME'] not in fkeys[n].columns:
            fkeys[n].columns.insert(pos, fk['COLUMN_NAME'])

        # referenced columns for this fk
        if fk['REFERENCED_COLUMN_NAME'] not in fkeys[n].referenced_columns:
            fkeys[n].referenced_columns.insert(pos, fk['REFERENCED_COLUMN_NAME'])

    return fkeys


class ForeignKeySchema(object):
    """
    Object representation of a single foreign key.
    Supports equality and inequality comparison of ForeignKeySchema.

    ``name`` is the column name.
    ``parent`` is an instance of TableSchema

    .. note::
      ForeignKeySchema objects are automatically created for you by foreign_key_schema_builder
      and loaded under ``schema.databases[name].tables[name].foreign_keys``

    Example

      '>>> schema.databases['sakila'].tables['rental'].foreign_keys.keys()
      ['fk_rental_customer', 'fk_rental_inventory', 'fk_rental_staff']


    Foreign Key Attributes
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].name
      'fk_rental_inventory'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].symbol
      'fk_rental_inventory'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].table_schema
      'sakila'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].table_name
      'rental'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].columns
      ['inventory_id']
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].referenced_table_name
      'inventory'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].referenced_table_schema
      'sakila'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].referenced_columns
      ['inventory_id']
      #match_option will always be None in MySQL 5.x, 6.x
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].match_option
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].update_rule
      'CASCADE'
      '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].delete_rule
      'RESTRICT'
    """

    def __init__(self, name, parent):
        self.parent = parent

        # name of the fk constraint
        self.name = name
        self.symbol = name

        # primary table info
        self.table_schema = None
        self.table_name = None
        self.columns = []

        # referenced table info
        self.referenced_table_schema = None
        self.referenced_table_name = None
        self.referenced_columns = []

        # constraint options
        self.match_option = None  # will always be none in mysql 5.0-6.0
        self.update_rule = None
        self.delete_rule = None

    @classmethod
    def _format_referenced_col(cls, field, length):
        """
        Generate the SQL to format referenced columns in a foreign key
        """
        if length:
            return "`%s`(%d)" % (field, length)
        else:
            return "`%s`" % field

    def create(self):
        """
        Generate the SQL to create (ADD) this foreign key

          '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].create()
          'ADD CONSTRAINT `fk_rental_inventory`
          FOREIGN KEY `fk_rental_inventory` (`inventory_id`)
          REFERENCES `inventory` (`inventory_id`)
          ON DELETE RESTRICT ON UPDATE CASCADE'

        .. note:
          match_option is ignored when creating a foreign key.
        """
        sql = ["ADD CONSTRAINT `%s`" % self.symbol,
               "FOREIGN KEY `%s` (%s)" % (self.symbol, ",".join([("`%s`" % c) for c in self.columns]))]

        if self.referenced_table_schema != self.table_schema:
            sql.append("REFERENCES `%s`.`%s`" % (self.referenced_table_schema, self.referenced_table_name))
        else:
            sql.append("REFERENCES `%s`" % self.referenced_table_name)

        sql.append("(%s)" % ",".join([("`%s`" % c) for c in self.referenced_columns]))

        if self.delete_rule:
            sql.append("ON DELETE %s" % self.delete_rule)

        if self.update_rule:
            sql.append("ON UPDATE %s" % self.update_rule)

        return ' '.join(sql)

    def drop(self):
        """
        Generate the SQL to drop this foreign key

          '>>> schema.databases['sakila'].tables['rental'].foreign_keys['fk_rental_inventory'].drop()
          'DROP FOREIGN KEY `fk_rental_inventory`'
        """
        return "DROP FOREIGN KEY `%s`" % self.symbol

    def __eq__(self, other):
        if not isinstance(other, ForeignKeySchema):
            return False

        # table_schema and referenced_table_schema are ignored
        return ((self.table_name == other.table_name)
                and (self.referenced_table_name == other.referenced_table_name)
                and (self.update_rule == other.update_rule)
                and (self.delete_rule == other.delete_rule)
                and (self.columns == other.columns)
                and (self.referenced_columns == other.referenced_columns))

    def __ne__(self, other):
        return not self.__eq__(other)
