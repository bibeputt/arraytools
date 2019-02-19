# -*- coding: utf-8 -*-
"""
===========
geom_create
===========

Script :   create.py

Author :   Dan_Patterson@carleton.ca

Modified : 2019-02-18

Purpose :  Tools for creating arrays of various geometric shapes

Notes
-----
Part of the `arraytools` module.  See circular in arraytools.geomtools.circular
for some implementation examples.

References

"""
# pylint: disable=C0103  # invalid-name
# pylint: disable=R0914  # Too many local variables
# pylint: disable=R1710  # inconsistent-return-statements
# pylint: disable=W0105  # string statement has no effect

import sys
import numpy as np


ft = {'bool': lambda x: repr(x.astype(np.int32)),
      'float_kind': '{: 0.3f}'.format}
np.set_printoptions(edgeitems=10, linewidth=80, precision=2, suppress=True,
                    threshold=100, formatter=ft)
np.ma.masked_print_option.set_display('-')  # change to a single -

script = sys.argv[0]  # print this should you need to locate the script

__all__ = ['arc_', 'arc_sector',
           'circle', 'circle_mini', 'circle_ring',
           'ellipse',
           'hex_flat', 'hex_pointy',
           'convex',
           'mesh_xy',
           'pyramid',
           'rectangle',
           'triangle',
           'pnt_from_dist_bearing',
           'xy_grid',
           'transect_lines'
           ]
# ---- helpers ---- rot_matrix -----------------------------------------------
#
def rot_matrix(angle=0, nm_3=False):
    """Return the rotation matrix given points and rotation angle

    Parameters
    ----------
      - rotation angle in degrees and whether the matrix will be used with
        homogenous coordinates

    Returns
    -------
    - rot_m - rotation matrix for 2D transform
    - rotate around  translate(-x, -y).rotate(theta).translate(x, y)
    """
    rad = np.deg2rad(angle)
    c = np.cos(rad)
    s = np.sin(rad)
    rm = np.array([[c, -s, 0.],
                   [s, c, 0.],
                   [0., 0., 1.]])
    if not nm_3:
        rm = rm[:2, :2]
    return rm


# ---- arc_sector, convex hull, circle ellipse, hexagons, rectangles,
#      triangle, xy-grid --
#
def arc_(radius=100, start=0, stop=1, step=0.1, xc=0.0, yc=0.0):
    """Create an arc from a specified radius, centre and start/stop angles

    Parameters
    ----------
    radius : number
        cirle radius from which the arc is obtained
    start, `stop`, `step` : numbers
        angles in degrees
    xc, yc : number
        center coordinates in projected units
    as_list : boolean
        False, returns an array.  True yields a list
   
    Returns
    -------
      Points on the arc as either a list or array
    """
    start, stop = sorted([start, stop])
    angle = np.deg2rad(np.arange(start, stop, step))
    x_s = radius*np.cos(angle)         # X values
    y_s = radius*np.sin(angle)         # Y values
    pnts = np.array([x_s, y_s]).T + [xc, yc]
    return pnts


def arc_sector(outer=10, inner=9, start=1, stop=6, step=0.1):
    """Form an arc sector bounded by a distance specified by two radii

    Parameters
    ----------
    outer : number
        outer radius of the arc sector
    inner : number
        inner radius
   `start : number
        start angle of the arc
    stop : number
        end angle of the arc
    step : number
        the angle densification step

    Requires
    --------
      `arc_` is used to produce the arcs, the top arc is rotated clockwise and
      the bottom remains in the order produced to help form closed-polygons.
    """
    s_s = [start, stop]
    s_s.sort()
    start, stop = s_s
    top = arc_(outer, start, stop, step, 0.0, 0.0)
    top = top[::-1]
    bott = arc_(inner, start, stop, step, 0.0, 0.0)
    close = top[0]
    pnts = np.concatenate((top, bott, [close]), axis=0)
    return pnts


