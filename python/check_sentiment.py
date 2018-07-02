"""

"""
import collections
from datetime import datetime, timedelta
import nltk
import numpy
import pytz
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import counting
import parsing_arguments
import tweet_requester
from stock_prices import get_stock_price

nltk.download('vader_lexicon')


def analyze_text(input_text):
    """

    :param input_text:
    :return:
    """

    sid = SentimentIntensityAnalyzer()
    # print(input_text)
    scores = sid.polarity_scores(input_text)
    print scores
    return scores


def average_sentiment_per_day(tweet_dict, hour_offset=None):
    """

    :param hour_offset:
    :param tweet_dict:
    :return:
    """
    dict = collections.defaultdict(list)
    last_time = None
    for tweet_time, tweet_text in tweet_dict.items():

        # round off time to day
        time = datetime.fromtimestamp(tweet_time, pytz.utc) #todo NEED INPUT TIMEZONE, e.g. eastern for trump
        dt1 = datetime(time.year, time.month, time.day, 0, 0)
        analyzed = analyze_text(tweet_text)
        dict[dt1].append(analyzed['compound'])

        # insert nothing (zero) for missing days simply for display
        # TODO think about leaving missing days blank
        if last_time is not None:
            delta = dt1 - last_time
            if delta > timedelta(days=1):
                missing = dt1 - timedelta(days=1)
                dict[missing] = [0]

        last_time = dt1

    # done organizing data, time to average
    for time, data in dict.items():
        dict[time] = numpy.mean(data)
        dt2 = time + timedelta(hours=23) + timedelta(minutes=59) + timedelta(seconds=59)
        dict[dt2] = dict[time]

    return dict


def plot_sentiment_and_stock():
    args = parsing_arguments.get_parsing_arguments()

    for twitter_account in args.twitter_accounts:
        tweet_dict = tweet_requester.search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)

        data = average_sentiment_per_day(tweet_dict)
        dates = sorted(data.keys())
        values = [data[k] for k in dates]

        closing_stock = get_stock_price('TSLA', args.start_date, args.end_date)
        sorted_keys = sorted(closing_stock.keys())
        stock_dates = [k[1] for k in sorted_keys]
        stock_values = [closing_stock[k] for k in sorted_keys]

        counting.plot_compound_sentiment(dates, values, 'test', stock_dates, stock_values)


def plot_sentiment_and_average():
    args = parsing_arguments.get_parsing_arguments()

    for twitter_account in args.twitter_accounts:

        tweet_dict = tweet_requester.search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)

        s_k = sorted(tweet_dict.keys())
        dates = [datetime.fromtimestamp(tweet_time, pytz.utc) for tweet_time in s_k]
        values = [tweet_dict[k] for k in s_k]
        sentinment = []
        for v in values:
            sentinment.append(analyze_text(v)['compound'])

        average_date = average_sentiment_per_day(tweet_dict)
        a_dates = sorted(average_date.keys())
        a_values = [average_date[k] for k in a_dates]

        counting.plot_compound_sentiment(dates, sentinment, a_dates, a_values)

def plot_sentiment_and_moving_average():
    args = parsing_arguments.get_parsing_arguments()

    for twitter_account in args.twitter_accounts:

        tweet_dict = tweet_requester.search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)

        s_k = sorted(tweet_dict.keys())
        dates = [datetime.fromtimestamp(tweet_time, pytz.utc) for tweet_time in s_k]
        values = [tweet_dict[k] for k in s_k]
        sentinment = []
        for v in values:
            sentinment.append(analyze_text(v)['compound'])
        # two loops :-(
        a_values = []
        sl = len(sentinment)
        window = 15
        for i in xrange(0, sl):
            avg = 0
            # 5 is the window
            for j in xrange(0, window):
                index = i-j
                if sl > index >= 0:
                    avg += sentinment[index]
            avg = avg * 1.0 / window
            a_values.append(avg)

        counting.plot_compound_sentiment(dates, sentinment, dates, a_values)




def plot_sentiment():
    args = parsing_arguments.get_parsing_arguments()

    for twitter_account in args.twitter_accounts:

        tweet_dict = tweet_requester.search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)

        dates = [datetime.fromtimestamp(tweet_time, pytz.utc) for tweet_time in sorted(tweet_dict.keys())]
        values = [tweet_dict[k] for k in sorted(tweet_dict.keys())]
        sentinment = []
        for v in values:
            sentinment.append(analyze_text(v)['compound'])

        counting.plot_compound_sentiment(dates, sentinment)


if __name__ == "__main__":
    plot_sentiment_and_moving_average()
