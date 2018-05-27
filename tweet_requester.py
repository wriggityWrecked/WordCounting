import base64
import requests
import urllib
import string
import json
import time
from datetime import datetime
from collections import OrderedDict
#Request URL: https://twitter.com/i/profiles/show/realDonaldTrump/timeline/tweets?composed_count=0&include_available_features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count=0&min_position=996487798759854082
#https://twitter.com/i/profiles/show/realDonaldTrump/timeline/tweets?include_available_features=1&include_entities=1&max_position=981126375716409344&reset_error_state=false


def obtain_bearer_token(token_from_file):

	with open(token_from_file) as f:  
		token = str(f.read()).strip()

	encoded = base64.b64encode(token)
	key = encoded.decode('ascii')
	headers = {
		'Authorization': 'Basic ' + key, 
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}

	r = requests.post('https://api.twitter.com/oauth2/token', headers=headers, data={'grant_type':'client_credentials'})
	access_token = r.json()['access_token']
	return access_token


def search_twitter(handle, start_date, end_date):
	#todo args: user handle, start date, end date
	#https://twitter.com/search?l=&q=from%3ArealDonaldTrump%20since%3A2018-05-14%20until%3A2018-05-15

	##https://blog.scrapinghub.com/2016/06/22/scrapy-tips-from-the-pros-june-2016/?utm_content=buffer84a4c&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer
	header = {
	    'Authorization': 'Bearer ' + obtain_bearer_token('token.txt') #todo global? command line arg parse?
	}

	data = {
	    'q': 'from:' + handle + ' since:' + start_date + ' until:' + end_date,
	    'tweet_mode': 'extended'
	}

	r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=header, params=data)

	tweet_dict = {}
	for i in r.json()['statuses']:
		#discard retweets
		if not 'RT' == i['full_text'][:2]:

			date = i['created_at'].encode('utf-8').replace("+0000", "")
			tweet_text = i['full_text'].encode('utf-8')
			#storing key as unix time works well for sorting
			date_timestamp = time.mktime(time.strptime(date, "%a %b %d %H:%M:%S %Y"))
			tweet_dict[date_timestamp] = tweet_text

	otd = OrderedDict(sorted(tweet_dict.items()))
	print otd

	now = datetime.now()
	now_string = now.strftime("%Y-%m-%dT%H:%M:%S")

	with open('data_' + now_string + '.json', 'w') as fp:
		json.dump(tweet_dict, fp)

	return otd

if __name__ == "__main__":
	search_twitter('realDonaldTrump', '2018-05-23', '2018-05-26')