def circle(radius=100, clockwise=True, theta=1, rot=0.0, scale=1,
           xc=0.0, yc=0.0):
    """Produce a circle/ellipse depending on parameters.

    Parameters
    ----------
    radius : number
        in projected units
    clockwise : boolean
        True for clockwise (outer rings), False for counter-clockwise
        (for inner rings)
    theta : number
        Angle spacing. If theta=1, angles between -180 to 180, are returned
        in 1 degree increments. The endpoint is excluded.
    rot : number
         rotation angle in degrees... used if scaling is not equal to 1
    scale : number
         For ellipses, change the scale to <1 or > 1. The resultant
         y-values will favour the x or y-axis depending on the scaling.

    Returns
    -------
      list of coordinates for the circle/ellipse

    Notes
    -----
     You can also use np.linspace if you want to specify point numbers.
     np.linspace(start, stop, num=50, endpoint=True, retstep=False)
     np.linspace(-180, 180, num=720, endpoint=True, retstep=False)
    """
    if clockwise:
        angles = np.deg2rad(np.arange(180.0, -180.0-theta, step=-theta))
    else:
        angles = np.deg2rad(np.arange(-180.0, 180.0+theta, step=theta))
    x_s = radius*np.cos(angles)            # X values
    y_s = radius*np.sin(angles) * scale    # Y values
    pnts = np.array([x_s, y_s]).T
    if rot != 0:
        rot_mat = rot_matrix(angle=rot)
        pnts = (np.dot(rot_mat, pnts.T)).T
    pnts = pnts + [xc, yc]
    return pnts


def circle_mini(radius=1.0, theta=10.0, xc=0.0, yc=0.0):
    """Produce a circle/ellipse depending on parameters.

    Parameters
    ----------
    radius : number
        Distance from centre
    theta : number
        Angle of densification of the shape around 360 degrees

    """
    angles = np.deg2rad(np.arange(180.0, -180.0-theta, step=-theta))
    x_s = radius*np.cos(angles) + xc    # X values
    y_s = radius*np.sin(angles) + yc    # Y values
    pnts = np.array([x_s, y_s]).T
    return pnts


def circle_ring(outer=100, inner=0, theta=10, rot=0, scale=1, xc=0.0, yc=0.0):
    """Create a multi-ring buffer around a center point (xc, yc)

    Parameters
    ----------
    outer : number
        outer radius
    inner : number
        inner radius
    theta : number
        See below
    rot : number
        rotation angle, used for non-circles
    scale : number
         used to scale the y-coordinates

    Notes
    -----
    Angles to use to densify the circle::

    - 360+ for circle
    - 120 for triangle
    - 90  for square
    - 72  for pentagon
    - 60  for hexagon
    - 45  for octagon
    - etc
    """
    top = circle(outer, clockwise=True, theta=theta, rot=rot,
                 scale=scale, xc=xc, yc=yc)
    if inner == 0.0:
        return top    
    bott = circle(inner, clockwise=False, theta=theta, rot=rot,
                  scale=scale, xc=xc, yc=yc)
    return np.concatenate((top, bott), axis=0)


def ellipse(x_radius=1.0, y_radius=1.0, theta=10., xc=0.0, yc=0.0):
    """Produce an ellipse depending on parameters.

    Parameters
    ----------
    radius : number
        Distance from centre in the X and Y directions
    theta : number
        Angle of densification of the shape around 360 degrees
    """
    angles = np.deg2rad(np.arange(180.0, -180.0-theta, step=-theta))
    x_s = x_radius*np.cos(angles) + xc    # X values
    y_s = y_radius*np.sin(angles) + yc    # Y values
    pnts = np.concatenate((x_s, y_s), axis=0)
    return pnts


def hex_flat(dx=1, dy=1, cols=1, rows=1):
    """Generate the points for the flat-headed hexagon

    Parameters
    ----------
    dy_dx : number
        The radius width, remember this when setting hex spacing
    dx : number
        Increment in x direction, +ve moves west to east, left/right
    dy : number
        Increment in y direction, -ve moves north to south, top/bottom
    """
    f_rad = np.deg2rad([180., 120., 60., 0., -60., -120., -180.])
    X = np.cos(f_rad) * dy
    Y = np.sin(f_rad) * dy            # scaled hexagon about 0, 0
    seed = np.array(list(zip(X, Y)))  # array of coordinates
    dx = dx * 1.5
    dy = dy * np.sqrt(3.)/2.0
    hexs = [seed + [dx * i, dy * (i % 2)] for i in range(0, cols)]
    m = len(hexs)
    for j in range(1, rows):  # create the other rows
        hexs += [hexs[h] + [0, dy * 2 * j] for h in range(m)]
    return hexs


