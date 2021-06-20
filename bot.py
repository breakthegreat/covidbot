#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import tweepy
import time
import random
import locale


from US_General import USCovid
from State import listState

locale.setlocale(locale.LC_ALL, 'en_US')

consumer_key = "p3AHgsrIVRAU9w6KIHi4lc8hE"
consumer_secret = "H32uWhmcuYfe3YRC2bB8A3yudGXmCb2JxyXxj54EQrs5mhOD4W"

key = "1403551620680589312-qFuSjzXcpngQARw31rESUzLj0jNNvp"
secret = "B2iXnJg4fxMyxcCZsoH6dPEG40qg3w3ov4gOYGA02SRAZ"

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


def replyCovidUSA():
    tweets = api.mentions_timeline(read_last_seen(last_seen))
    for tweet in reversed(tweets):
        if "USA".lower() or "United States".lower() in tweet.full_text.lower():
            try:
                print("Found tweet: " + tweet.text)
                api.update_status(
                    "@" + tweet.user.screen_name + " 🚨 Hello " + tweet.user.screen_name + " 🚨 " + status(),
                    tweet.id)

                api.create_favorite(tweet.id)

                print("Tweet liked \n Tweet ID : " + str(tweet.id))
                store_last_seen(last_seen, tweet.id)

            except tweepy.TweepError as e:
                print(e.reason)


def status():
    s1 = USCovid()
    date = s1.date
    cases = s1.cases
    cases = locale.format_string("%d", int(cases), grouping=True)
    deaths = s1.deaths
    deaths = locale.format_string("%d", int(deaths), grouping=True)
    tweet = "As of " + date + " There was " + cases + " cases and " + deaths + " deaths due to Covid in the USA."

    oldTweet = read_last_tweet(covid)

    if tweet != oldTweet:
        store_last_tweet(covid, tweet)
        try:
            api.update_status(
                tweet + "\n\n Source: nytimes" + "\n\n#Covid19 #CovidUSA #CovidAmerica #coronavirus #covidcases #coviddeaths #covidstats")
            print("Status update : " + tweet)

        except tweepy.TweepError as e:
            print(e.reason)
    else:
        print("Nothing new, let's move on")


def replyCovidState():
    s1 = USCovid()
    date = s1.date
    tweets = api.mentions_timeline(read_last_seen(last_seen), tweet_mode="extended")
    for tweet in reversed(tweets):
        try:
            for x in range(len(listState)):

                if listState[x].name.lower() in tweet.full_text.lower():
                    cases = listState[x].cases
                    cases = locale.format_string("%d", int(cases), grouping=True)
                    deaths = listState[x].deaths
                    deaths = locale.format_string("%d", int(deaths), grouping=True)

                    print("Found tweet: " + tweet.full_text)
                    api.update_status(
                        "@" + tweet.user.screen_name + " 🚨 Hello " + tweet.user.screen_name + " 🚨 \n\n🇺🇸 State of : " +
                        listState[x].name + "\n\n📅 As of " + str(date) + ":\n"
                        + "😷 Cases: " + cases + " \n⚰️ Deaths: " + deaths + "\n\n Source: nytimes " + "\n\n#Covid" +
                        listState[x].name.replace(" ", "") + " #Covid",
                        tweet.id)

                    api.create_favorite(tweet.id)
                    print("Tweet liked \n Tweet ID : " + str(tweet.id))
                    store_last_seen(last_seen, tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)


def sleep(sec):
    for i in range(sec, -1, -1):
        sys.stdout.write("\rWaiting : " + str(i) + ' seconds')
        sys.stdout.flush()
        if i == 0:
            sys.stdout.write("\r")
        time.sleep(1)

print("============================================ COVIDBOT 1.10 ============================================\n"
      "============================================ READY FOR DUTY ============================================")
while True:
    status()

    replyCovidState()

    replyCovidUSA()
    randomNum = random.randint(15, 30)
    sleep(int(randomNum))

# ==================================END=======================================
