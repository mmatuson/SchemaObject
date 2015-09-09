from schemaobject.collections import OrderedDict

def ViewSchemaBuilder(database):
    conn = database.parent.connection

    v = OrderedDict()
    sql = """
            SELECT TABLE_NAME, VIEW_DEFINITION
            FROM information_schema.views
            WHERE TABLE_SCHEMA = '%s'
        """
    views = conn.execute(sql % database.name)

    if not views:
        return v

    for view_info in views:
        view_name = view_info['TABLE_NAME']
        
        vv = ViewSchema(name=view_name,parent=database)
        vv.definition = view_info['VIEW_DEFINITION']
   
        v[view_name] = vv

    return v

class ViewSchema(object):
    def __init__(self,name,parent):
        self.parent = parent
        self.name = name
        self.definition = None

    def define(self):
        return self.definition

    def create(self):
        return "CREATE VIEW `%s` AS %s;" % (self.name, self.definition)

    def modify(self):
        return "ALTER VIEW `%s` AS %s;" % (self.name, self.definition)

    def drop(self):
        return "DROP VIEW `%s`;" % self.name

    def __eq__(self,other):
        if not isinstance(other, ViewSchema):
            return False

        return ((self.name == other.name)
                and (self.definition == other.definition))

    def __ne__(self,other):
        return not self.__eq__(other)
