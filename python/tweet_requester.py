"""
Methods to authenticate and obtain tweets using Twitter's search API.
"""

from collections import OrderedDict
import time
import base64
import requests
import calendar

import parsing_arguments
from utils import get_filename, save_json_data, make_directory


def obtain_bearer_token(token_from_file):
    """Get the bearer token using the Twitter oauth API.

    See https://developer.twitter.com/en/docs/basics/authentication/api-reference/token.html
    """
    with open(token_from_file) as opened_file:
        token = str(opened_file.read()).strip()

    encoded = base64.b64encode(token)
    key = encoded.decode('ascii')
    headers = {
        'Authorization': 'Basic ' + key,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    request = requests.post('https://api.twitter.com/oauth2/token',
                            headers=headers, data={'grant_type': 'client_credentials'})
    access_token = request.json()['access_token']
    return access_token


def search_twitter(handle, start_date, end_date, save_data):
    """
    Using the Twitter search API, return and save tweets from the input handle
    using the start_date and end_date as search parameters. Retweets are not
    requested as part of the search (excluded).

    If the save data flag is true then the output will be saved to a file.

    This function returns a dictionary of key (unix time) value (tweet text)
    dictionary.
    """

    header = {
        # todo global? command line arg parse?
        'Authorization': 'Bearer ' + obtain_bearer_token('token.txt')
    }

    # https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    # https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines

    data = {
        'q': 'from:' + handle + ' since:' + start_date + ' until:' + end_date + ' exclude:retweets',
        'tweet_mode': 'extended',
        'lang': 'en',
        'count': str(200)  # 100 is the documented max per the API
    }

    request = requests.get('https://api.twitter.com/1.1/search/tweets.json?',
                           headers=header, params=data)

    tweet_dict = {}

    for i in request.json()['statuses']:
        date = i['created_at'].encode('utf-8').replace("+0000", "")
        tweet_text = i['full_text'].encode('utf-8')

        # storing key as unix time (UTC - note calendar.timegm) in seconds
        # as it works well for sorting
        date_timestamp = calendar.timegm(time.strptime(date, "%a %b %d %H:%M:%S %Y"))

        # key timestamp, value tweet text
        tweet_dict[date_timestamp] = tweet_text

    otd = OrderedDict(sorted(tweet_dict.items()))

    if save_data:
        # create directory for handle if it doesn't exist
        path = 'data/' + handle  # should probably be global or allow configurable path
        make_directory(path)
        save_json_data(tweet_dict, get_filename(path + '/' + handle + '_tweets', 'json'))

    return otd


if __name__ == "__main__":

    args = parsing_arguments.get_parsing_arguments()

    for twitter_account in args.twitter_accounts:
        print twitter_account
        print search_twitter(twitter_account, args.start_date, args.end_date, args.save_data)
