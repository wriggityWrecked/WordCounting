import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import tweet_requester
import counting_plotting_tools

nltk.download('vader_lexicon')

def analyze_text(text):

	sid = SentimentIntensityAnalyzer()
	#print(text)
	scores = sid.polarity_scores(text)
	return scores

if __name__ == "__main__":

	now = datetime.now()
	next_day = (now + timedelta(days=1)).strftime("%Y-%m-%d")
	last_day = (now - timedelta(days=1)).strftime("%Y-%m-%d")
	tweet_dict = tweet_requester.search_twitter('realDonaldTrump', last_day, next_day, True)
	
	lista = []
	listb = []
	listc = []
	listd = []
	for text in tweet_dict.values():
		data = analyze_text(text)
		lista.append(data['compound'])
		listb.append(data['pos'])
		listc.append(data['neg'])
		listd.append(data['neu'])


	counting_plotting_tools.plot_compound_sentinment(lista, listb, listc, listd, 'test')