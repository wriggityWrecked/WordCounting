# coding: utf-8
# encoding: utf-8

#https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
#https://twitter.com/search?l=&q=from%3ArealDonaldTrump%20since%3A2018-05-14%20until%3A2018-05-15&src=typd
#https://twitter.com/search?l=&q=from%3ASenSanders%20since%3A2018-05-11%20until%3A2018-05-15&src=typd
#https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets

import collections
import string
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sys
import copy
import datetime
import tweet_requester

STOP_WORDS_FILE = "word_files/stop_words.txt"
POSITIVE_WORDS_FILE = "word_files/positive_words.txt"
NEGATIVE_WORDS_FILE = "word_files/negative_words.txt"

def process_text(text, stop_words_list):

	#strip out puncutation
	text = text.strip().encode('utf-8').translate(None, string.punctuation)
	
	#lowercase
	text = text.lower()

	count = collections.Counter(text.split()) #split on spaces
	
	#remove stop words
	count = prune_stop_words(count, stop_words_list)

	return count

def prune_stop_words(counter, stop_words_list):

	#todo add '&' to stop words and filter out

	for word in stop_words_list:
		if word in counter:
			del counter[word]

	return counter

def filter_positive_negative_words(counter, positive_set, negative_set):
	negative = {}
	positive = {}
	for word, count in counter.items():
		if word in positive_set:
			positive[word] = count
		elif word in negative_set:
			negative[word] = count
	return collections.Counter(positive), collections.Counter(negative)

#todo clean up with the three below
def load_stop_words():
	l = []
	stop_words_file = open(STOP_WORDS_FILE, "r")
	for line in stop_words_file:
		l.append(line.rstrip())
	stop_words_file.close()
	return l

def load_positive_words():
	positive_words_file = open(POSITIVE_WORDS_FILE, "r")
	l = []
	for line in positive_words_file:
		l.append(line.rstrip())
	positive_words_file.close()
	return frozenset(l)

def load_negative_words():
	negative_words_file = open(NEGATIVE_WORDS_FILE, "r")
	l = []
	for line in negative_words_file:
		l.append(line.rstrip())
	negative_words_file.close()
	return frozenset(l)

def barplot_count(counter, plot_title, color):

	labels, values = zip(*counter.most_common(10))

	plt.rcdefaults()
	figure, axes = plt.subplots()

	axes.set_title(plot_title)
	axes.set_autoscale_on(True)
	axes.invert_yaxis() 

	indexes = np.arange(len(labels))

	axes.barh(indexes, values, 0.5, align='center', color=color)

	plt.yticks(indexes, labels)
	plt.xticks(np.arange(0, values[0]+1, step=1))
	plt.tight_layout()
	#plt.show()

	return figure

def generate_wordcloud(counter):
	wordcloud= WordCloud().generate_from_frequencies(counter)
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

def generate_stats_and_plots(tweeter, tweet_dictionary):

	reload(sys)
	sys.setdefaultencoding('utf8')
	tweet_list = tweet_dict.values()

	#todo pass as arguments for function so we only have to load once
	#would be nice when processing multiple twitter accounts
	p_set = load_positive_words()	
	n_set = load_negative_words()

	counter = collections.Counter()
	positive_counter = collections.Counter()
	negative_counter = collections.Counter()

	average_words_per_tweet = 0
	average_positive_words = 0
	average_negative_words = 0

	stop_words_list = load_stop_words()

	#count words for each tweet
	for tweet in tweet_list:

		c = process_text(tweet, stop_words_list)

		p_count, n_count = filter_positive_negative_words(c, p_set, n_set)

		average_words_per_tweet += sum(c.values())
		average_positive_words += sum(p_count.values())
		average_negative_words += sum(n_count.values())

		#combine counts
		counter += c
		positive_counter += p_count
		negative_counter += n_count

	tweet_list_length = len(tweet_list)
	average_words_per_tweet = average_words_per_tweet / tweet_list_length
	average_positive_words = average_positive_words / tweet_list_length #per tweet
	average_negative_words = average_negative_words / tweet_list_length #per tweet

	counter_value_sum = sum(counter.values())
	positive_word_percentage = 1.0 * sum(positive_counter.values()) / counter_value_sum * 100
	negative_word_percentage = 1.0 * sum(negative_counter.values()) / counter_value_sum * 100

	#convert unix time keys to strings
	tweet_dict_keys_list = list(tweet_dict.keys())
	start_date = datetime.datetime.fromtimestamp(tweet_dict_keys_list[0]).strftime('%Y-%m-%dZ%H:%M:%S')
	end_date = datetime.datetime.fromtimestamp(tweet_dict_keys_list[len(tweet_dict_keys_list)-1]).strftime('%Y-%m-%dZ%H:%M:%S')

	now = datetime.datetime.now()
	now_string = now.strftime("%Y-%m-%dT%H:%M:%S")

	#save generated figures
	file_names = []
	figure = barplot_count(counter, tweeter + ' Word Count\n\n'+start_date + ' - ' + end_date, 'g')
	fn = tweeter + '_word_count_' + now_string + '.png'
	file_names.append(fn)
	plt.savefig(fn, edgecolor='b')
	
	figure = barplot_count(positive_counter, tweeter + ' Positive Count\n\n'+start_date + ' - ' + end_date, 'b')
	fn = tweeter + '_positive_count_' + now_string + '.png'
	file_names.append(fn)
	plt.savefig(fn, edgecolor='b')
	
	figure = barplot_count(negative_counter, tweeter + ' Negative Count\n\n'+start_date + ' - ' + end_date, 'r')
	fn = tweeter + '_negative_count_' + now_string + '.png'
	file_names.append(fn)
	plt.savefig(fn, edgecolor='b')

	print file_names

	#plot positive / negative word percentage against polling numbers

	#now post to jekyll blog 
	#    with average words per tweet
	#    with percentage positive words
	#    with percentage negative words

	#todo pickle / save daily counts for analysis later 



