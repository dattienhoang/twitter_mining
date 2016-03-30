# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 11:46:01 2015

@author: Dat Tien Hoang
"""
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "455401861-viU2AifsDdblIWmr9vTFDrCsCasGPZNGyUOu8F5P"
access_token_secret = "4csu90ftGXIz7fafv6ED0v5Hog9aH0p0tfbmFxydmjeU3"
consumer_key = "BJL8JF2AN34IfTWBzEB73TiBb"
consumer_secret = "c2E3A4bhOaCdyn7Od8ff7tZysfAPK7gpzdlrMtKxqAgaJV1E4T"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['keyword of interest'])
