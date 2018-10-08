import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np


def plot_cormat(plot_file, cor_mat, list_labels=[], label_size=2,
                cmap='rainbow'):
    """plot correlation matrix"""

    fig1 = plt.figure()
    ax = fig1.add_subplot(1, 1, 1)
    im = ax.matshow(cor_mat, interpolation="none")
    [i.set_visible(False) for i in ax.spines.values()]
    im.set_cmap(cmap)

    # add labels
    if len(list_labels):
        assert len(list_labels) == cor_mat.shape[0], "Error number of labels \
            {} and matrix shape {}".format(len(list_labels), cor_mat.shape[0])

        plt.xticks(list(range(len(list_labels))), list_labels,
                   rotation='vertical', fontsize=label_size)
        plt.yticks(list(range(len(list_labels))), list_labels,
                   fontsize=label_size)
        plt.subplots_adjust(top=0.8)

    # ticks
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    left=False, right=False)
    # colorbar
    fig1.colorbar(im)
    fig1.savefig(plot_file)
    plt.close(fig1)
    del fig1


def plot_ranged_cormat(plot_file, cor_mat, list_labels=[],
                       fix_full_range=[-1.0, 1.0], label_size=2,
                       cmap='spectral'):
    """plot ranged correlation matrix"""
    fig1 = plt.figure(frameon=False)
    ax = fig1.add_subplot(1, 1, 1)
    im = ax.matshow(cor_mat, vmin=fix_full_range[0], vmax=fix_full_range[1],
                    interpolation="none")

    [i.set_visible(False) for i in ax.spines.values()]
    im.set_cmap(cmap)

    nb_labels = len(list_labels)

    # add labels
    if nb_labels:

        assert nb_labels == cor_mat.shape[0], ("Error number of labels \
            {} and matrix shape {}".format(nb_labels, cor_mat.shape[0]))

        plt.xticks(list(range(nb_labels)), list_labels,
                   rotation='vertical', fontsize=label_size)
        plt.yticks(list(range(nb_labels)), list_labels, fontsize=label_size)

        plt.subplots_adjust(top=0.8)

    # ticks
    plt.tick_params(axis='both',  which='both',  bottom='off', top='off',
                    left='off', right='off')

    # colorbasr
    fig1.colorbar(im)
    fig1.savefig(plot_file)
    plt.close(fig1)
    del fig1


def plot_int_mat(plot_file, cor_mat, list_labels=[], fix_full_range=[-4, 4],
                 label_size=2, cmap='jet'):

    fig1 = plt.figure(frameon=False)
    ax = fig1.add_subplot(1, 1, 1)

    cmap = plt.get_cmap(cmap, len(
        np.unique(np.arange(fix_full_range[0], fix_full_range[1]+1))))

    im = ax.matshow(cor_mat, vmin=fix_full_range[0], vmax=fix_full_range[1],
                    interpolation="none", cmap=cmap)

    [i.set_visible(False) for i in ax.spines.values()]

    # add labels
    if len(list_labels):
        assert len(list_labels) == cor_mat.shape[0], ("Error number of labels\
            {} and matrix shape {}".format(len(list_labels), cor_mat.shape[0]))

        plt.xticks(list(range(len(list_labels))), list_labels,
                   rotation='vertical', fontsize=label_size)
        plt.yticks(list(range(len(list_labels))),
                   list_labels, fontsize=label_size)

        plt.subplots_adjust(top=0.8)

    # ticks
    plt.tick_params(axis='both',  which='both', bottom='off', top='off',
                    left='off', right='off')
    # colorbar
    fig1.colorbar(im, ticks=list(range(-4, 5)))
    fig1.savefig(plot_file)
    plt.close(fig1)
    del fig1


def plot_hist(plot_hist_file, data, nb_bins=100):
    """ plot histogramms """
    fig2 = plt.figure()
    ax = fig2.add_subplot(1, 1, 1)
    y, x = np.histogram(data, bins=nb_bins)
    ax.plot(x[:-1], y)
    fig2.savefig(plot_hist_file)
    plt.close(fig2)
    del fig2


def plot_colorbar(plot_colorbar_file, colors):
    """plot colorbar"""
    fig2 = plt.figure(figsize=(8, 3))
    ax2 = fig2.add_axes([0.05, 0.475, 0.9, 0.15])

    cmap = mpl.colors.ListedColormap(colors)

    cmap.set_over('0.25')
    cmap.set_under('0.75')

    bounds = list(range(len(colors)))

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    print(bounds)

    print(norm)

    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm,
                                    boundaries=bounds, spacing='proportional',
                                    orientation='horizontal')

    cb2.set_label('Discrete intervals, some other units')

    fig2.savefig(plot_colorbar_file)
    plt.close(fig2)
    del fig2


def plot_signals(plot_signals_file, signals_matrix, colors=[],
                 ylim=[], labels=[], add_zero_line=False):
    """ plot signals"""
    fig2 = plt.figure()
    ax = fig2.add_subplot(1, 1, 1)

    if len(ylim):
        ax.set_ylim(ylim[0], ylim[1])

    if len(signals_matrix.shape) == 1:
        ax.plot(list(range(signals_matrix.shape[0])), signals_matrix[:])

    else:
        nb_signals = signals_matrix.shape[0]
        nb_timings = signals_matrix.shape[1]

        for i in range(nb_signals):

            if len(colors) == nb_signals:

                if len(labels) == 0 or len(labels) != len(colors):
                    ax.plot(list(range(nb_timings)), signals_matrix[i, :],
                            colors[i])
                else:
                    ax.plot(list(range(nb_timings)), signals_matrix[i, :],
                            colors[i], label=labels[i])

            elif len(colors) == 1:
                ax.plot(list(range(nb_timings)), signals_matrix[i, :],
                        colors[0])

            else:
                if len(labels) == nb_signals:
                    ax.plot(list(range(nb_timings)), signals_matrix[i, :],
                            label=labels[i])
                else:
                    ax.plot(list(range(nb_timings)),
                            signals_matrix[i, :])

    if add_zero_line:
        ax.plot(list(range(nb_timings)), [
                0.0]*nb_timings, color='black', linestyle='--')

    if nb_signals == len(labels):
        ax.legend(loc=0, prop={'size': 8})

    fig2.savefig(plot_signals_file)

    plt.close(fig2)
    del fig2


def plot_sep_signals(plot_signals_file, signals_matrix, colors=[],
                     range_signal=-1):

    fig2 = plt.figure()
    ax = fig2.add_subplot(1, 1, 1)

    if range_signal == -1:
        range_signal = np.amax(signals_matrix) - np.amin(signals_matrix)

    if len(colors) == signals_matrix.shape[0]:

        for i in range(signals_matrix.shape[0]):
            print(range_signal*i)
            ax.plot(signals_matrix[i, :] + range_signal*i, colors[i])

    else:

        for i in range(signals_matrix.shape[0]):
            ax.plot(signals_matrix[i, :] + range_signal*i)

    x1, x2, y1, y2 = ax.axis()
    ax.axis((x1, x2, -2.0, y2))

    fig2.savefig(plot_signals_file)
    plt.close(fig2)
    del fig2
