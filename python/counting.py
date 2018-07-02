"""
Tools used for counting tweets (or any text really) and plotting word
freqeuencies using the python Counter.
"""

import collections
import re
from datetime import datetime, timedelta
import pytz

import parsing_arguments
import tweet_requester
from counter_stats import CounterStats
from plotting import subplot_all_counts
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
    text = re.sub('[!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~]', '', text).decode('utf-8')

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
    and return counters of both positive occurrences and negative occurrences.
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
    Load line delimited words from a file and return as a frozenset.
    """

    opened_file = open(file_name, "r")
    tmp_list = []
    for line in opened_file:
        tmp_list.append(line.rstrip())
    opened_file.close()
    return frozenset(tmp_list)


def generate_stats(handle, tweet_dictionary, stop_words_list,
                   positive_words_set, negative_words_set, save_data):
    """
    Given the input tweeter (twitter handle), tweet_dictionary {timestamp:
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

    stats = CounterStats(counter, positive_counter, negative_counter, number_of_tweets,
                      average_words_per_tweet, positive_word_percentage,
                      negative_word_percentage, average_time_between_tweets)
    if save_data:
        save_pickle_counter_stats(stats, handle + get_filename('_pickle', 'pkl'))

    return stats


def count_and_plot_accounts(twitter_handles, start_request_time, end_request_time, save_data):
    """
    Batch request, process, and generate stats for multiple twitter accounts over
    the same period of time (input).
    """

    stop_words = load_words_as_list(STOP_WORDS_FILE)
    p_set = load_words_as_frozenset(POSITIVE_WORDS_FILE)
    n_set = load_words_as_frozenset(NEGATIVE_WORDS_FILE)
    generated_plots = []

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
            tweet_dict_keys_list[0], tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        end_date = datetime.fromtimestamp(tweet_dict_keys_list[len(
            tweet_dict_keys_list) - 1], tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

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
