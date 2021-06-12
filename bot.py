import tweepy
import time
import main
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

consumer_key = "XXXXXXXX"
consumer_secret = "XXXXXX"

key = "XXXXXXXXX"
secret = "XXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

last_seen = "last_seen_id.txt"
covid = "covid.txt"


def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, "r")
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def read_last_tweet(FILE_NAME):
    file_read = open(FILE_NAME, "r")
    last_seen_id = file_read.read().strip()
    file_read.close()
    return last_seen_id
def store_last_tweet(FILE_NAME, tweet):
    file_write = open(FILE_NAME, "w")
    file_write.write(tweet)
    file_write.close()


def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, "w")
    file_write.write(str(last_seen_id))
    file_write.close()


def reply():
    tweets = api.mentions_timeline(read_last_seen(last_seen))
    for tweet in reversed(tweets):
        try:
            print("Found tweet: " + tweet.text)
            api.update_status("@" + tweet.user.screen_name + " 🚨 Hello " + tweet.user.screen_name + " 🚨 " + status(),
                              tweet.id)
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)

            print("Retweet done! \n Tweet liked \n Tweet ID : " + str(tweet.id))
            store_last_seen(last_seen, tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)


def status():
    date = main.getDate()
    cases = main.getCases()
    cases = locale.format_string("%d", int(cases), grouping=True)
    deaths = main.getDeaths()
    deaths = locale.format_string("%d", int(deaths), grouping=True)
    tweet = "As of " + date + " There was " + cases + " cases and " + deaths + " deaths due to Covid in the USA."
    oldTweet = read_last_tweet(covid)

    if tweet != oldTweet:
        try:
            api.update_status(tweet)
            print("Status update : " + tweet)
            store_last_tweet(covid, tweet)
        except tweepy.TweepError as e:
            print(e.reason)
    else:
        print("nothing new, moving on!")
    return tweet


while True:
    status()
    print("Looking for reply...")
    reply()
    time.sleep(12)
