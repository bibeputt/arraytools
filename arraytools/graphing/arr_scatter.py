# -*- coding: UTF-8 -*-
"""
:Script:   arr_scatter.py
:Author:   Dan.Patterson@carleton.ca
:Modified: 2017-01-23
:
:Purpose:
:
:Notes:
:
:References:
:
:---------------------------------------------------------------------:
"""
# ---- imports, formats, constants ----

import sys
import numpy as np
import matplotlib
#matplotlib.use('TkAgg', warn=True, force=False)  # pythonwin use TkAgg,
matplotlib.use('QT5agg')  # don't work Agg, WX, QTAgg, QT4Agg
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle


ft = {'bool': lambda x: repr(x.astype('int32')),
      'float': '{: 0.3f}'.format}
np.set_printoptions(edgeitems=10, linewidth=80, precision=2,
                    suppress=True, threshold=100, formatter=ft)
np.ma.masked_print_option.set_display('-')

script = sys.argv[0]

# ---- functions ----


# noinspection PyDefaultArgument,PyShadowingNames,PyShadowingNames
def scatter_params(plt, fig, ax, title="Title", lbls=['X', 'Y']):
    """Default parameters for plots
    :Notes:
    :  ticklabel_format(useoffset), turns off scientific formatting
    """
    x_label, y_label = lbls
    font1 = {'family': 'sans-serif', 'color': 'black',
             'weight': 'bold', 'size': 8}  # set size to other values
    markers = ['o', 's', '+', '*', 'x']
    ax.set_aspect('equal', adjustable='box')
#    ax.margins(0.05)  # set a gap
    ax.ticklabel_format(style='sci', axis='both', useOffset=False)
    ax.set_xlabel(x_label, labelpad=12)
    ax.xaxis.label_position = 'bottom'
    ax.xaxis.label.set_fontsize(12)
#    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.set_ylabel(y_label, labelpad=12)
    ax.yaxis.label_position = 'left'
    ax.yaxis.label.set_fontsize(12)
    plt.title(title + "\n", loc='center', fontdict=font1, size=12)
    plt.tight_layout
    plt.grid(True)
    return plt, fig, ax


# noinspection PyDefaultArgument,PyShadowingNames,PyShadowingNames,
# PyShadowingNames,PyShadowingNames
def plot_pnts_(pnts, title='Title', r_c=False, lbls=['X', 'Y'], params=True):
    """Plot points for Nx2 array representing x,y or row,col data.
    :Requires:  see _params() to specify special parameters
    :--------
    :  pnts - point or row/column array
    :  r_c - boolean. If True, the y-axis is inverted to represent row-column
    :    formatting rather than x,y formatting.
    :Returns:
    :-------
    :  A scatterplot representing the data.  It is easier to modify the
    :  script below than to provide a whole load of input parameters.
    :----------
    """
    from matplotlib.markers import MarkerStyle
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1)
    markers = MarkerStyle.filled_markers
    # ---- optional parameter def ----
    if params:  # use parameter def
        plt, fig, ax = scatter_params(plt, fig, ax, title, lbls)
        x_min, y_min = pnts.min(axis=0) - [0.5, 0.5]
        x_max, y_max = pnts.max(axis=0) + [0.5, 0.5]
        #
        lbl = np.arange(len(pnts))
        for label, xpt, ypt in zip(lbl, pnts[:, 0], pnts[:, 1]):
            plt.annotate(label, xy=(xpt, ypt), xytext=(2, 2), size=8,
                         textcoords='offset points', ha='left', va='bottom')
        plt.xlim(x_min, x_max)
        if r_c:
            plt.ylim(y_max, y_min)
        else:
            plt.ylim(y_min, y_max)
    # ---- enable multiple point files ----
    if isinstance(pnts, (list, tuple)):
        i = 0
        for p in pnts:  # plot x, y using marker i.
            plt.scatter(p[:, 0], p[:, 1], marker=markers[i])
            i += 1
    else:
        plt.scatter(pnts[:, 0], pnts[:, 1])  # , marker=markers[0])
    plt.show()
#    plt.close()  # turn close back on in some IDEs
    return plt, ax


# ----------------------------------------------------------------------
# .... running script or testing code section
def _tool():
    """run when script is from a tool
    """
    in_fc = sys.argv[1]
    group_by = str(sys.argv[2])
    x_fld = int(sys.argv[3])
    y_fld = str(sys.argv[4])
#    out_type = str(sys.argv[5])
#    out_fc = sys.argv[6]
    return in_fc, x_fld, y_fld


gdb_pth = "/".join(script.split("/")[:-2]) + "/Data/Point_tools.gdb"

if len(sys.argv) == 1:
    testing = True
    in_fc = gdb_pth + r"/r_sorted"
    group_by = 'Group_'
    k_factor = 3
    hull_type = 'concave'  # 'convex'
    out_type = 'Polyline'
    out_fc = gdb_pth + r"/r_11"
else:
    testing = False
    in_fc, group_by, k_factor, hull_type, out_type, out_fc = _tool()


# noinspection PyShadowingNames,PyShadowingNames,PyShadowingNames
def _demo():
    """Plot 20 points which have a minimum 1 unit point spacing
    :
    """
    a = np.array([[0.4, 0.5], [1.2, 9.1], [1.2, 3.6], [1.9, 4.6],
                  [2.9, 5.9], [4.2, 5.5], [4.3, 3.0], [5.1, 8.2],
                  [5.3, 9.5], [5.5, 5.7], [6.1, 4.0], [6.5, 6.8],
                  [7.1, 7.6], [7.3, 2.0], [7.4, 1.0], [7.7, 9.6],
                  [8.5, 6.5], [9.0, 4.7], [9.6, 1.6], [9.7, 9.6]])
    plt, ax = plot_pnts_(a, title='Points no closer than... test',
                         r_c=False, lbls=['X-values', 'Y-values'],
                         params=True)
    return a, plt,  ax

# ---------------------------------------------------------------------
if __name__ == "__main__":
    """Main section...   """
#    print("Script... {}".format(script))
#    a, plt, ax = _demo()
