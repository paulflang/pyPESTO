import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from .clust_color import assign_color


def parameters(result, ax=None):
    """
    Plot parameter values.

    Parameters
    ----------

    result: pypesto.Result
        Optimization result obtained by 'optimize.py'.

    ax: matplotlib.Axes, optional
        Axes object to use.

    Returns
    -------

    ax: matplotlib.Axes
        The plot axes.
    """

    result_fval = result.optimize_result.get_for_key('fval')
    result_x = result.optimize_result.get_for_key('x')
    lb = result.problem.lb
    ub = result.problem.ub

    return parameters_lowlevel(result_x, result_fval, lb, ub, ax,)


def parameters_lowlevel(xs, fvals, lb=None, ub=None, ax=None):

    """
    Plot waterfall plot using list of cost function values.

    Parameters
    ----------

    xs: nested list or array
        Including optimized parameters for each startpoint.

    fvals: numeric list or array
        Including values need to be plotted.

    lb, ub: array_like, optional
        The lower and upper bounds.

    ax: matplotlib.Axes, optional
        Axes object to use.

    Returns
    -------

    ax: matplotlib.Axes
        The plot axes.
    """

    if ax is None:
        ax = plt.subplots()[1]

    n_fvals = len(fvals)

    fvals = np.reshape(fvals, [n_fvals, 1])

    # assign color
    colors = assign_color(fvals)

    # parameter indices
    parameters_ind = range(1, len(xs[0]) + 1)

    # plot parameters
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for j_x, x in reversed(list(enumerate(xs))):
        ax.plot(x, parameters_ind, color=colors[j_x], marker='o')

    # draw bounds
    if lb is not None:
        ax.plot(lb[0], parameters_ind, 'b--', marker='+')
    if ub is not None:
        ax.plot(ub[0], parameters_ind, 'b--', marker='+')

    ax.set_xlabel('Parameter value')
    ax.set_ylabel('Parameter index')
    ax.set_title('Estimated parameters')

    return ax
