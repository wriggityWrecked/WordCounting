"""
Tools used for counting tweets (or any text really) and plotting word
freqeuencies using the python Counter.
"""

import collections
import re
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import parsing_arguments
import tweet_requester
from counter_stats import CounterStats
from utils import get_filename, save_pickle_counter_stats

STOP_WORDS_FILE = "word_files/stop_words.txt"
POSITIVE_WORDS_FILE = "word_files/positive_words.txt"
NEGATIVE_WORDS_FILE = "word_files/negative_words.txt"


def process_text(text, stop_words_list):
    """
    Count the words in the provided input text, but filtered given the
    input stop_words_list.
    """
    # strip out puncutation
    text = text.strip().lower()

    # didn't use translate punctuation as we want to keep hashtags and mentions
    text = re.sub('&.*?;', '', text)  # filter out html
    text = text.replace('\xe2\x80\x93', '')  # filter out unicode dash
    # todo there has to be a better way, need to read up....nltk tokenizer?

    # filter out punctuation
    text = re.sub(
        '[!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~]', '', text).decode('utf-8')

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


def plot_compound_sentinment(compound, negative, positive, neutral, plot_title):
    plt.style.use('ggplot')  # https://matplotlib.org/users/style_sheets.html

    plt.figure(figsize=(11, 7))
    plt.ylim(-1.05, 1.05)

    line1 = plt.plot(compound, color='#b5e7a0', linewidth=3)
    line2 = plt.plot(negative, color='#f7786b', linewidth=1.5)
    line3 = plt.plot(positive, color='#80ced6', linewidth=1.5)
    line4 = plt.plot(neutral, color='#f6cd61', linewidth=1.5)

    frame = plt.gca()
    frame.axes.tick_params(axis='both', which='both',
                           bottom=False, top=False, left=False)

    plt.subplots_adjust(top=0.75, bottom=0.35)

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
    labels, ax1_values = zip(*counter.most_common(number))
    indexes = np.arange(len(labels))

    axes1.barh(indexes, ax1_values, 0.82, align='center',
               color='#b5e7a0', edgecolor='black', linewidth=0.7)
    plt.yticks(indexes, labels, fontsize=10, snap=True, va='center')
    plt.xticks(np.arange(0, ax1_values[0] + 1, step=1))
    plt.tight_layout()

    # axes 2
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
    watermark_text = 'Generated by wriggitywrecked.github.io/WordCounting/'

    figure.text(0.65, 0.05, watermark_text,
                fontsize=19, color='gray', ha='center', va='bottom', alpha=0.6)

    to_save = plot_title + '_' + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + '.png'

    plt.savefig(to_save, edgecolor='b', pad_inches=0.2, dpi=250)

    return to_save


def generate_stats(handle, tweet_dictionary, stop_words_list,
                   positive_words_set, negative_words_set, save_data):
    """
    Given the input tweeter (twitter handle), tweet_dictionarY {timestamp:
    tweet_text}, stop words list, positive words set, and negative words set
    generate the total word count, positive word count, and negative word count.

    Return a named tuple (CounterStats) with the following names: count,
    positive_count, negative_count, number_of_tweets, avg_words_per_tweet,

    """

    counter = collections.Counter()

    average_words_per_tweet = 0
    average_time_between_tweets = 0
    last_timestamp = None

    # count words for each tweet
    for timestamp, tweet in tweet_dictionary.items():

        cnt = process_text(tweet, stop_words_list)

        # sum up all words in the tweet processed
        average_words_per_tweet += sum(cnt.values())

        # combine count
        counter += cnt

        if last_timestamp is None:
            last_timestamp = timestamp
        else:
            average_time_between_tweets += timestamp - last_timestamp
            last_timestamp = timestamp

    positive_counter, negative_counter = filter_positive_negative_words(counter,
                                                                        positive_words_set,
                                                                        negative_words_set)

    number_of_tweets = len(tweet_dictionary.keys())
    average_words_per_tweet = 1.0 * average_words_per_tweet / number_of_tweets
    average_time_between_tweets = average_time_between_tweets / number_of_tweets

    print 'Average time between tweets: ' + str(timedelta(seconds=average_time_between_tweets))

    # todo average time between tweets

    counter_value_sum = sum(counter.values())
    positive_word_percentage = 1.0 * \
                               sum(positive_counter.values()) / counter_value_sum * 100
    negative_word_percentage = 1.0 * \
                               sum(negative_counter.values()) / counter_value_sum * 100

    print('Number of tweets: ' + str(number_of_tweets))
    print('Average words per tweet: ' + str(format(average_words_per_tweet, '.1f')))
    print('% of positive words: ' + str(format(positive_word_percentage, '.1f')))
    print('% of negative words: ' + str(format(negative_word_percentage, '.1f')))

    cs = CounterStats(counter, positive_counter, negative_counter, number_of_tweets,
                      average_words_per_tweet, positive_word_percentage,
                      negative_word_percentage, average_time_between_tweets)
    if save_data:
        save_pickle_counter_stats(cs, handle + get_filename('_pickle', 'pkl'))

    return cs


def count_and_plot_accounts(twitter_handles, start_request_time, end_request_time, save_data):
    """
    Batch request, process, and generate stats for multiple twitter accounts over
    the same period of time (input).
    """

    stop_words = load_words_as_list(STOP_WORDS_FILE)
    p_set = load_words_as_frozenset(POSITIVE_WORDS_FILE)
    n_set = load_words_as_frozenset(NEGATIVE_WORDS_FILE)

    for handle in twitter_handles:

        # dictionary is ordered by key (timestamp) from oldest to newest
        tweet_dict = tweet_requester.search_twitter(
            handle, start_request_time, end_request_time, True)

        if len(tweet_dict) == 0:
            print 'No tweets found for handle ' + handle
            continue

        print 'handle @' + handle
        print 'Total number of tweets: ' + str(len(tweet_dict))
        data = generate_stats(handle, tweet_dict, stop_words, p_set, n_set, save_data)

        # convert unix time keys to strings
        tweet_dict_keys_list = list(tweet_dict.keys())

        start_date = datetime.fromtimestamp(
            tweet_dict_keys_list[0]).strftime('%Y-%m-%d %H:%M:%S UTC')
        end_date = datetime.fromtimestamp(tweet_dict_keys_list[len(
            tweet_dict_keys_list) - 1]).strftime('%Y-%m-%d %H:%M:%S UTC')

        # generate figure and save
        figure_file_name = subplot_all_counts(data.count, data.positive_count,
                                              data.negative_count, handle, 10,
                                              start_date, end_date)

    # todo return list of file names generated for each handle and the CounterStats data


if __name__ == "__main__":

    args = parsing_arguments.get_parsing_arguments()

    count_and_plot_accounts(args.twitter_accounts, args.start_date, args.end_date, args.save_data)

    # now post to jekyll blog
    #    with average words per tweet
    #    with percentage positive words
    #    with percentage negative words

    # todo pickle / save daily counts for analysis later
