=====================
Upgrading SchemaObject
=====================

Upgrading with easy_install
--------------------------
::

    sudo easy_install --upgrade schemaobject
    

Upgrading the Standard Installation
-----------------------------------

If you installed SchemaObject using setup.py install, you can upgrade by deleting the SchemaObject directory from your Python site-packages (or virtualenv) and :ref:`re-installing <installing>` the new version. 
   
**Where are my site-packages stored?**

The location of the site-packages directory depends on the operating system, and the location in which Python was installed. To find out your system’s site-packages location, execute the following:
::

    python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
    
Note that this should be run from a shell prompt, not a Python interactive prompt. 
Thanks to `the Django install page <http://docs.djangoproject.com/en/dev/topics/install/#remove-any-old-versions-of-django>`_ for these helpful instructions.
    
