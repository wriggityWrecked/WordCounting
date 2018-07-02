import collections
import string
import time
from random import randint

import numpy

import parsing_arguments
import tweet_requester


def construct_markov_chain(tweet_dict, input_dict=None):
    """

    :param tweet_dict:
    :param input_dict:
    :return:
    """
    if input_dict is None:
        input_dict = collections.defaultdict(list)

    for text in tweet_dict.values():  # each tweet in the dictionary
        split_words = text.split()
        length = len(split_words)
        for i in xrange(1, length):  # each word in the tweet
            input_dict[split_words[i-1]].append(split_words[i])

    return input_dict


# todo save chain

# todo update chain

if __name__ == "__main__":

    args = parsing_arguments.get_parsing_arguments()
    input_dict = None
    for twitter_account in args.twitter_accounts:
        tweet_dict = tweet_requester.search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)
        input_dict = construct_markov_chain(tweet_dict, input_dict)

    # check if we reached a dead end
    list_of_words = []
    total_length = len(input_dict.keys())
    while len(list_of_words) <= 0:
        start_index = randint(0, total_length)
        list_of_words = input_dict[(input_dict.keys())[start_index]]

    sentence = [numpy.random.choice(list_of_words)]

    count = 0
    word_soft_limit = 50
    max_limit = 255
    not_finished = True
    while not_finished:
        list_of_words = input_dict[sentence[-1]]  # get the list of words for the last word
        while len(list_of_words) <= 0:
            start_index = randint(0, len(input_dict.keys()) - 1)
            list_of_words = input_dict[input_dict.keys()[start_index]]

        sentence.append(numpy.random.choice(list_of_words))
        count += 1
        if count > word_soft_limit:
            for c in sentence[-1]:
                if c in '!.?' or count >= max_limit:
                    not_finished = False  # break out of while
                    break

    print ' '.join(sentence)

    print input_dict['Trump']
