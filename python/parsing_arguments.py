"""
Standalone methods to call counting_plotting_tools functions from the command
line.
"""

import argparse
import collections
from datetime import datetime, timedelta

# handles.append('JustinTrudeau')
# handles.append('LindseyGrahamSC')
# handles.append('NancyPelosi')
# handles.append('SenateMajLdr')
# handles.append('VP')
# handles.append('SenJohnMcCain')
# handles.append('SenWarren')
# handles.append('BarackObama')
# handles.append('HillaryClinton')
# handles.append('elonmusk')
# handles.append('SenFeinstein')

ParsingArguments = collections.namedtuple("ParsingArguments", ['twitter_accounts', 'start_date', 'end_date', 'save_data'])


def get_parsing_arguments():
    """
    Helpful function to specify arguments for twitter accounts, start time, and
    end time to request twitter data, count words, and plot tweet data.
    :return: ParsingArguments named tuple
    """

    # get time in a 'nice' format for the twitter request
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    last_week = (now - timedelta(days=8)).strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(description='Requests tweets from \
                                        specified accounts and analyze text for \
                                     plots and stats.')

    parser.add_argument('twitter_accounts', metavar='Twitter Account(s)', nargs='*',
                         help='Twitter account(s) to process')

    parser.add_argument('--start_date', metavar='Request Starting Date of the \
                           form %Y-%m-%d. If not specified then default is last \
                           week ' + str(last_week), default=last_week, help='')

    parser.add_argument('--end_date', metavar='Request Ending Date of the \
                           form %Y-%m-%d. If not specified then default is \
                           tomorrow ' + str(tomorrow), default=tomorrow, help='')

    parser.add_argument('-s', '--save_data', action='store_true')

    twitter_accounts = parser.parse_args().twitter_accounts
    start_date = parser.parse_args().start_date
    end_date = parser.parse_args().end_date
    save_data = parser.parse_args().save_data

    print twitter_accounts
    print start_date
    print end_date
    print save_data

    return ParsingArguments(twitter_accounts, start_date, end_date, save_data)
