"""
Module for the CounterStats named tuple.
"""

import collections

CounterStats = collections.namedtuple("CounterStats", ["count", "positive_count",
                                                       "negative_count", "number_of_tweets",
                                                       "avg_words_per_tweet",
                                                       "positive_word_percentage",
                                                       "negative_word_percentage",
                                                       "average_time_between_tweets"])
