.. SchemaObject documentation master file, created by
   sphinx-qschemaobjectuickstart on Wed Sep 16 09:45:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SchemaObject v0.5 documentation 
+++++++++++++++++++++++++++++++

Introduction
============
SchemaObject creates an object representation of a MySQL schema including its databases, tables, columns, indexes, and foreign keys. It allows you to process and iterate over a MySQL schema through python object properties and methods.

You can generate the SQL syntax for creating, altering and dropping any part of the schema. As of v0.5, a separate process is needed to push any generated changes to your database instance/schema. 

Status & License
================
SchemaObject is under active development and released under the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_. You can obtain a copy of the latest source code from the Git repository, or fork it on Github.

Installation
=============

Dependancies and Requirements
-----------------------------
* Python 2.5
* MySQLdb

Installing with easy_install
--------------------------------
Simply run ``sudo easy_install schemaobject``

Installing from source
----------------------
[todo]


Documentation
=============
.. toctree::
    :maxdepth: 1

    api/schema.rst
    api/database.rst
    api/table.rst
    api/column.rst
    api/index.rst
    api/foreignkey.rst
    api/option.rst
    

    
Examples
==============
Verify all tables in our database are InnoDB::
    
    import schemaobject
    schema  = schemaobject.SchemaObject('mysql://username:password@localhost:3306/mydb')
    tables = schema.databases['mydb'].tables #or schema.selected.tables
    for t in tables:
        assert tables[t].options['engine'].value == 'InnoDB'
        
Verify our MySQL instance is version 5.x+::

    import schemaobject
    schema  = schemaobject.SchemaObject('mysql://username:password@localhost:3306/mydb')
    assert int(schema.version[:1]) >= 5 #test against the major # of the version string
    
    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`