======================
Contents of arraytools
======================

.. toctree::
   :maxdepth: 2
   :caption: arraytools:


The imports and basic layout of the package are listed in the ``__init__`` file.
The remainder of the imports are presented in subsequent sections.

------------------------------------------------------------------------------

.. arraytools:

arraytools ``__init__``
-----------------------

Initialization of arraytools doesn't import any of the functionality for
``arcpy`` by default so that extra requirement doesn't clog namespace.

.. automodule:: arraytools.__init__
   :members:

------------------------------------------------------------------------------

.. _basic:

_basic module
-------------

Fundamental array methods and properties.

.. automodule:: arraytools._basic
   :members:

------------------------------------------------------------------------------

.. _io:

_io module
----------

Input and output for arrays to and from disk.

.. automodule:: arraytools._io
   :members:

------------------------------------------------------------------------------

.. create:

create module
-------------

Create arrays representing geometric objects.

.. automodule:: arraytools.create
   :members:

------------------------------------------------------------------------------

.. frmts:

format arrays
-------------

Format arrays in a variety of ways.

.. automodule:: arraytools.frmts
   :members:

------------------------------------------------------------------------------

.. geom:

geometry functions
------------------

Functions dealing with geometry.

.. automodule:: arraytools.geom
   :members:

------------------------------------------------------------------------------

.. geom_common:

Common geometry functions
-------------------------

Shared functions for working with geometry.

.. automodule:: arraytools.geom_common
   :members:

------------------------------------------------------------------------------

.. geom_properties:

Geometry properties
-------------------

Properties of geometry objects.

.. automodule:: arraytools.geom_properties
   :members:

------------------------------------------------------------------------------

.. grid:

arrays as grids
---------------

Arrays as grids, largely as replacements for the Spatial Analyst.

.. automodule:: arraytools.grid
   :members:

------------------------------------------------------------------------------

.. ndset:

set operations
--------------

Set operations on arrays.

.. automodule:: arraytools.ndset
   :members:

------------------------------------------------------------------------------

.. py_tools:

python tools
------------

General python tools.

.. automodule:: arraytools.py_tools
   :members:

------------------------------------------------------------------------------
   
.. saws:

Switch arrange weave shape
--------------------------

A multipurpose set of tools for reorganizing arrays.

.. automodule:: arraytools.saws
   :members:

------------------------------------------------------------------------------

.. stackstats

Statistical tools for stacked arrays
------------------------------------

Statistics for N-D arrays.

.. automodule:: arraytools.stackstats
   :members:

------------------------------------------------------------------------------

.. tbl

Table operations for arrays
---------------------------

Arrays as tables.

.. automodule:: arraytools.tbl
   :members:

------------------------------------------------------------------------------

.. tblstats

Statistical tools for tabular arrays
------------------------------------

Statistics for N-D arrays.

.. automodule:: arraytools.tblstats
   :members:

------------------------------------------------------------------------------

.. tools

main array tools
----------------

A large collection of tools for working with arrays.

.. automodule:: arraytools.tools
   :members:

------------------------------------------------------------------------------

.. utils:

utility functions
-----------------

General utility functions and helpers.

.. automodule:: arraytools.utils
   :members:
