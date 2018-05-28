"""
Tools used for counting tweets (or any text really) and plotting word
freqeuencies using the python Counter.
"""

import collections
import string
import sys
import copy
import datetime
import numpy as np
import matplotlib.pyplot as plt
import tweet_requester

STOP_WORDS_FILE = "word_files/stop_words.txt"
POSITIVE_WORDS_FILE = "word_files/positive_words.txt"
NEGATIVE_WORDS_FILE = "word_files/negative_words.txt"


def process_text(text, stop_words_list):
    """
    Count the words in the provided input text, but filtered given the
    input stop_words_list.
    """
    # strip out puncutation
    text = text.strip().decode('utf-8')
    text.translate(string.punctuation)

    # lowercase
    text = text.lower()

    count = collections.Counter(text.split())  # split on spaces

    # remove stop words
    count = prune_stop_words(count, stop_words_list)

    return count


def prune_stop_words(counter, stop_words_list):
    """
    Filter the input counter with the input stop_words_list and return the
    result.
    """
    # todo add '&' to stop words and filter out
    # todo check if need to filter other non alpha numeric

    for word in stop_words_list:
        if word in counter:
            del counter[word]

    return counter


def filter_positive_negative_words(counter, positive_set, negative_set):
    """
    Filter words provided in a counter by positive a negative (as set inputs)
    and return counters of both positive occurances and negative occurances.
    """

    negative = {}
    positive = {}
    for word, count in counter.items():
        if word in positive_set:
            positive[word] = count
        elif word in negative_set:
            negative[word] = count
    return collections.Counter(positive), collections.Counter(negative)


def load_words_as_list(file_name):
    """
    Load line delimited words from a file and return as a list.
    """

    tmp_list = []
    opened_file = open(file_name, "r")
    for line in opened_file:
        tmp_list.append(line.rstrip())
    opened_file.close()
    return tmp_list


def load_words_as_frozenset(file_name):
    """
    Load line delimitedwords from a file and return as a frozenset.
    """

    opened_file = open(file_name, "r")
    tmp_list = []
    for line in opened_file:
        tmp_list.append(line.rstrip())
    opened_file.close()
    return frozenset(tmp_list)


def barplot_count(counter, plot_title, color):
    """
    Generate a barplot using the input counter, input plot_title, and input
    bar color.
    """
    #neat unpacking trick
    #https://docs.python.org/3.3/library/functions.html#zip
    labels, values = zip(*counter.most_common(10))

    plt.rcdefaults()
    figure, axes = plt.subplots()

    axes.set_title(plot_title)
    axes.set_autoscale_on(True)
    axes.invert_yaxis()

    indexes = np.arange(len(labels))

    axes.barh(indexes, values, 0.5, align='center', color=color)

    plt.yticks(indexes, labels)
    plt.xticks(np.arange(0, values[0] + 1, step=1))
    plt.tight_layout()
    # plt.show()

    return figure

def subplot_all_counts(counter, positive_count, negative_count, plot_title, number, start_date, end_date):
    """
    Generate a subplot of the top number words, top number positive, and top
    number negative for the given counter inputs. Return the name of the file
    (plots) saved.
    """

    _, (axes1, axes2, axes3) = plt.subplots(ncols=1, nrows=3, sharex=True)

    plt.suptitle(start_date + ' -- ' + end_date, fontsize=12)

    axes1.set_title(plot_title + ' ' + 'Top ' + str(number) + ' Word Count', fontsize=10)
    axes1.grid(linestyle='dashed', linewidth=0.5, axis='x')
    axes1.set_autoscale_on(True)
    axes1.invert_yaxis()

    axes2.set_title(plot_title + ' ' + 'Top ' + str(number) + ' Positive Words', fontsize=10)
    axes2.grid(linestyle='dashed', linewidth=0.5, axis='x')
    axes2.set_autoscale_on(True)
    axes2.invert_yaxis()

    axes3.set_title(plot_title + ' ' + 'Top ' + str(number) + ' Negative Words', fontsize=10)
    axes3.grid(linestyle='dashed', linewidth=0.5, axis='x')
    axes3.set_autoscale_on(True)
    axes3.invert_yaxis()

    plt.sca(axes1)

    #axes 1
    labels, ax1_values = zip(*counter.most_common(number))
    indexes = np.arange(len(labels))

    axes1.barh(indexes, ax1_values, 0.82, align='center', color='g', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=7, snap=True, va='center')
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()

    #axes 2
    labels, values = zip(*positive_count.most_common(number))
    indexes = np.arange(len(labels))
    plt.sca(axes2)

    axes2.barh(indexes, values, 0.82, align='center', color='b', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=7, snap=True)
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()

    #axes 3
    labels, values = zip(*negative_count.most_common(number))
    indexes = np.arange(len(labels))
    plt.sca(axes3)

    axes3.barh(indexes, values, 0.82, align='center', color='r', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=7, snap=True)
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()
    
    now_string = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    plt.subplots_adjust(left=0.175, top=0.875)

    to_save = plot_title + '_' + now_string + '.png'
    plt.savefig(to_save, edgecolor='b', pad_inches=0.2, dpi=250)

    return to_save