def hex_pointy(dx=1, dy=1, cols=1, rows=1):
    """Pointy hex angles, convert to sin, cos, zip and send.  Also called
    ``traverse hexagons`` by some.

    Parameters
    ----------
    dy_dx - number
        The radius width, remember this when setting hex spacing
    dx : number
        Increment in x direction, +ve moves west to east, left/right
    dy : number
        Increment in y direction, -ve moves north to south, top/bottom
    """
    p_rad = np.deg2rad([150., 90, 30., -30., -90., -150., 150.])
    X = np.cos(p_rad) * dx
    Y = np.sin(p_rad) * dy      # scaled hexagon about 0, 0
    seed = np.array(list(zip(X, Y)))
    dx = dx * np.sqrt(3.)/2.0
    dy = dy * 1.5
    hexs = [seed + [dx * i * 2, 0] for i in range(0, cols)]
    m = len(hexs)
    for j in range(1, rows):  # create the other rows
        hexs += [hexs[h] + [dx * (j % 2), dy * j] for h in range(m)]
    return hexs


def convex(points):
    """Calculates the convex hull for given points
    :Input is a list of 2D points [(x, y), ...]
    """
    def _cross_(o, a, b):
        """Cross-product for vectors o-a and o-b
        """
        xo, yo = o
        xa, ya = a
        xb, yb = b
        return (xa - xo)*(yb - yo) - (ya - yo)*(xb - xo)
    #
    if isinstance(points, np.ndarray):
        points = points.tolist()
        points = [tuple(i) for i in points]
    points = sorted(set(points))  # Remove duplicates
    if len(points) <= 1:
        return points
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and _cross_(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and _cross_(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    #print("lower\n{}\nupper\n{}".format(lower, upper))
    return np.array(lower[:-1] + upper)  # upper[:-1]) # for open loop


def mesh_xy(L=0, B=0, R=5, T=5, dx=1, dy=1, as_rec=True):
    """Create a mesh of coordinates within the specified X, Y ranges

    Parameters
    ----------
    L(eft), R(ight), dx : number
        Coordinate min, max and delta x for X axis
    B(ott), T(op), dy  : number
        Same as above for Y axis
    as_rec : boolean
        Produce a structured array (or convert to a record array)

    Returns
    -------
    -  A list of coordinates of X,Y pairs and an ID if as_rec is True.
    -  A mesh grid X and Y coordinates is also produced.

    See Also
    --------
    `mesh_pnts.py` in arraytools.geomtools
    """
    dt = [('Pnt_num', '<i4'), ('X', '<f8'), ('Y', '<f8')]
    x = np.arange(L, R + dx, dx, dtype='float64')
    y = np.arange(B, T + dy, dy, dtype='float64')
    mesh = np.meshgrid(x, y, sparse=False)
    if as_rec:
        xs = mesh[0].ravel()
        ys = mesh[1].ravel()
        p = list(zip(np.arange(len(xs)), xs, ys))
        pnts = np.array(p, dtype=dt)
    else:
        p = list(zip(mesh[0].ravel(), mesh[1].ravel()))
        pnts = np.array(p)
    return pnts, mesh


def pyramid(core=9, steps=10, incr=(1, 1), posi=True):
    """Create a pyramid see pyramid_demo.py"""
    a = np.array([core])
    a = np.atleast_2d(a)
    for i in range(1, steps):
        val = core - i
        if posi and (val <= 0):
            val = 0
        a = np.lib.pad(a, incr, "constant", constant_values=(val, val))
    return a


def rectangle(dx=1, dy=1, cols=1, rows=1):
    """Create the array of pnts to construct a rectangle.

    Parameters
    ----------
    dx : number
        Increment in x direction, +ve moves west to east, left/right
    dy : number
        Increment in y direction, -ve moves north to south, top/bottom
    rows, cols : ints
        The number of rows and columns to produce
    """
    X = [0.0, 0.0, dx, dx, 0.0]       # X, Y values for a unit square
    Y = [0.0, dy, dy, 0.0, 0.0]
    seed = np.array(list(zip(X, Y)))  # [dx0, dy0] keep for insets
    a = [seed + [j * dx, i * dy]       # make the shapes
         for i in range(0, rows)   # cycle through the rows
         for j in range(0, cols)]  # cycle through the columns
    a = np.asarray(a)
    return a


def triangle(dx=1, dy=1, cols=1, rows=1):
    """Create a row of meshed triangles.

    Parameters
    ----------
    dx : number
        Increment in x direction, +ve moves west to east, left/right
    dy : number
        Increment in y direction, -ve moves north to south, top/bottom
    rows, cols : ints
        The number of rows and columns to produce
    """
    grid_type = 'triangle'
    a, dx, b = dx/2.0, dx, dx*1.5
    Xu = [0.0, a, dx, 0.0]   # X, Y values for a unit triangle, point up
    Yu = [0.0, dy, 0.0, 0.0]
    Xd = [a, b, dx, a]       # X, Y values for a unit triangle, point down
    Yd = [dy, dy, 0.0, dy]   # shifted by dx
    seedU = np.vstack((Xu, Yu)).T  # np.array(list(zip(Xu, Yu)))
    seedD = np.vstack((Xd, Yd)).T  # np.array(list(zip(Xd, Yd)))
    seed = np.array([seedU, seedD])
    a = [seed + [j * dx, i * dy]       # make the shapes
         for i in range(0, rows)       # cycle through the rows
         for j in range(0, cols)]      # cycle through the columns
    a = np.asarray(a)
    s1, s2, s3, s4 = a.shape
    a = a.reshape(s1*s2, s3, s4)
    return a, grid_type


def pnt_from_dist_bearing(orig=(0, 0), bearings=None, dists=None, prn=False):
    """Point locations given distance and bearing from an origin.
    Calculate the point coordinates from distance and angle

    References
    ----------
    `<https://community.esri.com/thread/66222>`_.

    `<https://community.esri.com/blogs/dan_patterson/2018/01/21/
    origin-distances-and-bearings-geometry-wanderings>`_.

    Notes
    -----
    Sample calculation::

        bearings = np.arange(0, 361, 22.5)  # 17 bearings
        dists = np.random.randint(10, 500, len(bearings)) * 1.0  OR
        dists = np.full(bearings.shape, 100.)
        data = dist_bearing(orig=orig, bearings=bearings, dists=dists)

    Create a featureclass from the results::

        shapeXY = ['X_to', 'Y_to']
        fc_name = 'C:/path/Geodatabase.gdb/featureclassname'
        arcpy.da.NumPyArrayToFeatureClass(out, fc_name,
                                          ['X_to', 'Y_to'], "2951")
        # ... syntax
        arcpy.da.NumPyArrayToFeatureClass(in_array=out,
                                          out_table=fc_name,
                                          shape_fields=shapeXY,
                                          spatial_reference=SR)
    """
    if bearings is None and dists is None:
        return "origin with distances and bearings required"
    orig = np.array(orig)
    rads = np.deg2rad(bearings)
    dx = np.sin(rads) * dists
    dy = np.cos(rads) * dists
    x_t = np.cumsum(dx) + orig[0]
    y_t = np.cumsum(dy) + orig[1]
    stack = (x_t, y_t, dx, dy, dists, bearings)
    names = ["X_to", "Y_to", "orig_dx", "orig_dy", "distance", "bearing"]
    data = np.vstack(stack).T
    N = len(names)
    if prn:  # ---- just print the results ----------------------------------
        frmt = "Origin ({}, {})\n".format(*orig) + "{:>10s}"*N
        print(frmt.format(*names))
        frmt = "{: 10.2f}"*N
        for i in data:
            print(frmt.format(*i))
        return data
    # ---- produce a structured array from the output -----------------------
    names = ", ".join(names)
    kind = ["<f8"]*N
    kind = ", ".join(kind)
    out = data.transpose()
    out = np.core.records.fromarrays(out, names=names, formats=kind)
    return out

def xy_grid(x, y=None, top_left=True):
    """Create a 2D array of locations from x, y values.  The values need not
    be uniformly spaced just sequential. Derived from `meshgrid` in References.

    Parameters
    ----------
    x, y : array-like
        To form a mesh, there must at least be 2 values in each sequence
    top_left: boolean
        True, y's are sorted in descending order, x's in ascending

    References
    ----------
    `<https://github.com/numpy/numpy/blob/master/numpy/lib/function_base.py>`_.
    """
    if y is None:
        y = x
    if x.ndim != 1:
        return "A 1D array required"
    xs = np.sort(np.asanyarray(x))
    ys = np.asanyarray(y)
    if top_left:
        ys = np.argsort(-ys)
    xs = np.reshape(xs, newshape=((1,) + xs.shape))
    ys = np.reshape(ys, newshape=(ys.shape + (1,)))
    xy = [xs, ys]
    xy = np.broadcast_arrays(*xy, subok=True)
    shp = np.prod(xy[0].shape)
    final = np.zeros((shp, 2), dtype=xs.dtype)
    final[:, 0] = xy[0].ravel()
    final[:, 1] = xy[1].ravel()
    return final


def transect_lines(N=5, orig=None, dist=1, x_offset=0, y_offset=0,
                   bearing=0, as_ndarray=True):
    """Construct transect lines from origin-destination points given a
    distance and bearing from the origin point

    Parameters
    ----------
    N : number
        The number of transect lines
    orig : array-like
         A single origin.  If None, the cartesian origin (0, 0) is used
    dist : number or array-like
        The distance(s) from the origin
    x_offset, y_offset : number
        If the `orig` is a single location, you can construct offset lines
        using these values
    bearing : number or array-like
        If a single number, parallel lines are produced. An array of values
        equal to the `orig` can be used.

    Returns
    -------
    Two outputs are returned, the first depends on the `as_ndarray` setting.

    1. True, a structured array. False - a recarray
    2. An ndarray with the field names in case the raw data are required.

    Notes
    -----
    It is easiest of you pick a `corner`, then use x_offset, y_offset to
    control whether you are moving horizontally and vertically from the origin.
    The bottom left is easiest, and positive offsets move east and north from.

    Use XY to Line tool in ArcGIS Pro to convert the from/to pairs to a line.
    See references

    Examples
    --------
    >>> out, data = transect_lines(N=5, orig=None,
                                   dist=100, x_offset=10,
                                   y_offset=0, bearing=45, as_ndarray=True)
    >>> data
    array([[  0.  ,   0.  ,  70.71,  70.71],
           [ 10.  ,   0.  ,  80.71,  70.71],
           [ 20.  ,   0.  ,  90.71,  70.71],
           [ 30.  ,   0.  , 100.71,  70.71],
           [ 40.  ,   0.  , 110.71,  70.71]])
    >>> out
    array([( 0., 0.,  70.71, 70.71), (10., 0.,  80.71, 70.71),
    ...    (20., 0.,  90.71, 70.71), (30., 0., 100.71, 70.71),
    ...    (40., 0., 110.71, 70.71)],
    ...   dtype=[('X_from', '<f8'), ('Y_from', '<f8'),
    ...          ('X_to', '<f8'), ('Y_to', '<f8')])
    ...
    ... Create the table and the lines
    >>> tbl = 'c:/folder/your.gdb/table_name'
    >>> # arcpy.da.NumPyArrayToTable(a, tbl)
    >>> # arcpy.XYToLine_management(
    ... #       in_table, out_featureclass,
    ... #       startx_field, starty_field, endx_field, endy_field,
    ... #       {line_type}, {id_field}, {spatial_reference}
    ... This is general syntax, the first two are paths of source and output
    ... files, followed by coordinates and options parameters.
    ...
    ... To create compass lines
    >>> b = np.arange(0, 361, 22.5)
    >>> a, data = transect_lines(N=10, orig=[299000, 4999000],
                                 dist=100, x_offset=0, y_offset=0,
                                 bearing=b, as_ndarray=True)

    References
    ----------
    `<https://community.esri.com/blogs/dan_patterson/2019/01/17/transect-
    lines-parallel-lines-offset-lines>`_.

    `<http://pro.arcgis.com/en/pro-app/tool-reference/data-management
    /xy-to-line.htm>`_.
    """
    def _array_struct_(a, fld_names=['X', 'Y'], kinds=['<f8', '<f8']):
        """Convert an array to a structured array"""
        dts = list(zip(fld_names, kinds))
        z = np.zeros((a.shape[0],), dtype=dts)
        for i in range(a.shape[1]):
            z[fld_names[i]] = a[:, i]
        return z
    #
    if orig is None:
        orig = np.array([0., 0.])
    args = [orig, dist, bearing]
    arrs = [np.atleast_1d(i) for i in args]
    orig, dist, bearing = arrs
    # o_shp, d_shp, b_shp = [i.shape for i in arrs]
    #
    rads = np.deg2rad(bearing)
    dx = np.sin(rads) * dist
    dy = np.cos(rads) * dist
    #
    n = len(bearing)
    N = [N, n][n > 1]  # either the number of lines or bearings
    x_orig = np.arange(N) * x_offset + orig[0]
    y_orig = np.arange(N) * y_offset + orig[1]
    x_dest = x_orig + dx
    y_dest = y_orig + dy
    # ---- create the output array
    names = ['X_from', 'Y_from', 'X_to', 'Y_to']
    cols = len(names)
    kind = ['<f8']*cols
    data = np.vstack([x_orig, y_orig, x_dest, y_dest]).T
    if as_ndarray:  # **** add this as a flag
        out = _array_struct_(data, fld_names=names, kinds=kind)
    else:
        out = data.transpose()
        out = np.core.records.fromarrays(out, names=names, formats=kind)
    return out, data
# ----------------------------------------------------------------------
# __main__ .... code section
if __name__ == "__main__":
    print("Script path {}".format(script))
