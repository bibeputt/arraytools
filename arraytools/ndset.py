# -*- coding: utf-8 -*-
"""
ndset
=====

Script :   ndset.py

Author :   Dan_Patterson@carleton.ca

Modified : 2018-12-10

Purpose
-------
This set of functions is largely directed to extending some of numpy set
functions to apply to Nxd shaped arrays as well as structured and recarrays.
The functionality largely depends on using a `view` of the input array so that
each row can be treated as a unique record in the array.

If you are working with arrays and wish to perform functions on certain columns
then you will have to preprocess/preselect.  You can only add so much to a 
function before it loses its readability and utility.

**ndset**
::
  _view_as_, is_in, nd_diff, nd_diffxor, nd_intersect, nd_union, nd_uniq

Notes:
------
_view_as_(a)
    >>> a = np.array([[  0,   0], [  0, 100], [100, 100]])
    >>> _view_as_(a)
    ... array([[(  0,   0)],
    ...        [(  0, 100)],
    ...        [(100, 100)]], dtype=[('f0', '<i4'), ('f1', '<i4')])

is_in
    >>> a = np.array([[  0,   0], [  0, 100], [100, 100]])
    >>> look_for = np.array([[  0, 100], [100, 100]])
    >>> is_in(a, look_for, reverse=False)
    array([[  0, 100],
    ...    [100, 100]])
    >>> is_in(a, look_for, reverse=True)
    array([[0, 0]])

For the following:
    >>> a = np.array([[  0,   0], [  0, 100], [100, 100]])
    >>> b = np.array([[  0, 100], [100, 100]])
    >>> c = np.array([[ 20, 20], [100, 20], [100, 0], [ 0, 0]])

nd_diff(a, b)
    >>> nd_diff(a, b)
    array([[0, 0]])

nd_diffxor(a, b, uni=False)
    >>> nd_diffxor(a, c, uni=False)
    array([[  0, 100],
           [ 20,  20],
           [100,   0],
           [100,  20],
           [100, 100]])

nd_intersect(a, b, invert=False)
    >>> nd_intersect(a, b, invert=False)
    array([[  0, 100],
           [100, 100]])
    >>> nd_intersect(a, c, invert=False)
    array([[0, 0]])

nd_union(a, b)
    >>> nd_union(a, c)
    array([[  0,   0],
           [  0, 100],
           [ 20,  20],
           [100,   0],
           [100,  20],
           [100, 100]])

nd_uniq(a, counts=False)
    >>> d = np.array([[ 0, 0], [100, 100], [100, 100], [ 0, 0]])
    nd_uniq(d)
    array([[  0,   0],
           [100, 100]])

References:
-----------
`<https://community.esri.com/blogs/dan_patterson/2016/10/23/numpy-lessons-5-
identical-duplicate-unique-different>`_.

`<https://github.com/numpy/numpy/blob/master/numpy/lib/arraysetops.py>`_.

"""
import sys
import numpy as np


ft = {'bool': lambda x: repr(x.astype(np.int32)),
      'float_kind': '{: 0.3f}'.format}
np.set_printoptions(edgeitems=10, linewidth=80, precision=2, suppress=True,
                    threshold=100, formatter=ft)
np.ma.masked_print_option.set_display('-')  # change to a single -

script = sys.argv[0]  # print this should you need to locate the script


__all__ = ['_view_as_',
           'is_in',
           'nd_diff',
           'nd_diffxor',
           'nd_intersect',
           'nd_union',
           'nd_uniq'
           ]


def _view_as_(a):
    """Key function to get uniform nd arrays to be viewed as structured arrays.
    A bit of trickery, but it works for all set-like functionality
    
    Parameters:
    -----------
    a : array
        ndarray to be viewed

    Returns:
    --------
    Array view as structured/recarray, with shape = (N, 1)

    See main documentation under ``Notes``.
    """
    if a.dtype.kind in ('O', 'V'):
        a = a.reshape(a.shape[0], 1)
    a_view = a.view(a.dtype.descr * a.shape[1])
    return a_view


def is_in(a, look_for, reverse=False):
    """Checks ndarray `a` for the presence of other records ndarray `look_for`

    Parameters:
    ----------
    arr : array
        the array to check for the elements
    look_for : number, list or array
        what to use for the check
    reverse : boolean
        Switch the query look_for to `True` to find those not in `a`
    """
    a_view = _view_as_(a)
    b_view = _view_as_(look_for)
    inv = False
    if reverse:
        inv = True
    idx = np.in1d(a_view, b_view, assume_unique=False, invert=inv)
    return a[idx]


def nd_diff(a, b, invert=True):
    """See nd_intersect.  This just returns the opposite/difference
    """
    diff = nd_intersect(a, b, invert=True)
    return diff


def nd_diffxor(a, b, uni=False):
    """using setxor... it is slower than nd_diff, 36 microseconds vs 18.2
    but this is faster for large sets
    """
    a_view = _view_as_(a)
    b_view = _view_as_(b)
    ab = np.setxor1d(a_view, b_view, assume_unique=uni)
    return ab.view(a.dtype).reshape(-1, a.shape[1])


def nd_intersect(a, b, invert=False):
    """Intersect of two, 2D arrays using views and in1d

    Parameters:
    -----------
    a, b : arrays
        Arrays are assumed to have a shape = (N, 2)

    `<https://github.com/numpy/numpy/blob/master/numpy/lib/arraysetops.py>`_.

    `<https://stackoverflow.com/questions/9269681/intersection-of-2d-
    numpy-ndarrays>`_.
    """
    a_view = _view_as_(a)
    b_view = _view_as_(b)
    if len(a) > len(b):
        idx = np.in1d(a_view, b_view, assume_unique=False, invert=invert)
        return a[idx] 
    else:
        idx = np.in1d(b_view, a_view, assume_unique=False, invert=invert)
        return b[idx] 


def nd_union(a, b):
    """Union view of arrays
    """
    a_view = _view_as_(a)
    b_view = _view_as_(b)
    ab= np.union1d(a_view, b_view)
    ab = np.unique(np.concatenate((a_view, b_view), axis=None))
    return ab.view(a.dtype).reshape(-1, a.shape[1]).squeeze()


def nd_uniq(a, counts=False):
    """Taken from, but modified for simple axis 0 and 1 and structured
    arrays in (N, m) or (N,) format.

    To enable determination of unique values in uniform arrays with
    uniform dtypes.  np.unique in versions < 1.13 need to use this.

    https://github.com/numpy/numpy/blob/master/numpy/lib/arraysetops.py
    """
    a_view = _view_as_(a)
    if counts:
        u, i, inv, cnts = np.unique(a_view, return_index=True,
                               return_inverse=True,
                               return_counts=counts)
        uni = a[np.sort(i)]
        return uni, cnts
    else:
        u, i = np.unique(a_view, return_index=True, return_counts=counts)
        uni = a[np.sort(i)]
        return uni
    
# ----------------------------------------------------------------------
# __main__ .... code section
if __name__ == "__main__":
    """Optionally...
    : - print the script source name.
    : - run the _demo
    """