def generate_stats_and_plots(tweeter, tweet_dictionary, stop_words_list,
                             positive_words_set, negative_words_set):

    #reload(sys)
    #sys.setdefaultencoding('utf8')

    tweet_list = tweet_dict.values()

    counter = collections.Counter()
    positive_counter = collections.Counter()
    negative_counter = collections.Counter()

    average_words_per_tweet = 0

    # count words for each tweet
    for tweet in tweet_list:

        cnt = process_text(tweet, stop_words_list)

        #could do this at the end since we aren't looking at averages per tweet
        p_count, n_count = filter_positive_negative_words(cnt,
        	                                                 positive_words_set,
        	                                                 negative_words_set)

        average_words_per_tweet += sum(cnt.values())

        # combine counts
        counter += cnt
        positive_counter += p_count
        negative_counter += n_count

    tweet_list_length = len(tweet_list)
    average_words_per_tweet = average_words_per_tweet / tweet_list_length

    counter_value_sum = sum(counter.values())
    positive_word_percentage = 1.0 * \
        sum(positive_counter.values()) / counter_value_sum * 100
    negative_word_percentage = 1.0 * \
        sum(negative_counter.values()) / counter_value_sum * 100

    # convert unix time keys to strings
    tweet_dict_keys_list = list(tweet_dict.keys())
    start_date = datetime.datetime.fromtimestamp(
        tweet_dict_keys_list[0]).strftime('%Y-%m-%d %H:%M:%S UTC')
    end_date = datetime.datetime.fromtimestamp(tweet_dict_keys_list[len(
        tweet_dict_keys_list) - 1]).strftime('%Y-%m-%d %H:%M:%S UTC')

    # generate figure and save
    figure_file_name = subplot_all_counts(counter, positive_counter,
                                          negative_counter, handle, 10, 
                                          start_date, end_date)


    #print file_names


    # plot positive / negative word percentage against polling numbers

    # now post to jekyll blog
    #    with average words per tweet
    #    with percentage positive words
    #    with percentage negative words

    # todo pickle / save daily counts for analysis later


if __name__ == "__main__":

	#todo command line arguments via argparse?
    handles = []
    #handles.append('SenSanders')
    handles.append('realDonaldTrump')
    #handles.append('LindseyGrahamSC')
    #handles.append('NancyPelosi')
    #handles.append('SenateMajLdr')
    #handles.append('VP')
    #handles.append('SenJohnMcCain')
    #handles.append('RandPaul')
    #handles.append('SenWarren')

    stop_words = load_words_as_list(STOP_WORDS_FILE)
    p_set = load_words_as_frozenset(POSITIVE_WORDS_FILE)
    n_set = load_words_as_frozenset(NEGATIVE_WORDS_FILE)

    #todo configurable start date and end date

    for handle in handles:
        tweet_dict = tweet_requester.search_twitter(
            handle, '2018-05-27', '2018-05-29')
        generate_stats_and_plots(handle, tweet_dict, stop_words, p_set, n_set)
