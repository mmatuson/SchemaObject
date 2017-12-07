#!/usr/bin/env python
from setuptools import setup

setup(
    name='SchemaObject',
    packages=['schemaobject'],
    version='0.5.8',
    description="Iterate over a MySQL database schema as a Python object.",
    author="Mitch Matuson, Mustafa Ozgur",
    author_email="code@matuson.com, root@mit.sh",
    url="http://matuson.com/code/schemaobject",
    keywords=["MySQL", "database", "schema"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
    ],
    long_description="""\
        SchemaObject provides a simple, easy to use Python object interface to a MySQL database schema.
        You can effortlessly write tools to test, validate, sync, migrate, or manage your schema as well as generate
        the SQL necessary to make changes to it.
        """,
    install_requires=[
        "PyMySQL >= 0.6.2",
    ],
)
