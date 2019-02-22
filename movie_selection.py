"""
Created on 21 February, 2019

@author: Harjyot Kaur, Ankur Gulati

Implementation of automating movie selection
"""

# load packages
import json
import tweepy
import sys
import jsonpickle
import os
import urllib
import pandas as pd
import re
import requests
import string

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.utils.encoding import smart_str
import imdb as imdb
from bs4 import BeautifulSoup





#function to fetch tweets
def fetch_tweets(movie,path,maxTweets):
    '''
    Fetch tweets for a movie

    Parameters
    ----------
    movie : str
        name of the movie for which tweets have to fetched

    path :  str
        path to store tweet data

    max_Tweets: int
        upper limits of number of tweets to be fetched

    Returns
    -------
    str

        path of the file storing tweet data

    Example
    --------
    >>> path = os.getcwd()+"\\Twitter_Data\\"
    >>> fetch_tweets('Inception',path,100)

    '''

    print ('Pulling Tweets')
    moviepath=movie.replace(' ','')
    file1= path +moviepath+'_tweets.txt'
    file2= path +moviepath+'_text.txt'

    # ccreating query to pull tweets
    query=movie+ ' -collection -boxoffice -ticket -win -contest lang:en since:'
    total= 0
    m= -1
    with open(file1,'w') as f:
        while total<maxTweets:
            try:
                new=twitter_api.search(q=query,since_id=None,count=100, max_id=str(m-1))
                if not new:
                    print("tweets exhausted")
                    break
                with open(file2,'w') as f2:
                    for tweet in new:
                        f2.write(str(tweet.id))
                        f2.write("\n")
                        f.write(jsonpickle.encode(tweet._json,unpicklable=False)+'\n')
                        m=tweet.id
                total+=len(new)
                msg2="Fetched" +str(total) + "tweets"
                print (msg2)
            except tweepy.TweepError as e:
                break
    return file1



def clean(text):

    """
    Remove tickers, special characters, links and numerical strings

    Parameters
    ----------

    text : str

       User given input

    Returns
    -------

    str

        cleaned text


    Examples

    --------

    >>>text="RT $USD @Amila #Test\nTom\'s newly listed Co. &amp; Mary\'s unlisted Group to supply tech for

            nlTK.\nh.. $TSLA $AAPL https://  t.co/x34afsfQsh'"

    >>> clean(text)

    'RT   Amila  TestTom s newly listed Co   amp  Mary s unlisted Group to supply tech for  nlTK h    '

    """

    # remove tickers
    remove_tickers=re.sub(r'\$\w*','',text)

    # remove new line symbol
    remove_newline=re.sub(r'\n','',remove_tickers)

    # remove links
    remove_links=re.sub(r'https?:\/\/.*\/\w*','',remove_newline)

    # remove special characters
    remove_punctuation=re.sub(r'['+string.punctuation+']+', ' ', remove_links)

    # remove numerical strings
    remove_numeric_words=re.sub(r'\b[0-9]+\b\s*', '',remove_punctuation)

    clean_text=remove_numeric_words

    return clean_text



def sentiment_score(movie,file):
    '''
    Fetch tweets for a movie

    Parameters
    ----------
    movie : str
        name of the movie for which tweets have to fetched

    file1 :  str
        path of the file storing tweet data

    Returns
    -------
    float

        sentiment score for the movie

    >>> path = os.getcwd()+"\\Twitter_Data\\"
    >>> fetch_tweets('Inception',path,100)
    >>> sentiment_score('Inception',file)

    4.2

    '''

    tpath=file
    tfile=open(tpath,"r")
    pos=neg=neutral=0
    for l in tfile:
        t=json.loads(l)
        text=clean(t['text'])
        tok1=re.sub(movie,"",text)

        # to avoid retweet redundancy
        if 'RT' not in t['text']:
            sia=SentimentIntensityAnalyzer()
            ss =sia.polarity_scores(tok1)
            op=0
            if ss['compound']>0:
                op=1
                pos+=1
            if ss['compound']<0:
                op=-1
                neg+=1
            if ss['compound']==0:
                neutral+=1
    # calculat sentiment score
    score=round(pos/(pos+neg),2)*5
    return score



