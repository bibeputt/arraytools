# -*- coding: UTF-8 -*-
"""
:Script:   cross_tab.py
:Author:   Dan.Patterson@carleton.ca
:Modified: 2017-09-29
:Purpose:  Crosstabulate data
:Notes:
:
:References:
: https://stackoverflow.com/questions/12983067/how-to-find-unique-vectors-of
:         -a-2d-array-over-a-particular-axis-in-a-vectorized
: https://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array
: http://stackoverflow.com/questions/38030054/
:      create-adjacency-matrix-in-python-for-large-dataset
: np.unique
: in the newer version, they use flags to get the sums
:
"""
import sys
import numpy as np
import arcpy
from textwrap import indent

ft = {'bool': lambda x: repr(x.astype('int32')),
      'float': '{: 0.3f}'.format}
np.set_printoptions(edgeitems=50, linewidth=80, precision=2,
                    suppress=True, threshold=100,
                    formatter=ft)
np.ma.masked_print_option.set_display('-')

script = sys.argv[0]


def tweet(msg):
    """Print a message for both arcpy and python.
    : msg - a text message
    """
    m = "\n{}\n".format(msg)
    arcpy.AddMessage(m)
    print(m)
    print(arcpy.GetMessages())


def crosstab(row, col, verbose=False):
    """Crosstabulate 2 data arrays, shape (N,), using np.unique.
    :  scipy.sparse has similar functionality and is faster for large arrays.
    :
    :Requires:  A 2D array of data with shape(N,) representing two variables
    :--------
    : row - row variable
    : col - column variable
    :
    :Useage:
    :------
    :  float_min = np.finfo(np.float).min
    :  float_max = np.finfo(np.float).max
    :  int_min = np.iinfo(np.int_).min
    :  int_max = np.iinfo(np.int_).max
    :  f = r'C:\some\path\your.gdb\your_featureclass'
    :  null_dict = {'Int_fld': int_min, 'Float_fld': float_min}  # None strings
    :
    :  flds = ['Int_field', 'Txt01', 'Txt02']  # 2 text fields
    :  t = arcpy.da.TableToNumPyArray(in_table=f, field_names=flds,
    :                                 skip_nulls=False)
    :                                 # , null_value=null_dict) if needed
    :  rows = t['Txt01']
    :  cols = t['Txt02']
    :  ctab, a, result, r, c = crosstab(rows, cols, verbose=False)
    :Returns:
    : ctab - the crosstabulation result as row, col, count array
    : a - the crosstabulation in a row, col, count, but filled out whether a
    :     particular combination exists or not.
    : r, c - unique values/names for the row and column variables
    :
    """
    def _prn(r, c, a):
        """fancy print formatting.
        """
        r_sze = max(max([len(i) for i in r]), 8)
        c_sze = [max(len(str(i)), 5) for i in c]
        f_0 = '{{!s:<{}}} '.format(r_sze)
        f_1 = ('{{!s:>{}}} '*len(c)).format(*c_sze)
        frmt = f_0 + f_1
        hdr = 'Result' + '_' * (r_sze-7)
        txt = [frmt.format(hdr, *c)]
        txt2 = txt + [frmt.format(r[i], *a[i]) for i in range(len(r))]
        result = "\n".join(txt2)
        return result

    dt = np.dtype([('row', row.dtype), ('col', col.dtype)])
    rc = np.asarray(list(zip(row, col)), dtype=dt)
    r = np.unique(row)
    c = np.unique(col)
    u, idx, inv, cnt = np.unique(rc, return_index=True, return_inverse=True,
                                 return_counts=True)
    rcc_dt = u.dtype.descr
    rcc_dt.append(('Count', '<i4'))
    ctab = np.asarray(list(zip(u['row'], u['col'], cnt)), dtype=rcc_dt)
    a = np.zeros((len(r), len(c)), dtype=np.int_)
    rc = [[(np.where(r == i[0])[0]).item(),
           (np.where(c == i[1])[0]).item()] for i in ctab]
    for i in range(len(ctab)):
        rr, cc = rc[i]
        a[rr, cc] = ctab[i][2]
    result = _prn(r, c, a)
    if verbose:
        tweet(result)
    return ctab, a, result, r, c


frmt = """
Crosstab results ....
{}\n
The array of counts/frequencies....
{}\n
Row and column headers...
{}
{}\n
And as a fancy output which can be saved to a csv file using
....np.savetxt('c:/path/file_name.csv', array_name, fmt= '%s', delimiter=', ')
{}
"""


if len(sys.argv) == 1:
    pass
else:
    in_tbl = sys.argv[1]
    row_fld = sys.argv[2]
    col_fld = sys.argv[3]
    flds = [row_fld, col_fld]
    t = arcpy.da.TableToNumPyArray(in_table=in_tbl, field_names=flds,
                                   skip_nulls=False)  # , null_value=null_dict)
    rows = t[row_fld]
    cols = t[col_fld]
    ctab, a, result, r, c = crosstab(rows, cols, verbose=True)
    args = [in_tbl, row_fld, col_fld]
    msg = "\nTable {}\nrow field {}\ncol field {}".format(*args)
    tweet(msg)

if __name__ == "__main__":
    """run crosstabulation with data"""
#    ctab, a, result, r, c = _demo()
