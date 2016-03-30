# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 13:16:54 2015

@author: Dat Tien Hoang

Notes:

(1) May get an error with httpsclient...DO NOT update the SSLContext

"""
print 'BEGIN read_twitter_stream.py'
print '...importing packages'
import json, requests
import matplotlib.pyplot as plt
import pandas as pd
import re
#import geopy
import plotly.plotly as py

#input latlng is a string formated as: '2.2,3.3'
def reverseGeocode(latlng):
    result = {}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}'
    apikey = 'AIzaSyCUyhnEr2oJmErj3ahn2F9AnK_-QoiVP7o'
    #apikey = 'AIzaSyB6j66BsRb5dp2BLempjh8aLCuf_eNJaGc'
    request = url.format(latlng, apikey)
    #request = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + \
    #          latlng +'&key=' + apikey
    #print request
    data = json.loads(requests.get(request).text)
    if len(data['results']) > 0:
        result = data['results'][0]
    return result

def word_in_text(word, text):
    if text == None:
        text = 'None'
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

states = {
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AS': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DC': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MP': 0,
        'MS': 0,
        'MT': 0,
        'NA': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'PR': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VI': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
}

statescounter = {
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AS': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DC': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MP': 0,
        'MS': 0,
        'MT': 0,
        'NA': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'PR': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VI': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
}

print '...ok starting main pro'
tweets_data_path = [
#files = [
#'left_20160126_A.txt',
#'left_20160126_B.txt',
#'left_20160126_C.txt', 
#'left_20160126_D.txt', 
#'left_20160126_E.txt',
#'left_20160126_F.txt',
#'left_20160126_G.txt',
#'left_20160126_H.txt',
#'left_20160126_I.txt',
#'left_20160126_J.txt']
'left_20160202_A.txt',
'left_20160202_B.txt',
'left_20160202_C.txt',
'left_20160202_D.txt']

sentiments = 'AFINN-111.txt'

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

print '...searching for incomplete tweet entries'
excise = []
for i in range(len(tweets_data)):
    if 'text' not in tweets_data[i]:
        excise.append(i)
if len(excise) != 0:
    tweets_data = [i for j, i in enumerate(tweets_data) if j not in excise]
    print '......incomplete tweets found and excised!'

print '...amount of tweets in data set:', len(tweets_data)
print '...structuring tweets'

tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8', 
                 errors='replace'), tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] \
                    if tweet['place'] != None else None, tweets_data)
tweets['coord'] = map(lambda tweet: tweet['place']['bounding_box']['coordinates'] \
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
ax.set_title('Top 10 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:10].plot(ax=ax, kind='bar', color='red')

#another simple characterization of this data...plot tweets by country
tweets_by_country = tweets['country'].value_counts()
print '......showing country data'
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 10 countries', fontsize=15, fontweight='bold')
tweets_by_country[:10].plot(ax=ax, kind='bar', color='blue')

#country listing is insufficient! what to do...
print '......no. tweets listing country:', len(filter(None, tweets['country']))
print '......no. American tweets:', (tweets['country']=='United States').sum()

#coordinates are in a bounding box...reduce it to something simpler!
print '...geocoding spatial coordinates for American tweets'
meancoord = []
tweets['geocodedat'] = ''
tweets['state'] = ''
for i in range(len(tweets)):
#for i, row in tweets.iterrows():
    #only assign coordinates to american tweets
    if (tweets['coord'][i] != None and tweets['country'][i] == 'United States'):
        a = tweets['coord'][i][0]
        meancoord.append([(a[0][0] + a[1][0] + a[2][0]+ a[3][0])/4,
                          (a[0][1] + a[1][1] + a[2][1]+ a[3][1])/4])
    else:
        meancoord.append(None)
    if meancoord[i] != None:
        #twitter and google have opposite convention for lon, lat ordering
        print '......found coord:', str(meancoord[i][0]) + ',' + \
                                    str(meancoord[i][1])
        #preserve the amount of calls to the server since I'm limited....
        tweets['geocodedat'][i] = reverseGeocode(str(meancoord[i][1]) + ',' + \
                                  str(meancoord[i][0]))
        #some geolocating returns blank...why?...omit them
        if len(tweets['geocodedat'][i]) != 0:
            for info in tweets['geocodedat'][i]['address_components']:
                if info['types'][0] == 'administrative_area_level_1':
                    tweets['state'][i] = info['short_name']
                    print '......found a state! ', tweets['state'][i]
        else: tweets['state'][i] = None
#import and deal with sentiment data into workable format...
scores = {} # initialize an empty dictionary
afinnfile = open(sentiments)
#The file is tab-delimited. "\t" means "tab character"
for line in afinnfile:
    term, score  = line.split("\t")
    scores[term] = int(score)
#but only the american tweets...no need to bother with foreign ones
print 'len(twscore)', len(tweets)
twscore = []
val = 0
i = 0
for tweet in tweets['text']:
    for key in scores:
        val2 = tweet.find(key)
        if val2 != -1: val += scores[key]
    twscore.append(val)
    if tweets['state'][i] in states:
        states[tweets['state'][i]] += val
        statescounter[tweets['state'][i]] += 1
    val = 0
    i += 1
print 'len(twscore)', len(twscore)

#convert dictionary to pandas datafram
for item in states:
    if statescounter[item] != 0:
        states[item] = float(states[item])/float(statescounter[item])
#weighted by tweet count
result = pd.DataFrame(states.items(), columns=['state', 'rawscore'])
result['counts'] = ''
for i in range(len(result['state'])):
    result['counts'][i] = statescounter[result['state'][i]]

#----------------------------------------------
py.sign_in('dattienhoang', '08xhph2kx4')
df = result
for col in df.columns:
    df[col] = df[col].astype(str)
scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'], \
        [0.4, 'rgb(188,189,220)'], [0.6, 'rgb(158,154,200)'], \
        [0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
#text to display upon hovering
df['text'] = df['state'] + '<br>' +\
    'Average Sentiment Score '+df['rawscore']+'<br>'+\
    'Tweet Count '+df['counts']+'<br>'#+\
    #'Raw Sentiment Score '+df['rawscore']*df['counts']
data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = True,#False,
        locations = df['state'],
        z = df['rawscore'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = dict(
            title = "Sentiment"
        ),
        zmin = -1.5,
        zmax = 1.5
    ) ]
layout = dict(
        title = 'Socialism Sentiments in the United States 2016-02-01',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        ),
    )
fig = dict( data=data, layout=layout )
url = py.plot( fig, filename='socsent-cloropleth-map_2' )

print 'END read_twitter_stream.py'
