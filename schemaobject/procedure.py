import re
from schemaobject.collections import OrderedDict

def ProcedureSchemaBuilder(database):
    conn = database.parent.connection

    p = OrderedDict()

    sql = """
            SELECT name, param_list, body, created, modified, comment
            FROM mysql.proc
            WHERE type = 'PROCEDURE'
            AND db = '%s'
        """

    procedures = conn.execute(sql % database.name)

    if not procedures:
        return p

    for proc_info in procedures:
        proc_name = proc_info['name']

        proc = ProcedureSchema(name=proc_name, parent=database)
        proc.param_list = proc_info['param_list']
        body = re.sub('--.*','',proc_info['body']) # Remove SQL comments
        # Remove newlines to be able to compare strings
        body = body.replace('\n',' ').replace('\r', ' ').replace('\r\n', ' ') 
        proc.body = body
        proc.created = proc_info['created']
        proc.modified = proc_info['modified']
        proc.comment = proc_info['comment']

        p[proc_name] = proc

    return p

class ProcedureSchema(object):
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.param_list = None
        self.body = None
        self.created = None
        self.modified = None
        self.comment = None

    def define(self):
        sql = []
        sql.append("`%s` (%s) %s" % (self.name, self.param_list,self.body))

        if self.comment is not None and len(self.comment) > 0:
            sql.append("COMMENT '%s'" % self.comment)

        return ' '.join(sql)

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
                and (self.param_list == other.param_list)
                and (self.body == other.body)
                and (self.comment == other.comment))

    def __ne__(self, other):
        return not self.__eq__(other)
