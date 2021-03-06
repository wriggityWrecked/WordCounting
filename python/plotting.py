from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from utils import make_directory


def plot_compound_sentiment(dates, compound, ancillary_data_dates=None, ancillary_data_values=None):
    """

    :param dates:
    :param compound:
    :param ancillary_data_dates:
    :param ancillary_data_values:
    :return:
    """
    plt.style.use('ggplot')  # https://matplotlib.org/users/style_sheets.html

    plt.figure(figsize=(12, 7))
    plt.ylim(-1.05, 1.05)

    ax1 = plt.gca()
    ax1.plot(dates, compound, color='#80ced6', markeredgecolor='black', markeredgewidth=0.15, marker='o',
             linestyle='None')
    # ax1.set_yticks(np.linspace(-1.0, 1.0, 5))
    ax1.axes.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)

    if ancillary_data_dates is not None and ancillary_data_values is not None:
        # ax2 = ax1.axes.twinx()
        # ax2 = ax1.axes.twiny()
        ax1.plot(ancillary_data_dates, ancillary_data_values, color='#7bce82', linewidth=1.5)
        # ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())))
        ax1.axes.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)

    plt.subplots_adjust(top=0.75, bottom=0.35, left=0.075, right=0.975)
    plt.xticks(rotation=45)
    # plt.tight_layout()

    plt.show()


def subplot_all_counts(counter, positive_count, negative_count, plot_title,
                       number, start_date, end_date):
    """
    Generate a subplot of the top number words, top number positive, and top
    number negative for the given counter inputs.

    Return the name of the plot (filename) saved to disk.
    """
    # style to look good
    plt.style.use('ggplot')  # https://matplotlib.org/users/style_sheets.html

    figure, (axes1, axes2, axes3) = plt.subplots(ncols=1, nrows=3, sharex=True,
                                                 squeeze=True, figsize=(11, 7.5))

    # main title
    plt.suptitle('@' + plot_title + ' : ' + start_date +
                 ' -- ' + end_date + '\n', fontsize=12)

    # top # sub plot
    axes1.set_title('Top ' + str(number) + ' Word Count', fontsize=11)
    axes1.set_autoscale_on(True)
    axes1.invert_yaxis()
    axes1.tick_params(axis='both', which='both',
                      bottom=False, top=False, left=False)

    # top # positive subplot
    axes2.set_title('Top ' + str(number) + ' Positive Words', fontsize=11)
    axes2.set_autoscale_on(True)
    axes2.invert_yaxis()
    axes2.tick_params(axis='both', which='both',
                      bottom=False, top=False, left=False)

    # top # negative subplot
    axes3.set_title('Top ' + str(number) + ' Negative Words', fontsize=11)
    axes3.set_autoscale_on(True)
    axes3.invert_yaxis()
    axes3.tick_params(axis='both', which='both', bottom=False, left=False)

    # set current
    plt.sca(axes1)

    # axes 1
    # TODO CHECK IF MOST COMMON IS ZERO
    labels, ax1_values = zip(*counter.most_common(number))
    indexes = np.arange(len(labels))

    axes1.barh(indexes, ax1_values, 0.82, align='center',
               color='#b5e7a0', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=10, snap=True, va='center')
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()

    # axes 2
    # TODO CHECK IF MOST COMMON IS ZERO

    labels, values = zip(*positive_count.most_common(number))
    indexes = np.arange(len(labels))
    plt.sca(axes2)

    axes2.barh(indexes, values, 0.82, align='center',
               color='#80ced6', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=10, snap=True)
    # same scale as total count
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()

    # axes 3
    # TODO CHECK IF MOST COMMON IS ZERO

    labels, values = zip(*negative_count.most_common(number))
    indexes = np.arange(len(labels))
    plt.sca(axes3)

    axes3.barh(indexes, values, 0.82, align='center',
               color='#f7786b', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=10, snap=True)
    # same scale as total count
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1), fontsize=12)
    plt.tight_layout()

    # add space for top title
    plt.subplots_adjust(top=0.915)

    # watermark
    watermark_text = 'Generated by theLostWizard'
    # watermark_text = 'Generated by wriggitywrecked.github.io/WordCounting/'

    figure.text(0.65, 0.05, watermark_text,
                fontsize=19, color='gray', ha='center', va='bottom', alpha=0.6)

    make_directory('images')
    to_save = 'images/' + plot_title + '_' + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + '.png'

    plt.savefig(to_save, edgecolor='b', pad_inches=0.2, dpi=250)

    return to_save
