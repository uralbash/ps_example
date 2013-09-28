*********************
API
*********************

Models
======


.. autoclass:: example.models.TestHSTORE
   :inherited-members:

.. note::
    Works only with PostgreSQL database.
    
.. autoclass:: example.models.TestTEXT
   :inherited-members:    
.. autoclass:: example.models.TestBOOL
   :inherited-members:
.. autoclass:: example.models.TestDND
   :inherited-members:
.. autoclass:: example.models.TestUNION
   :inherited-members:
       
Initializedb
============

.. autofunction:: example.scripts.initializedb.add_extension

.. note::
    Works only with PostgreSQL database.
    
.. autofunction:: example.scripts.initializedb.add_fixture
