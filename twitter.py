import tweepy
from pymongo import MongoClient


CONSUMER_KEY = 'HWfrcgDgiFx4sxyi8mv6fqa0I'
CONSUMER_SECRET = 'ou7mTUWUwa7n5975DBICIyvWpx4XjgGKc5iYgJqEOj8fom4y3s'
ACCESS_TOKEN = '2312617934-5AQ0ybJgdxLrXYbGU98OcSI9FavFTDuDMtAXnoh'
ACCESS_SECRET = 'E4GbLVac03Yneulpn4IGLcScrVboYtdovovytJl0kUZGu'


def connect_twitter ():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	api = tweepy.API(auth)
	return api

def connect_mongo ():
	client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
	db = client['tsentimeter']
	return db

def score_tweet(text, tokenizer, model):

	# Encode the text
	encoded_dict = tokenizer.encode_plus(text, add_special_tokens = True, max_length=160, pad_to_max_length=True, return_tensors='pt', return_attention_mask=True) 

	# Set the device to CPU
	device = torch.device('cpu')
	input_ids = torch.tensor(encoded_dict['input_ids']).to(device)
	attention_masks = torch.tensor(encoded_dict['attention_mask']).to(device)

	# Get our raw outputs
	outputs = model(input_ids, token_type_ids=None, attention_mask=attention_masks)[0]

	# Get the probability of positive sentiment
	sm = torch.nn.Softmax()
	probabilities = sm(outputs) 
	pos_prob = torch.Tensor.cpu(probabilities).detach().numpy()[:,0][0]
	return pos_prob


def store_tweets(model, tokenizer):



	# Connect to the Twitter API
	api = connect_twitter()

	# Connect to the Data Base
	db = connect_mongo()
	tweets_collection = db.tweets

	# This is an example of the fields you should make in your entry
	# entry = {
	# 	'date': '',
	# 	'topic_name': '',
	# 	'search_method': '',
	# 	'tweet_id': '',
	# 	'tweet_text': '',
	# 	'num_likes': '',
	# 	'num_retweets': '',
	# 	'location': ''
	# }

	# The person or entity we are searching
	topics = ["Biden", "Trump"]

	# The type of tweet we are searching for: user_tweets, user_mentions
	search_method = "user_mentions" 

	# Our Twitter search parameters
	searchQuerys = ["@JoeBiden", "@realDonaldTrump"]
	retweet_filter = '-filter:retweets'
	tweetsPerQry = 10

	for i in range(0,2):

		q=searchQuerys[i]+retweet_filter

		# Get the tweets
		mentions = api.search(q=q, count=tweetsPerQry)

		# Loop throught each tweet and save an entry into database
		for mention in mentions:
				tweet = {}

				tweet['topic'] = topics[i]
				tweet['search_method'] = search_method
				tweet['date'] = mention._json['created_at']
				tweet['tweet_id'] = str(mention._json['id'])
				tweet['tweet'] = mention._json['text']
				tweet['retweet_count'] = mention.retweet_count
				tweet['favorite_count'] = mention.favorite_count
				sentiment = score_tweet(mention._json['text'], tokenizer, model)
				tweet['sentiment'] = str(sentiment)
				print(mention._json['text'])
				print(sentiment)
				tweets_collection.insert_one(tweet)




