# coding: utf-8
"""
Modified: 2017-09-29

arrtools
=======

Provides tools to facilitate working with numpy and geometry and attributes
largely derived from ArcMap and ArcGIS Pro.

Documentation notes
-------------------
It is assumed throughout that numpy has been imported as
   >>> import numpy as np

Available modules and subpackages
---------------------
a_io.py  (7)
  io tools for numpy arrays and operating system access
  __all_aio__
    'arr_json', 'get_dir', 'load_npy', 'read_txt', 'save_npy', 'save_txt',
    'sub_folders']

apt.py  (15)
  tools for arcpy tools
  __all_apt__
    '_arr_common', '_shapes_fc', 'arr_pnts', 'arr_polygon', 'arr_polyline',
    'array_fc', 'array_struct', 'change_fld', 'fc_array', 'pnts_arr',
    'polygons_arr', 'polylines_arr', 'tbl_arr', 'to_fc', 'tweet'

fc.py  (11)
  tools for working with featureclasses
  __all_fc__
    '_describe', '_get_shapes', '_ndarray', '_props', '_two_arrays', '_xy',
    '_xyID', '_xy_idx', 'change_fld', 'fc_info', 'fld_info']

frmts.py  (11)
  Format options to facilitate viewing of numpy arrays in a variety of ways.
  __all_frmt__
    'col_hdr', 'deline', 'frmt_', 'frmt_ma', 'frmt_rec', 'frmt_struct',
    'in_by', 'make_row_format', 'redent', '_demo', '_ma_demo']

tools.py  (19)
  Main tool set containing the following functions...
  __all_art__:
    'arr2xyz', 'block_arr', 'change', 'doc_func', 'find', 'fc_info',
    'get_func', 'get_modu', 'group_pnts', 'group_vals', '_join_array',
    'info', 'make_blocks', 'make_flds', 'nd_struct', 'reclass', 'scale',
    'stride', 'rolling_stats']

analysis:  (5)
    Tools for calculating distance, proximity, angles.
  __all__
  'compass', 'line_dir', 'not_closer', 'n_near', 'vincenty'

geom:  (12)
  Geometry related function
  __all_geo__
    '_view', '_reshape_', 'areas', 'center', 'centroid',  'e_area',
    'obj_array', 'e_dist', 'e_leng', 'seg_lengths', 'total_length', 'lengths'

graphing:
  Graphing capabilities using MatPlotLib as the basic graphing program
     plot_pnts_
stats:
  Statistics and related
    crosstab
other:
    Placeholder

examples:
    Documentation for *.py script, will have the same name but end with *.txt.


"""
from textwrap import dedent
from . import _common
from ._common import _describe, fc_info, fld_info
from . import a_io
from .a_io import *
from . import tools
from .tools import *
from . import apt
from .apt import *
from . import fc
from .fc import *
from . import frmts
from .frmts import *
from . import geom
from .geom import *
from . import analysis
from .analysis import *
from . import graphing
from .graphing import plot_pnts_
from . import stats
from .stats.cross_tab import crosstab


def __art_modules__():
    """print the array tools modules"""
    frmt = """\
-----------------------------------------------------------------------
Information on .... arraytools ....
More information can be obtained for the following modules...
Use ... dir(art.module) ... where 'module' is in...
- _common\n....{}
- a_io\n....{}
- apt\n....{}
- analysis\n....{}
- fc\n....{}
- frmts\n....{}
- geom\n....{}
- tools\n....{}
"""
    print(dedent(frmt).format(*__args))


__art_version__ = "Arraytools version 1.0"
__all__ = ['__art_version__', '__art_modules__']
__args = [_common.__all_common__, a_io.__all_aio__, analysis.__all__,
          apt.__all_apt__, fc.__all_fc__, frmts.__all_frmt__,
          geom.__all_geo__, tools.__all_art__]
for _arg in __args:
    __all__.extend(_arg)

__all__.sort()
del _arg