if __name__ == "__main__":
	
	handles = []
	#tweet_dict = collections.OrderedDict([(1527106734.0, 'There will be big news coming soon for our great American Autoworkers. After many decades of losing your jobs to other countries, you have waited long enough!'), (1527107646.0, 'WITCH HUNT!'), (1527117544.0, 'Thank you @SBAList! #SBAGala https://t.co/mPKwukX08o'), (1527128963.0, 'Today on Long Island, we were all moved to be joined by families who have suffered unthinkable heartbreak at the hands of MS-13. I was truly honored to be joined again by the courageous families who were my guests at the State of the Union... https://t.co/Gs0CGJYqXU'), (1527129318.0, 'Crippling loopholes in our laws have enabled MS-13 gang members and other criminals to infiltrate our communities - and Democrats in Congress REFUSE to close these loopholes, including the disgraceful practice known as Catch-and-Release. Democrats must abandon their resistance... https://t.co/VkMCIzwt8v'), (1527144107.0, 'Thank you to all of the incredible law enforcement officers and firefighters in Bethpage, New York. Keep up the great work! https://t.co/SMaZ8Hfas4'), (1527145729.0, 'Great to be in New York for the day. Heading back to the @WhiteHouse now, lots of work to be done! https://t.co/w3LUiQ8SWh'), (1527148684.0, 'Will be interviewed on @foxandfriends tomorrow morning at 6:00 A.M. Enjoy!'), (1527189668.0, 'Clapper has now admitted that there was Spying in my campaign. Large dollars were paid to the Spy, far beyond normal. Starting to look like one of the biggest political scandals in U.S. history. SPYGATE - a terrible thing!'), (1527190469.0, 'Not surprisingly, the GREAT Men &amp; Women of the FBI are starting to speak out against Comey, McCabe and all of the political corruption and poor leadership found within the top ranks of the FBI. Comey was a terrible and corrupt leader who inflicted great pain on the FBI! #SPYGATE'), (1527203905.0, 'Sadly, I was forced to cancel the Summit Meeting in Singapore with Kim Jong Un. https://t.co/rLwXxBxFKx'), (1527204278.0, 'It was my great honor to host a roundtable re: MS-13 yesterday in Bethpage, New York. Democrats must abandon their resistance to border security so that we can SUPPORT law enforcement and SAVE innocent lives! https://t.co/pxe9Z4efyZ'), (1527206271.0, 'I have decided to terminate the planned Summit in Singapore on June 12th. While many things can happen and a great opportunity lies ahead potentially, I believe that this is a tremendous setback for North Korea and indeed a setback for the world... https://t.co/jT0GfxT0Lc'), (1527209676.0, 'Today, it was my honor to sign #S2155, the "Economic Growth, Regulatory Relief, and Consumer Protection Act.\xe2\x80\x9d Read more: https://t.co/sYZ4PzzxxW https://t.co/gi0qGe6ukX'), (1527221912.0, 'Today, it was my great honor to present the #MedalOfHonor to @USNavy (SEAL) Master Chief Special Warfare Operator Britt Slabinski in the East Room of the @WhiteHouse. Full ceremony: https://t.co/2UldFozRh1 https://t.co/R3ACmkWsqJ')])
	#handle = 'SenSanders'
	#handle = 'realDonaldTrump'
	#handle = 'LindseyGrahamSC'
	#handles.append('NancyPelosi')
	#handles.append('SenateMajLdr')
	#handles.append('VP')
	#handles.append('SenJohnMcCain')
	#handles.append('RandPaul')
	handles.append('SenWarren')
	
	for handle in handles:
		tweet_dict = tweet_requester.search_twitter(handle, '2018-05-23', '2018-05-26')
		generate_stats_and_plots(handle, tweet_dict)
