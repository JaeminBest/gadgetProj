Inspector Gadget Flask API
==========================
basic API of crowdsourcing web page of inspector gadget






Requirement
-----------
- anaconda
- python 3.x environment
- requried pip packages :

.. code-block:: text
  Flask              1.0.2     
  Flask-DebugToolbar 0.10.1    
  Flask-Login        0.4.1     
  Flask-Migrate      2.4.0     
  Flask-Script       2.0.6     
  Flask-SQLAlchemy   2.3.2     
  Flask-WTF          0.14.2    
  numpy              1.16.1    
  pip                19.0.1    
  PyMySQL            0.9.3      
  SQLAlchemy         1.2.17    
  Werkzeug           0.14.1    
  WTForms            2.2.1  
  Flask-Cors         3.0.7  (newly added on Feb 26)





Start
-----
1. construct server via mysql
2. locate correct username, password and database name in __init__.py
3. activate anaconda virtual environment in python 3 and install pip packages as shown above
4. execute ``python db.py db init``, ``python db.py reset``, ``python db.py update``, ``python db.py db migrate``, ``python db.py db upgrade``
5. change port number, host ip in run.py
6. execute ``python run.py`` (Quick Start)





Implementation in detail
------------------------
- /run.py 

basic setting of flask app execution. set (1)host address, (2)port number, (3)debug mode.

- /db.py

- /app/__init__.py

- /app/models.py

- /app/views.py

- /app/templates

- /app/static

- /app/templates

- /migrations






Developer Guide
---------------
- localhost:xxxx/
- localhost:xxxx/admin
- localhost:xxxx/admin/show_all_user
- localhost:xxxx/admin/show_one_user
- localhost:xxxx/admin/test_register
- localhost:xxxx/admin/test_unregister
- localhost:xxxx/admin/show_one_image
- localhost:xxxx/admin/display_one_image
