import re
from schemaobject.collections import OrderedDict

def ProcedureSchemaBuilder(database):
    conn = database.parent.connection

    p = OrderedDict()

    sql = """
            SELECT ROUTINE_NAME
            FROM information_schema.routines
            WHERE ROUTINE_TYPE='PROCEDURE'
            AND ROUTINE_SCHEMA='%s'
        """

    procedures = conn.execute(sql % database.name)

    if not procedures:
        return p

    for procedure in procedures:
        pname = procedure['ROUTINE_NAME']
        sql = "SHOW CREATE PROCEDURE %s"
        proc_desc = conn.execute(sql % pname)
        if not proc_desc or not proc_desc[0]['Create Procedure']: continue
        proc_desc = proc_desc[0]

        pp = ProcedureSchema(name=pname, parent=database)
        s = re.search('\(',proc_desc['Create Procedure'])
        if not s: continue

        definition = re.sub('--.*',
                                '',
                                proc_desc['Create Procedure'][s.start():])
		pp.definition = definition.replace('\n','').replace('\r\n','').replace('\r','')

        p[pname] = pp

    return p

class ProcedureSchema(object):
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.definition = None

    def define(self):
        sql = []
        return "`%s` %s" % (self.name, self.definition)

    def create(self):
        return "DELIMITER ;; CREATE PROCEDURE %s;; DELIMITER ;" % self.define()

    def modify(self, *args, **kwargs):
        pass # Not needed for now, one cannot alter body

    def drop(self):
        return "DROP PROCEDURE `%s`;" % self.name

    def __eq__(self, other):
        if not isinstance(other, ProcedureSchema):
            return False

        return ((self.name == other.name)
                and (self.definition == other.definition))

    def __ne__(self, other):
        return not self.__eq__(other)
