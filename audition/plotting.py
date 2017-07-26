import matplotlib
import numpy as np
import matplotlib.lines as mlines

matplotlib.use('Agg')
from matplotlib import pyplot as plt


def category_colordict(cmap_name, categories):
    # want to step through the discrete color map rather than sampling
    # across the entire range, so create an even spacing from 0 to 1
    # with as many steps as in the color map (cmap.N), then repeat it
    # enough times to ensure we cover all our categories
    cmap = plt.get_cmap(cmap_name)
    ncyc = int(np.ceil(1.0*len(categories) / cmap.N))
    colors = (cmap.colors * ncyc)[:len(categories)]
    return dict(zip(categories, colors))


def _plot_lines(frame, x_col, y_col, ax, grp_col, colordict, cat_col):
    # plot the lines, one for each model group,
    # looking up the color by model type from above
    for grp_val in np.unique(frame[grp_col]):
        df = frame.loc[frame[grp_col] == grp_val]
        color = colordict[df.iloc[0][cat_col]]
        df.plot(x_col, y_col, ax=ax, c=color, legend=False)


def generate_plot_lines(colordict, label_fcn):
    plot_lines = []
    # plot_labs = []
    for cat_val in sorted(colordict.keys()):
        # http://matplotlib.org/users/legend_guide.html
        lin = mlines.Line2D(
            xdata=[],
            ydata=[],
            color=colordict[cat_val],
            label=label_fcn(cat_val)
        )
        plot_lines.append(lin)
        # plot_labs.append(mt)
    return plot_lines


def _config_axes(
    ax,
    x_ticks,
    y_ticks,
    title,
    title_fontsize,
    x_label,
    y_label,
    label_fontsize
):
    if x_ticks is not None:
        ax.set_xticks(x_ticks)
    if y_ticks is not None:
        ax.set_yticks(y_ticks)
    ax.set_ylim([0, 1.1])
    ax.set_title(title, fontsize=title_fontsize)
    ax.set_ylabel(y_label, fontsize=label_fontsize)
    ax.set_xlabel(x_label, fontsize=label_fontsize)


def plot_cats(frame, x_col, y_col, cat_col='model_type', grp_col='model_group_id',
              title='', x_label='', y_label='', cmap_name='Vega10',
              figsize=[12, 6], x_ticks=None, y_ticks=None,
              legend_loc=None, legend_fontsize=12,
              label_fontsize=12, title_fontsize=16,
              label_fcn=None):
    """Plot a line plot with each line colored by a category variable.

    Arguments:
        frame (DataFrame) -- a dataframe containing the data to be plotted
        x_col (string) -- name of the x-axis column
        y_col (string) -- name of the y-axis column
        cat_col (string) -- name of the catagory column to color lines
        grp_col (string) -- column that identifies each group of
                            (x_col, y_col) points for each line
        title (string) -- allows specifying a custom title for the graph
        x_label (string) -- allows specifying a custom label for the x-axis
        y_label (string) -- allows specifying a custom label for the y-axis
        cmap_name (string) -- matplotlib color map name to use for plot
        figsize (tuple) -- figure size to pass to matplotlib
        x_ticks (sequence) -- optional ticks to use for x-axis
        y_ticks (sequence) -- optional ticks to use for y-axis
        legend_loc (string) -- allows specifying location of plot legend
        legend_fontsize (int) -- allows specifying font size for legend
        label_fontsize (int) -- allows specifying font size for axis labels
        title_fontsize (int) -- allows specifying font size for plot title
        label_fcn (method) -- function to map category names to more readable
                                names, accepting values of cat_col
    """

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # function for parsing cat_col values into more readable legend lables
    if label_fcn is None and cat_col == 'model_type':
        label_fcn = lambda x: x.split('.')[-1]
    elif label_fcn is None:
        label_fcn = lambda x: x

    categories = np.unique(frame[cat_col])

    colordict = category_colordict(cmap_name, categories)

    # plot the lines, one for each model group,
    # looking up the color by model type from above
    _plot_lines(frame, x_col, y_col, ax, grp_col, colordict, cat_col)

    # have to set the legend manually since we don't want one legend
    # entry per line on the plot, just one per model type.

    # I had to upgrade matplotlib to get handles working, otherwise
    # had to call like this with plot_labs as a separate list
    # plt.legend(plot_patches, plot_labs, loc=4, fontsize=10)
    plot_lines = generate_plot_lines(colordict, label_fcn)

    plt.legend(handles=plot_lines, loc=legend_loc, fontsize=legend_fontsize)

    _config_axes(
        ax=ax,
        x_ticks=x_ticks,
        y_ticks=y_ticks,
        title=title,
        title_fontsize=title_fontsize,
        x_label=x_label,
        y_label=y_label,
        label_fontsize=label_fontsize,
    )

    plt.show()
