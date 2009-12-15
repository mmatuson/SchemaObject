SchemaObject v0.5.2 documentation 
+++++++++++++++++++++++++++++++++

Introduction and Examples
-------------------------
SchemaObject provides a simple, easy to use Python object interface to a MySQL database schema. You can effortlessly write tools to test, validate, sync, migrate, or manage your schema as well as generate the SQL necessary to make changes to it. 

**Verify all tables are InnoDB**

::

    import schemaobject
    schema  = schemaobject.SchemaObject('mysql://username:password@localhost:3306/mydb')
    tables = schema.databases['mydb'].tables #or schema.selected.tables
    for t in tables:
        assert tables[t].options['engine'].value == 'InnoDB'


**Verify our MySQL instance is at least version 5.1**

::

        import schemaobject
        schema  = schemaobject.SchemaObject('mysql://username:password@localhost:3306/mydb')
        assert schema.version >= '5.1.0'
        
        
**Notes and Limitations**

* SchemaObject instances are read-only. Modifying the object or calling create(), modify(), alter(), or drop() will not change your schema. 
* The MySQL User needs to have privileges to execute SELECT and SHOW statements, as well as access the INFORMATION_SCHEMA. 
* All Databases, Tables, Columns, Indexes, and Foreign Keys are lazily loaded.
* SchemaObject does not load Events, Triggers, or Stored Procedures.

What's New in This Version
--------------------------
See the history of  :doc:`CHANGES </changes>`

.. _installing:

Download and Install
--------------------

**Prerequisites**

* SchemaObject has been tested against Python 2.4, 2.5, and 2.6.
* To use SchemaObject, you need to have `MySQL <http://www.mysql.com/>`_, version 5.0 or higher and `MySQLdb <http://sourceforge.net/projects/mysql-python>`_, version 1.2.1p2 or higher installed. 
* To run the test suite, you need to install a copy of the `Sakila Database <http://dev.mysql.com/doc/sakila/en/sakila.html>`_, version 0.8

**Standard Installation**

Download `SchemaObject-0.5.2 <http://www.matuson.com/code/schemaobject/downloads/SchemaObject-0.5.2.tar.gz>`_
::
    tar xvzf SchemaObject-0.5.2.tar.gz
    cd SchemaObject-0.5.2
    sudo python setup.py install
    
**Installing with easy_install**
::

    sudo easy_install schemaobject

**Installing the latest development version**
::

    git clone git://github.com/mmatuson/SchemaObject.git
    cd schemaobject
    sudo python setup.py install

To upgrade to a new version of SchemaObject, see  :doc:`Upgrading </upgrading>`
    
Documentation
-------------
.. toctree::
    :maxdepth: 1

    api/schema.rst
    api/database.rst
    api/table.rst
    api/column.rst
    api/index.rst
    api/foreignkey.rst
    api/option.rst
  
 
Projects using SchemaObject
---------------------------
`Schema Sync <http://www.schemasync.org>`_ - a MySQL schema versioning and migration utility

      
Status & License
-----------------
SchemaObject is under active development and released under the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_. 

You can obtain a copy of the latest source code from the `Git repository <http://github.com/mmatuson/SchemaObject>`_, or fork it on `Github <http://www.github.com>`_.

You can report bugs via the `SchemaObject Issues page <http://github.com/mmatuson/SchemaObject/issues>`_.

Comments, questions, and feature requests can be sent to code at matuson dot com

