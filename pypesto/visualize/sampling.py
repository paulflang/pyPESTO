import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# TODO: add in requirements: seaborn

def get_data_to_plot(result, problem, i_chain, burn_in, n_steps):
    '''
    get the respective data as pandas dataframe which should be plotted.
    Parameters
    ----------
    result:
    problem:
    i_chain: int
        which chain should be plotted
    burn_in: int
        last index of burn_in phase
    n_steps: int
        defines a subset of values which should be plotted, every n_steps
        value is plotted
    '''

    # get parameters and fval results as numpy-arrays
    arr_param = np.array(result.sample_result['trace_x'][i_chain])
    # get each n_steps element, from the index burn_in until end of vector
    arr_param = arr_param[np.arange(burn_in, len(arr_param), n_steps)]
    arr_fval = np.array(result.sample_result['trace_fval'][i_chain])
    arr_fval = arr_fval[np.arange(burn_in, len(arr_fval), n_steps)]
    theta_lb = problem.lb
    theta_ub = problem.ub

    param_names = problem.x_names

    # transform nparray to pandas for the use of seaborn
    pd_params = pd.DataFrame(arr_param, columns=param_names)
    pd_fval = pd.DataFrame(data=arr_fval,
                           columns=['logPosterior'])

    pd_iter = \
        pd.DataFrame(
            data=np.arange(burn_in+1,result.sample_result['n_fval']+1, n_steps),
            columns=['iteration'])
    params_fval = pd.concat([pd_params,pd_fval,pd_iter],
                            axis=1, ignore_index=False)

    # some global parameters
    nr_params = arr_param.shape[1]                # number of parameters

    return nr_params, params_fval, theta_lb, theta_ub


def sampling_fval(result, problem, i_chain=0, burn_in=0, n_steps=1, figsize=None, fs = 12):
    """
    Plot logPosterior over iterations.

    Parameters
    ----------
    result: dict
        sampling specific results object
    problem:
    i_chain: int
        which chain/temperature should be plotted. Default: First Chain
    burn_in: int
        index of end of burn-in phase, from which index on it should be plotted
    n_steps: int
        defines a subset of values which should be plotted, every n_steps
        value is plotted
    figsize: ndarray
        size of the figure, e.g. [10,5]
    fs: int
        fontsize

    Return
    --------
    ax: matplotlib-axes
    """
    # get data which should be plotted
    _, params_fval, _, _= get_data_to_plot(result,
                                           problem,
                                           i_chain,
                                           burn_in,
                                           n_steps)

    fig, ax = plt.subplots(figsize =figsize)

    sns.set(style="ticks")
    kwargs = {'edgecolor': "w",  # for edge color
              'linewidth': 0.3,
              's': 10}
    ax = sns.scatterplot(x="iteration", y="logPosterior", data=params_fval,
                         **kwargs)

    ax.set_xlabel('iteration index', fontsize = fs)
    ax.set_ylabel('log-posterior', fontsize = fs)
    if i_chain > 1:
        ax.set_title('Temperature chain: ' + str(i_chain), fontsize=fs)
    ax.set_xlim([burn_in,result.sample_result.n_fval +2])

    sns.despine()

    plt.show()

    return ax


