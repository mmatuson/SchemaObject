#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name='SchemaObject',
    
    packages=['schemaobject'],
    
    version='0.5',
    
    description="SchemaObject creates an object representation of a MySQL database schema.",
    
    author="Mitch Matuson",
    
    author_email = "code@matuson.com",
    
    url = "http://matuson.com/code/schemaobject",
    
    keywords = ["MySQL", "database", "schema"],
    
    classifiers = [
      "Intended Audience :: Developers",
      "License :: OSI Approved :: Apache Software License",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Topic :: Database",
      "Topic :: Database :: Front-Ends",
      ],
      
      long_description = """\
      SchemaObject creates an object representation of a MySQL schema including its databases, tables, columns, indexes, and foreign keys. 
      It allows you to process and iterate over a MySQL schema through python object properties and methods.
      """
)