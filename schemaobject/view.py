import re
from schemaobject.collections import OrderedDict


def view_schema_builder(database):
    conn = database.parent.connection

    v = OrderedDict()

    sql = """
        SELECT TABLE_NAME 
        FROM information_schema.views
        WHERE TABLE_SCHEMA = '%s'
        ORDER BY TABLE_NAME
        """

    views = conn.execute(sql % database.name)

    if not views:
        return v

    for view in views:
        vname = view['TABLE_NAME']
        sql = "SHOW CREATE VIEW %s"
        view_desc = conn.execute(sql % vname)
        if not view_desc:
            continue

        view_desc = view_desc[0]

        vv = ViewSchema(name=vname, parent=database)
        s = re.search('\(?select', view_desc['Create View'], re.IGNORECASE)
        if not s:
            continue

        vv.definition = view_desc['Create View'][s.start():]
        v[vname] = vv

    return v


class ViewSchema(object):
    def __init__(self, name, parent):
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

    def __eq__(self, other):
        if not isinstance(other, ViewSchema):
            return False

        return ((self.name == other.name)
                and (self.definition == other.definition))

    def __ne__(self, other):
        return not self.__eq__(other)
