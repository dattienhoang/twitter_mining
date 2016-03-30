# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 13:16:54 2015

@author: Dat Tien Hoang

"""
print 'BEGIN read_twitter_stream.py'
print '...importing packages'
import json
import matplotlib.pyplot as plt
import pandas as pd
import re

def word_in_text(word, text):
    if text == None:
        text = 'None'
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

def word_notin_text(word, text):
    if text == None:
        text = 'None'
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return False
    return True

print '...ok starting main pro'
tweets_data_path = [ \
'mtltor_20151111_1550P__20151112_0935A.txt',
'mtltor_20151112_1100A__20151112_1725P.txt']

tweets_data = []
for file in range(len(tweets_data_path)):
    tweets_file = open(tweets_data_path[file], "r")
    print '...twitter stream file found'
    print '......', tweets_file
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
print len(tweets_data)
print '...searching for incomplete tweet entries'
excise = []
for iline in range(len(tweets_data)):
    #print iline
    if 'text' not in tweets_data[iline]:
        excise.append(iline)
if len(excise) != 0:
    tweets_data = [i for j, i in enumerate(tweets_data) if j not in excise]
    print '......incomplete tweets found and excised!'
        
#print (tweets_data[1])['lang']
#print (tweets_data[1])['text'].encode('utf-8', errors='replace')

#print len(tweets_data), range
#print type(tweets_data)
#print (tweets_data[0])['text']
#for i in range(len(tweets_data)):
#    print 'tweet#:', i
#    print (tweets_data[i])['text'].encode('utf-8', errors='replace')

print '...amount of tweets in data set:', len(tweets_data)
print '...structuring tweets'

tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8', 
                 errors='replace'), tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] \
                         if tweet['place'] != None else None, tweets_data)

print '...done structuring. show basic structure results'

#first simple characterization of this data...plot tweets by language
tweets_by_lang = tweets['lang'].value_counts()
print '......showing language data'
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:10].plot(ax=ax, kind='bar', color='red')
plt.show()
#issue a pause here...example result
#raw_input("Press ENTER to continue")

#another simple characterization of this data...plot tweets by country
tweets_by_country = tweets['country'].value_counts()
print '......showing country data'
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:10].plot(ax=ax, kind='bar', color='blue')
plt.show()

#segregate by tags in 
print '...segregate by tags'
tweets['montreal'] = tweets['text'].apply(lambda tweet: 
                     word_in_text('montreal', tweet))
tweets[u'montréal'] = tweets['text'].apply(lambda tweet: 
                     word_in_text('montréal', tweet))
tweets['mtl'] = tweets['text'].apply(lambda tweet: word_in_text('mtl', tweet) and word_notin_text('montreal', tweet))
#tweets['nyc'] = tweets['text'].apply(lambda tweet: word_in_text('nyc', tweet))
tweets['toronto'] = tweets['text'].apply(lambda tweet: word_in_text('toronto', tweet))

print '......tag counts'
print '......', tweets['montreal'].value_counts()[True]
print '......', tweets['mtl'].value_counts()[True]
print '......', tweets[u'montréal'].value_counts()[True]
#print '......', tweets['nyc'].value_counts()[True]
print '......', tweets['toronto'].value_counts()[True]

#display according to tags...
tags = ['montreal', 'mtl', u'montréal', 'toronto']
tweets_by_tag = [tweets['montreal'].value_counts()[True], tweets['mtl'].value_counts()[True], tweets[u'montréal'].value_counts()[True], tweets['toronto'].value_counts()[True]]

x_pos = list(range(len(tags)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_tag, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: montreal vs. toronto (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(tags)
plt.grid()
plt.show()

#refine the data containing the additional keywords
print '...cleaning twitter data'

print '......non-canadian tweets'
tweets['NotCA'] = tweets['country'].apply(lambda tweet: word_notin_text('canada', tweet))
tweets['relevant'] = tweets['country'].apply(lambda tweet: word_notin_text('canada', tweet))

print tweets['NotCA'].value_counts()[True]
print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......canadian tweets'
tweets['Canada'] = tweets['country'].apply(lambda tweet: word_in_text('canada', tweet))
tweets['relevant'] = tweets['country'].apply(lambda tweet: word_in_text('canada', tweet))

print tweets['Canada'].value_counts()[True]
print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......french tweets'
tweets['fr'] = tweets['lang'].apply(lambda tweet: word_in_text('fr', tweet))
tweets['relevant'] = tweets['lang'].apply(lambda tweet: word_in_text('fr', tweet))

print tweets['fr'].value_counts()[True]
print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......french and foreign tweets'
tweets['relevant_L'] = tweets['lang'].apply(lambda tweet: word_in_text('fr', tweet))
tweets['relevant_C'] = tweets['country'].apply(lambda tweet: word_notin_text('canada', tweet))
#^need to do a double relevance bc picking two things of different categories!
#print tweets['relevant_L'] # a list of tweet indices and true/false
tweets['relevant'] = tweets['relevant_L']
for i in range(len(tweets['relevant_L'])):
    if (tweets['relevant_L'])[i] == True and (tweets['relevant_C'])[i] == True:
        (tweets['relevant'])[i] = True
    else:
        (tweets['relevant'])[i] = False

print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

intl_mtl_f = \
tweets[tweets['relevant'] == True]['montreal'].value_counts()[True] + \
tweets[tweets['relevant'] == True]['mtl'].value_counts()[True] + \
tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]

intl_tor_f = tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......french and canadian tweets'
tweets['relevant_L'] = tweets['lang'].apply(lambda tweet: word_in_text('fr', tweet))
tweets['relevant_C'] = tweets['country'].apply(lambda tweet: word_in_text('canada', tweet))
#^need to do a double relevance bc picking two things of different categories!
#print tweets['relevant_L'] # a list of tweet indices and true/false
tweets['relevant'] = tweets['relevant_L']
for i in range(len(tweets['relevant_L'])):
    if (tweets['relevant_L'])[i] == True and (tweets['relevant_C'])[i] == True:
        (tweets['relevant'])[i] = True
    else:
        (tweets['relevant'])[i] = False

print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

can_mtl_f = \
tweets[tweets['relevant'] == True]['montreal'].value_counts()[True] + \
tweets[tweets['relevant'] == True]['mtl'].value_counts()[True] + \
tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]

can_tor_f = tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......english and foreign tweets'
tweets['relevant_L'] = tweets['lang'].apply(lambda tweet: word_in_text('en', tweet))
tweets['relevant_C'] = tweets['country'].apply(lambda tweet: word_notin_text('canada', tweet))
#^need to do a double relevance bc picking two things of different categories!
#print tweets['relevant_L'] # a list of tweet indices and true/false
tweets['relevant'] = tweets['relevant_L']
for i in range(len(tweets['relevant_L'])):
    if (tweets['relevant_L'])[i] == True and (tweets['relevant_C'])[i] == True:
        (tweets['relevant'])[i] = True
    else:
        (tweets['relevant'])[i] = False

print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

intl_mtl_e = \
tweets[tweets['relevant'] == True]['montreal'].value_counts()[True] + \
tweets[tweets['relevant'] == True]['mtl'].value_counts()[True] + \
tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]

intl_tor_e = tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

print '......english and canadian tweets'
tweets['relevant_L'] = tweets['lang'].apply(lambda tweet: word_in_text('en', tweet))
tweets['relevant_C'] = tweets['country'].apply(lambda tweet: word_in_text('canada', tweet))
#^need to do a double relevance bc picking two things of different categories!
#print tweets['relevant_L'] # a list of tweet indices and true/false
tweets['relevant'] = tweets['relevant_L']
for i in range(len(tweets['relevant_L'])):
    if (tweets['relevant_L'])[i] == True and (tweets['relevant_C'])[i] == True:
        (tweets['relevant'])[i] = True
    else:
        (tweets['relevant'])[i] = False

print tweets['relevant'].value_counts()[True]

print tweets[tweets['relevant'] == True]['montreal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['mtl'].value_counts()[True]
print tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]
print tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

can_mtl_e = \
tweets[tweets['relevant'] == True]['montreal'].value_counts()[True] + \
tweets[tweets['relevant'] == True]['mtl'].value_counts()[True] + \
tweets[tweets['relevant'] == True][u'montréal'].value_counts()[True]

can_tor_e = tweets[tweets['relevant'] == True]['toronto'].value_counts()[True]

#first plot canadian tweets
#x-axis is percent of anglo tweets, scale shifted to start from -50%
#y-axis is the number of tweets in thousands

#plot canadian tweets first...first franco/anglophones for toronto
xs = [-50,(float(can_tor_f)/(can_mtl_f+can_tor_f))*100 - 50.,50,-50]
ys = [0,(can_tor_f+can_tor_e)/1000.,0,0]
plt.plot(xs,ys, color='b', linewidth=2)
plt.fill_between(xs,ys,color='#ccccff')
#now montreal...
xs = [-50,(float(can_mtl_f)/(can_mtl_f+can_tor_f))*100 - 50.,50,-50]
ys = [0,-1*(can_mtl_f+can_mtl_e)/1000.,0,0]
plt.plot(xs,ys, color='r', linewidth=2)
plt.fill_between(xs,ys,color='#ffcccc')
plt.axis([-100,100,-5,5],'off')
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
#annotate
plt.axvline(color='k', linestyle='dashed')
#plt.annotate('Toronto')
plt.show()

#plot international tweets next...first franco/anglophones for toronto
xs = [-50,(float(intl_tor_f)/(intl_mtl_f+intl_tor_f))*100 - 50.,50,-50]
ys = [0,(intl_tor_f+intl_tor_e)/1000.,0,0]
plt.plot(xs,ys, color='b', linewidth=2)
plt.fill_between(xs,ys,color='#ccccff')
#now montreal...
xs = [-50,(float(intl_mtl_f)/(intl_mtl_f+intl_tor_f))*100 - 50.,50,-50]
ys = [0,-1*(intl_mtl_f+intl_mtl_e)/1000.,0,0]
plt.plot(xs,ys, color='r', linewidth=2)
plt.fill_between(xs,ys,color='#ffcccc')
plt.axis([-100,100,-50,50],'off','equal')
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
#annotate
plt.axvline(color='k', linestyle='dashed')
#plt.annotate('Toronto')
plt.show()

print 'END read_twitter_stream.py'