def fetch_imdb(imdb_http,movie,year):
    '''
    Fetch imdb object for a movie

    Parameters
    ----------
    imdb_http : object
       an imdb object

    movie : str
        name of the movie

    year: str
        year the movie was released

    Returns
    -------
    object

        an imdb movie object {imdb.Movie.Movie}

    Example
    --------
    >>> imdb_http = imdb.IMDb()
    >>> fetch_imdb(imdb_http,'Inception','2010')

    Fetched Movie Object from IMDB API

    <Movie id:1375666[http] title:_Inception (2010)_>

    '''
    # searching movies matching query
    movie_list =imdb_http.search_movie(movie)

    # using movie name and title to find exact match
    movie_data = [i for i in movie_list
           if i.data['kind'] == 'movie' and
              i.data['title'] == movie and
              str(i.data['year']) == year]

    if len(movie_data)!=0:
        print("Fetched Movie Object from IMDB API")
        imdb_http.update(movie_data[0])
        return movie_data[0]

    else:
        print("Movie not found in IMDB")
        return ""



def imdb_score(movie):
    '''
    Fetch imdb rating for the movie

    Parameters
    ----------

    movie : object

        an imdb movie object {imdb.Movie.Movie}

    Returns
    -------
    float

        imdb score for the movie

    Example
    --------
    >>> imdb_http = imdb.IMDb()
    >>> imdb_score(fetch_imdb(imdb_http,'Inception','2010'))

    4.33

    '''
    # IMDb: augment movie info
    imdb_score=round(((movie.data['rating'] - 1) / 9.0) * 5,2)
    return imdb_score

def metacritic_score(imdb_http,movie):
    '''
    Fetch metacritic rating for the movie

    Parameters
    ----------

    movie : object

        an imdb movie object {imdb.Movie.Movie}

    Returns
    -------
    float

        metacritic score for the movie

    Example
    --------
    >>> imdb_http = imdb.IMDb()
    >>> metacritic_score(imdb_http,fetch_imdb(imdb_http,'Inception','2010'))

    3.7

    '''

     # meta critic
    x = imdb_http.get_movie_critic_reviews(movie.movieID)

    metacritic_score=round(int(x['data']['metascore']) / 20.0,2)
    return metacritic_score


def rotten_tomatoes_score(movie):
    '''
    Fetch rotten tomatoes rating for the movie

    Parameters
    ----------

    movie : object

        an imdb movie object {imdb.Movie.Movie}

    Returns
    -------
    float

        rotten tomatoes score for the movie

    Example
    --------
    >>>imdb_http = imdb.IMDb()
    >>> rotten_tomatoes_score(fetch_imdb(imdb_http,'Inception','2010'))

    4.3

    '''

    # creating query for rotten tomatoes
    tomato_base_url = 'https://www.rottentomatoes.com/m/'
    tomato_url = tomato_base_url + re.sub(':', '', re.sub(' ', '_', str(movie.data['title'])))

    # scraping rotten tomatoes
    soup = BeautifulSoup(requests.get(tomato_url).text,"lxml")  # rotten tomatoes: website parse tree
    rotten_tomatoes_score=int(min(soup.find('span', {'class': 'meter-value superPageFontColor'}).contents[0])) / 20.0
    return rotten_tomatoes_score


# twitter API keys
# to get access token visit
# https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html

#------------------the access tokens are required to run the code-------------------------#

ACCESS_TOKEN = ""
ACCESS_TOK_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET=""
authorization = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = tweepy.API(authorization, wait_on_rate_limit=True)
if(not twitter_api):
    print("Authentication error")
    sys.exit(-1)

#declaring file path and variables

#------------------the variables below are required to run the code-------------------------#
movies=[]
years=[]
path = os.getcwd()+"\\Twitter_Data\\"
maxtweets=100



compiled_scores = pd.DataFrame(columns=['title','year', 'Sentiment_Score','IMDB_Rating', 'Metacritic_Rating','Rotten_Tomatoes_Rating','Average_Rating'])
for i in range(0,len(movies)):
    # IMDb: augment movie info
    print("===================",movies[i],"===================")
    tweets=fetch_tweets(movies[i],path,maxtweets)

    imdb_http = imdb.IMDb()
    movie_obj=fetch_imdb(imdb_http,movies[i],years[i])

    score1=sentiment_score(movies[i],tweets)
    score2=imdb_score(movie_obj)
    score3=metacritic_score(imdb_http,movie_obj)
    score4=rotten_tomatoes_score(movie_obj)
    avg_score=round((score1+score2+score3+score4)/4,2)
    scores=[movies[i],years[i],score1,score2,score3,score4,avg_score]
    compiled_scores.loc[i]=scores


print ("The best overall rating is", max(compiled_scores['Average_Rating']),"for the movie(s):",list(compiled_scores['title'][compiled_scores['Average_Rating']==max(compiled_scores['Average_Rating'])]))
print(compiled_scores)