def sampling_parameters(result,
                        problem,
                        i_chain=0,
                        burn_in=0,
                        n_steps=1,
                        show_lb_ub=False,
                        figsize=None,
                        fs = 12):
    """
    Plot parameter values over iterations
    Parameters
    ----------
    result: dict
        sampling specific results object
    problem:
    i_chain: int
        which chain/temperature should be plotted. Default: First Chain
    burn_in: int
        index of end of burn-in phase, from which index on it should be plotted
    n_steps: int
        defines a subset of values which should be plotted, every n_steps
        value is plotted
    show_lb_ub: bool
        defines if the y-limits shall be the lower and upper bounds of
        parameter estimation problem
    figsize: ndarray
        size of the figure, e.g. [10,5]
    fs: int
        fontsize

    Return
    --------
    ax: matplotlib-axes
    """
    # get data which should be plotted
    nr_params, params_fval, theta_lb, theta_ub = \
        get_data_to_plot(result, problem, i_chain, burn_in, n_steps)
    param_names = params_fval.columns.values[0:nr_params]

    # compute, how many rows and columns we need for the subplots
    num_row = int(np.round(np.sqrt(nr_params)))
    num_col = int(np.ceil(nr_params / num_row))

    fig, axes = plt.subplots(num_row,num_col, squeeze=False, figsize=figsize)
    axes = dict(zip(param_names, axes.flat))

    sns.set(style="ticks")
    kwargs = {'edgecolor': "w",  # for edge color
              'linewidth': 0.3,
              's': 10}

    for idx, plot_id in enumerate(param_names):
        ax = axes[plot_id]
        ax = sns.scatterplot(x="iteration", y=plot_id, data=params_fval, ax=ax,
                             **kwargs)

        ax.set_xlabel('iteration index', fontsize=fs)
        ax.set_ylabel(param_names[idx], fontsize=fs)
        if show_lb_ub:
            ax.set_ylim([theta_lb[idx],theta_ub[idx]])

    ax.set_xlim([burn_in, result.sample_result.n_fval + 2])
    if i_chain > 1:
        fig.suptitle('Temperature chain: ' + str(i_chain), fontsize=fs)
    fig.tight_layout()
    sns.despine()
    plt.show()

    return ax


def sampling_scatter(result,
                     problem,
                     i_chain=0,
                     burn_in=0,
                     n_steps=1,
                     figsize=None,
                     fs=12):
    """
    Plot parameter correlations.

    Parameters
    ----------
    result: dict
        sampling specific results object
    problem:
    i_chain: int
        which chain/temperature should be plotted. Default: First Chain
    burn_in: int
        index of end of burn-in phase, from which index on it should be plotted
    n_steps: int
        defines a subset of values which should be plotted, every n_steps
        value is plotted
    figsize: ndarray
        size of the figure, e.g. [10,5]
    fs: int
        fontsize

    Return
    --------
    ax: matplotlib-axes
    """

    # get data which should be plotted
    nr_params, params_fval, theta_lb, theta_ub = \
        get_data_to_plot(result, problem, i_chain, burn_in, n_steps)

    sns.set(style="ticks")

    ax = sns.pairplot(params_fval.drop(['logPosterior', 'iteration'], axis=1))

    if i_chain > 1:
        ax.fig.suptitle('Temperature chain: ' + str(i_chain), fontsize=fs)

    return ax


def sampling_marginal(result, problem, i_chain=0, figsize=None, fs=12):
    """
    Plot Marginals.

    Parameters
    ----------
    result: dict
        sampling specific results object
    problem:
    i_chain: int
        which chain/temperature should be plotted. Default: First Chain
    bw: float
        bandwidth, softening of the kde-curve
    figsize: ndarray
        size of the figure, e.g. [10,5]
    fs: int
        fontsize

    Return
    --------
    ax: matplotlib-axes
    """
    # get data which should be plotted
    nr_params, params_fval, theta_lb, theta_ub = \
        get_data_to_plot(result, problem, i_chain, burn_in=0, n_steps=1)
    param_names = params_fval.columns.values[0:nr_params]

    # compute, how many rows and columns we need for the subplots
    num_row = int(np.round(np.sqrt(nr_params)))
    num_col = int(np.ceil(nr_params / num_row))

    fig, axes = plt.subplots(num_row, num_col, squeeze=False, figsize=figsize)
    axes = dict(zip(param_names, axes.flat))

    # fig, ax = plt.subplots(nr_params, figsize=size)[1]
    for idx, plot_id in enumerate(param_names):

        ax = axes[plot_id]
        sns.set(style="ticks")
        ax = sns.kdeplot(params_fval[plot_id], bw='silver', ax=ax)
        ax.set_xlabel('log(' + param_names[idx] + ')', fontsize=fs)
        ax.set_ylabel('Density', fontsize=fs)
        sns.despine()

    if i_chain > 1:
        fig.suptitle('Temperature chain: ' + str(i_chain), fontsize=fs)
    fig.tight_layout()
    plt.show()

    return ax
