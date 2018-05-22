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

STOP_WORDS = []
STOP_WORDS_FILE = "word_files/stop_words.txt"
POSITIVE_WORDS_FILE = "word_files/positive_words.txt"
NEGATIVE_WORDS_FILE = "word_files/negative_words.txt"

def process_text(text):
	print text
	#strip out puncutation
	text = text.strip().encode('utf-8').translate(None, string.punctuation)
	
	#lowercase
	text = text.lower()

	count = collections.Counter(text.split()) #split on spaces
	print count
	total_number_of_words = sum(count.values())

	#remove stop words
	count = prune_stop_words(count)

	return count, total_number_of_words

def prune_stop_words(counter):
	load_stop_words()

	for word in STOP_WORDS:
		if word in counter:
			del counter[word] #remove the input_list element from the counter

	return counter

def filter_positive_negative_words(counter, frozen_set):
	for word in counter.keys():
		if word not in frozen_set:
			print 'filtering ' + str(word)
			del counter[word] #TODO RETURN POSITIVE AND NEGATIVE, STUPID TO FILTER ONCE
	return counter

#todo clean up with the three below
def load_stop_words():
	global STOP_WORDS
	if not STOP_WORDS:
		stop_words_file = open(STOP_WORDS_FILE, "r")
		for line in stop_words_file:
			STOP_WORDS.append(line.rstrip())
		stop_words_file.close()

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

	indexes = np.arange(len(labels))

	plt.bar(indexes, values, 0.6, align='center', color=color)
	plt.ylabel('Word Count')
	plt.title(plot_title)
	plt.xticks(indexes, labels)
	plt.yticks(np.arange(0, values[0]+1, step=1))
	plt.show()

def generate_wordcloud(counter):
	wordcloud= WordCloud().generate_from_frequencies(counter)
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

