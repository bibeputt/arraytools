====================
Sphinx Documentation
====================

Organization is the key
-----------------------

Make a folder for your documentation.  It is easier if it is in your module folder.

For example::

    "C:/Modules/DoStuffModule"             Your code resides here
    "C:/Modules/DoStuffModule/docs"        documentation folder
    "C:/Modules/DoStuffModule/docs/source" where the `.rst` files go
	"C:/Modules/DoStuffModule/docs/build"  where the results go

This is a good visual example::

	..arraytools
	├── arraytools_docs
		│   │
		│   ├── __init__.py
		│   ├── _basic.py
		│   ├── _io.py
		│   ├.. snip .....
		│	├── tools.py
		│   └── utils.py
		├── build
		│     ├── doctrees
		│     └── html
		│
		├── source ————├──-------├── static (folder to put static items if needed)
		│              ├──    └── _templates (folder to put templates)
		├── make.bat   ├── conf.py
		│              ├── index.rst
		├── Makefile   ├── md_tester.rst
		│              ├── ... add more
		├── README.rst ├── ... rst files as needed
		│              └── < last file in `source` folder
		└── The end of the folder


see `<https://stackoverflow.com/questions/53639615/missing-module-documentation-with-sphinx-make-html>`_.


Using reStructuredText
----------------------

A few words here.


References
----------

`Sphinx Home <https://shimizukawa-sphinx.readthedocs.io/en/1.2.3/index.html>`_.

`Documentation contents <https://shimizukawa-sphinx.readthedocs.io/en/1.2.3/contents.html>`_.
