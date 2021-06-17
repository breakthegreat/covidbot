#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import tweepy
import time
import US_General
import locale
from US_General import us
from State import listState

locale.setlocale(locale.LC_ALL, 'en_US')

consumer_key = "XXXXXXXX"
consumer_secret = "XXXXXXXXXX"

key = "XXXXXXXXXXX"
secret = "XXXXXXXXXXXXXX"

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
        if "USA" or "United States" in tweet.full_text.lower():
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
    date = us.date
    cases = us.cases
    cases = locale.format_string("%d", int(cases), grouping=True)
    deaths = us.deaths
    deaths = locale.format_string("%d", int(deaths), grouping=True)
    tweet = "As of " + date + " There was " + cases + " cases and " + deaths + " deaths due to Covid in the USA."

    oldTweet = read_last_tweet(covid)

    if tweet != oldTweet:
        store_last_tweet(covid, tweet)
        try:
            api.update_status(tweet)
            print("Status update : " + tweet)

        except tweepy.TweepError as e:
            print(e.reason)


def replyCovidState():
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
                        "@" + tweet.user.screen_name + " 🚨 Hello " + tweet.user.screen_name + " 🚨 " + "As of " + str(
                            us.date)
                        + " there was " + cases + " cases and " + deaths + " deaths in " +
                        listState[x].name + " 🚨 ",
                        tweet.id)

                    api.create_favorite(tweet.id)
                    print("Tweet liked \n Tweet ID : " + str(tweet.id))
                    store_last_seen(last_seen, tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)


while True:

    status()

    replyCovidState()
    replyCovidUSA()

    for i in range(15, -1, -1):
        sys.stdout.write("\rWaiting : " + str(i) + ' seconds')
        sys.stdout.flush()
        if i == 0:
            sys.stdout.write("\r")

        time.sleep(1)
#==================================END=======================================