def test():
	#tweet_list = [u'Thank you to the Washington Examiner and @CortesSteve on the great article - on WINNING! https://t.co/b5dfUABN5q', u'#PeaceOfficersMemorialDay https://t.co/agxulpPyag', u'Today is one of the most important and solemn occasions of the year \u2013 the day we pay tribute to the Law Enforcement Heroes who gave their lives in the line of duty. They made the ultimate sacrifice so that we could live in safety and peace. We stand with our police (HEROES) 100%! https://t.co/XDtYRUeOk1', u'Nebraska - make sure you get out to the polls and VOTE for Deb Fischer today! https://t.co/bDHVaGv2FS', u'Can you believe that with all of the made up, unsourced stories I get from the Fake News Media, together with the  $10,000,000 Russian Witch Hunt (there is no Collusion), I now have my best Poll Numbers in a year. Much of the Media may be corrupt, but the People truly get it!', u'Trade negotiations are continuing with China. They have been making hundreds of billions of dollars a year from the U.S., for many years. Stay tuned!', u'Our great First Lady is doing really well. Will be leaving hospital in 2 or 3 days. Thank you for so much love and support!', u'Heading over to Walter Reed Medical Center to see our great First Lady, Melania. Successful procedure, she is in good spirits. Thank you to all of the well-wishers!', u'The so-called leaks coming out of the White House are a massive over  exaggeration put out by the Fake News Media in order to make us look as bad as possible. With that being said, leakers are traitors and cowards, and we will find out who they are!', u'ZTE, the large Chinese phone company, buys a big percentage of individual parts from U.S. companies. This is also reflective of the larger trade deal we are negotiating with China and my personal relationship with President Xi.', u'#USEmbassyJerusalem https://t.co/f1SFvrkcAH', u'Big day for Israel. Congratulations!', u'U.S. Embassy opening in Jerusalem will be covered live on @FoxNews &amp; @FoxBusiness. Lead up to 9:00 A.M. (eastern) event has already begun. A great day for Israel!']
	reload(sys)
	sys.setdefaultencoding('utf8')
	#tweet_dict = {'Thu May 17 12:45:03 +0000 2018': 'Wow, word seems to be coming out that the Obama FBI \xe2\x80\x9cSPIED ON THE TRUMP CAMPAIGN WITH AN EMBEDDED INFORMANT.\xe2\x80\x9d Andrew McCarthy says, \xe2\x80\x9cThere\xe2\x80\x99s probably no doubt that they had at least one confidential informant in the campaign.\xe2\x80\x9d If so, this is bigger than Watergate!', 'Thu May 17 15:25:57 +0000 2018': 'Congrats to the House for passing the VA MISSION Act yesterday. Without this funding our veterans will be forced to stand in never ending lines in order to receive care. Putting politics over our veterans care is UNACCEPTABLE \xe2\x80\x93 Senate must vote yes on this bill by Memorial Day!', 'Wed May 16 18:40:36 +0000 2018': '...and voted against the massive Tax Cut Bill. He\xe2\x80\x99s also weak on borders and crime. Sadly, our great Military and Vets mean nothing to Bobby Jr. Lou Barletta will win! #MAGA', 'Wed May 16 18:40:35 +0000 2018': 'Lou Barletta will be a great Senator for Pennsylvania but his opponent, Bob Casey, has been a do-nothing Senator who only shows up at election time. He votes along the Nancy Pelosi, Elizabeth Warren lines, loves sanctuary cities, bad and expensive healthcare...', 'Wed May 16 17:50:58 +0000 2018': 'Today, it was my great honor to welcome President Mirziyoyev of Uzbekistan to the @WhiteHouse! https://t.co/3EkHChjnYA', 'Wed May 16 13:09:19 +0000 2018': 'The Washington Post and CNN have typically written false stories about our trade negotiations with China. Nothing has happened with ZTE except as it pertains to the larger trade deal. Our country has been losing hundreds of billions of dollars a year with China...', 'Wed May 16 12:07:52 +0000 2018': 'Congratulations to Lou Barletta of Pennsylvania. He will be a great Senator and will represent his people well - like they haven\xe2\x80\x99t been represented in many years. Lou is a friend of mine and a special guy, he will very much help MAKE AMERICA GREAT AGAIN!', 'Tue May 15 20:29:39 +0000 2018': 'Thank you to the Washington Examiner and @CortesSteve on the great article - on WINNING! https://t.co/b5dfUABN5q', 'Wed May 16 22:57:25 +0000 2018': 'Gina Haspel is one step closer to leading our brave men and women at the CIA. She is exceptionally qualified and the Senate should confirm her immediately. We need her to keep our great country safe! #ConfirmGina', 'Wed May 16 12:25:42 +0000 2018': 'Congratulations to Deb Fischer. The people of Nebraska have seen what a great job she is doing - and it showed up at the ballot box! #MAGA', 'Thu May 17 13:52:44 +0000 2018': 'Despite the disgusting, illegal and unwarranted Witch Hunt, we have had the most successful first 17 month Administration in U.S. history - by far! Sorry to the Fake News Media and \xe2\x80\x9cHaters,\xe2\x80\x9d but that\xe2\x80\x99s the way it is!', 'Wed May 16 17:21:18 +0000 2018': 'House votes today on Choice/MISSION Act. Who will stand with our Great Vets, caregivers, and Veterans Service Organizations? Must get Choice passed by Memorial Day!', 'Wed May 16 13:09:20 +0000 2018': '...We have not seen China\xe2\x80\x99s demands yet, which should be few in that previous U.S. Administrations have done so poorly in negotiating. China has seen our demands. There has been no folding as the media would love people to believe, the meetings...', 'Thu May 17 11:28:09 +0000 2018': 'Congratulations America, we are now into the second year of the greatest Witch Hunt in American History...and there is still No Collusion and No Obstruction. The only Collusion was that done by Democrats who were unable to win an Election despite the spending of far more money!'}
	#tweet_dict = {'Thu May 17 22:17:08 +0000 2018': 'It was my great honor to visit with our HEROES last night at Walter Reed Medical Center. There is nobody like them! https://t.co/fG5W1SwIHK', 'Thu May 17 22:14:23 +0000 2018': 'Tomorrow, the House will vote on a strong Farm Bill, which includes work requirements. We must support our Nation\xe2\x80\x99s great farmers!', 'Fri May 18 10:24:53 +0000 2018': '\xe2\x80\x9cApparently the DOJ put a Spy in the Trump Campaign. This has never been done before and by any means necessary, they are out to frame Donald Trump for crimes he didn\xe2\x80\x99t commit.\xe2\x80\x9d  David Asman  @LouDobbs @GreggJarrett   Really bad stuff!', 'Fri May 18 20:22:25 +0000 2018': 'America is a Nation that believes in the power of redemption. America is a Nation that believes in second chances - and America is a Nation that believes that the best is always yet to come! #PrisonReform https://t.co/Yk5UJUYgHN', 'Fri May 18 22:57:09 +0000 2018': 'America is blessed with extraordinary energy abundance, including more than 250 years worth of beautiful clean coal. We have ended the war on coal, and will continue to work to promote American energy dominance!', 'Fri May 18 22:00:58 +0000 2018': 'California finally deserves a great Governor, one who understands borders, crime and lowering taxes. John Cox is the man - he\xe2\x80\x99ll be the best Governor you\xe2\x80\x99ve ever had. I fully endorse John Cox for Governor and look forward to working with him to Make California Great Again!', 'Fri May 18 16:34:24 +0000 2018': 'We grieve for the terrible loss of life, and send our support and love to everyone affected by this horrible attack in Texas. To the students, families, teachers and personnel at Santa Fe High School \xe2\x80\x93 we are with you in this tragic hour, and we will be with you forever... https://t.co/LtJ0D29Hsv', 'Fri May 18 15:05:35 +0000 2018': 'School shooting in Texas. Early reports not looking good. God bless all!', 'Fri May 18 20:41:21 +0000 2018': 'Just met with UN Secretary-General Ant\xc3\xb3nio Guterres who is working hard to \xe2\x80\x9cMake the United Nations Great Again.\xe2\x80\x9d When the UN does more to solve conflicts around the world, it means the U.S. has less to do and we save money. @NikkiHaley is doing a fantastic job! https://t.co/pqUv6cyH2z', 'Fri May 18 13:50:11 +0000 2018': 'Reports are there was indeed at least one FBI representative implanted, for political purposes, into my campaign for president. It took place very early on, and long before the phony Russia Hoax became a \xe2\x80\x9chot\xe2\x80\x9d Fake News story. If true - all time biggest political scandal!', 'Fri May 18 13:38:11 +0000 2018': 'Why isn\xe2\x80\x99t disgraced FBI official Andrew McCabe being investigated for the $700,000 Crooked Hillary Democrats in Virginia, led by Clinton best friend Terry M (under FBI investigation that they killed) gave to McCabe\xe2\x80\x99s wife in her run for office? Then dropped case on Clinton!', 'Fri May 18 10:51:43 +0000 2018': 'Fake News Media had me calling Immigrants, or Illegal Immigrants, \xe2\x80\x9cAnimals.\xe2\x80\x9d Wrong! They were begrudgingly forced to withdraw their stories. I referred to MS 13 Gang Members as \xe2\x80\x9cAnimals,\xe2\x80\x9d a big difference - and so true. Fake News got it purposely wrong, as usual!', 'Thu May 17 21:53:51 +0000 2018': 'Great talk with my friend President Mauricio Macri of Argentina this week. He is doing such a good job for Argentina. I support his vision for transforming his country\xe2\x80\x99s economy and unleashing its potential!'}
	tweet_dict = {'Thu May 17 22:17:08 +0000 2018': 'It was my great honor to visit with our HEROES last night at Walter Reed Medical Center. There is nobody like them! https://t.co/fG5W1SwIHK', 'Thu May 17 22:14:23 +0000 2018': 'Tomorrow, the House will vote on a strong Farm Bill, which includes work requirements. We must support our Nation\xe2\x80\x99s great farmers!', 'Fri May 18 10:24:53 +0000 2018': '\xe2\x80\x9cApparently the DOJ put a Spy in the Trump Campaign. This has never been done before and by any means necessary, they are out to frame Donald Trump for crimes he didn\xe2\x80\x99t commit.\xe2\x80\x9d  David Asman  @LouDobbs @GreggJarrett   Really bad stuff!', 'Fri May 18 20:22:25 +0000 2018': 'America is a Nation that believes in the power of redemption. America is a Nation that believes in second chances - and America is a Nation that believes that the best is always yet to come! #PrisonReform https://t.co/Yk5UJUYgHN', 'Fri May 18 22:57:09 +0000 2018': 'America is blessed with extraordinary energy abundance, including more than 250 years worth of beautiful clean coal. We have ended the war on coal, and will continue to work to promote American energy dominance!', 'Fri May 18 22:00:58 +0000 2018': 'California finally deserves a great Governor, one who understands borders, crime and lowering taxes. John Cox is the man - he\xe2\x80\x99ll be the best Governor you\xe2\x80\x99ve ever had. I fully endorse John Cox for Governor and look forward to working with him to Make California Great Again!', 'Fri May 18 16:34:24 +0000 2018': 'We grieve for the terrible loss of life, and send our support and love to everyone affected by this horrible attack in Texas. To the students, families, teachers and personnel at Santa Fe High School \xe2\x80\x93 we are with you in this tragic hour, and we will be with you forever... https://t.co/LtJ0D29Hsv', 'Fri May 18 15:05:35 +0000 2018': 'School shooting in Texas. Early reports not looking good. God bless all!', 'Fri May 18 20:41:21 +0000 2018': 'Just met with UN Secretary-General Ant\xc3\xb3nio Guterres who is working hard to \xe2\x80\x9cMake the United Nations Great Again.\xe2\x80\x9d When the UN does more to solve conflicts around the world, it means the U.S. has less to do and we save money. @NikkiHaley is doing a fantastic job! https://t.co/pqUv6cyH2z', 'Fri May 18 13:50:11 +0000 2018': 'Reports are there was indeed at least one FBI representative implanted, for political purposes, into my campaign for president. It took place very early on, and long before the phony Russia Hoax became a \xe2\x80\x9chot\xe2\x80\x9d Fake News story. If true - all time biggest political scandal!', 'Fri May 18 13:38:11 +0000 2018': 'Why isn\xe2\x80\x99t disgraced FBI official Andrew McCabe being investigated for the $700,000 Crooked Hillary Democrats in Virginia, led by Clinton best friend Terry M (under FBI investigation that they killed) gave to McCabe\xe2\x80\x99s wife in her run for office? Then dropped case on Clinton!', 'Fri May 18 10:51:43 +0000 2018': 'Fake News Media had me calling Immigrants, or Illegal Immigrants, \xe2\x80\x9cAnimals.\xe2\x80\x9d Wrong! They were begrudgingly forced to withdraw their stories. I referred to MS 13 Gang Members as \xe2\x80\x9cAnimals,\xe2\x80\x9d a big difference - and so true. Fake News got it purposely wrong, as usual!', 'Thu May 17 21:53:51 +0000 2018': 'Great talk with my friend President Mauricio Macri of Argentina this week. He is doing such a good job for Argentina. I support his vision for transforming his country\xe2\x80\x99s economy and unleashing its potential!'}
	tweet_list = tweet_dict.values()

	#https://matplotlib.org/gallery/subplots_axes_and_figures/subplot.html

	counter = collections.Counter()
	average_number_of_words = 0
	for tweet in tweet_list:	
		c, a = process_text(tweet)
		counter += c
		average_number_of_words += a
		#todo count positive and negative to provide averages per tweet

	print average_number_of_words / 1.0 * len(tweet_list)
	#barplot_count(counter, 'Trump Count, avg=' + str(average_number_of_words))

	pfset = load_positive_words()
	positive_count = filter_positive_negative_words(copy.deepcopy(counter), pfset)
	
	pnset = load_negative_words()
	negative_count = filter_positive_negative_words(copy.deepcopy(counter), pnset)

	#todo positive percentage of total
	#todo negative percentage of total
	barplot_count(positive_count, 'Positive Count, avg=' + str(sum(positive_count.values())), 'b')
	barplot_count(negative_count, 'Negative Count, total=' + str(sum(negative_count.values())), 'r')

	#generate_wordcloud(counter)
	#Positive and or negative separately? or just total

	#todo persist totals, and entirety of the counter (disregard positive / negative as we can re-filter if need be)

if __name__ == "__main__":
	test()
