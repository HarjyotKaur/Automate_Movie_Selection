<h1><img align="right" width="200" height="150" src="img/logo.PNG" alt="logo" /> Movie Selector </h1>

## Introduction

We all have sat for hours endlessly googling to narrow down one movie to go with our tab of popcorn. The time and struggle to make that decision is long and sometimes, consumes more time that the duration of the movie itself.

After, having to face this issue inevitably every week, we decided to automate movie selection. A common pattern for movie selection is viewing the rating,  trailer, genre, casting, popularity and social opinion of the movie. To inculcate these factors we have scraped and formulated rating from various renowned websites.

## Functionality

The code has been compiled to piece together movie rating from four diverse sources:

- [Twitter](https://twitter.com/)   
The twitter API has been used to pull tweet data for a movie. Using tweet data a sentiment score is calculated to formulate a social sentiment score for the movie.

- [IMDB](https://www.imdb.com/)   
The IMDB API has been used to pull the rating for the movie given by users on IMDB.

- [Metacritic](https://www.metacritic.com/)     
The IMDB API has been used to pull the rating for the movie given top critics.

- [Rotten Tomatoes](https://www.rottentomatoes.com/)   
Beautiful Soup has been used to pull the Tomatometer score, it is based on the opinions of hundreds of film and television critics.

The four rating are then aggregated to give an overall score. The four rating chosen factor in multiple opinions about the movie and would help the user to automate this decision.

## Usage

- Clone this repository

`https://github.com/HarjyotKaur/Automate_Movie_Selection.git`

- Fill in the following variables, as they are required to run the code:

  - List of movies you want to select from in `movie_selection.py`

  - List respective year of release of the these movies in `movie_selection.py`. This is done to avoid duplicity of movies that may be caused due to same movie names.

  - Get access tokens for working with Twitter API and fill them in `movie_selection.py`

The section to fill these variables is marked in the script.

#### Example

```
#declaring file path and variables

movies=['Aquaman','Incredibles 2','Game Night']
years=['2018','2018','2018','2018']
path = os.getcwd()+"\\Twitter_Data\\"
maxtweets=100

```
#### Output

```
=================== Aquaman ===================
Pulling Tweets
Fetched100tweets
Fetched Movie Object from IMDB API
=================== Incredibles 2 ===================
Pulling Tweets
Fetched97tweets
tweets exhausted
Fetched Movie Object from IMDB API
=================== Game Night ===================
Pulling Tweets
Fetched100tweets
Fetched Movie Object from IMDB API
```
```
The best overall rating is 4.00 for the movie(s): ['Incredibles 2']
```

|title|year|Sentiment_Score|IMDB_Rating|Metacritic_Rating|Rotten_Tomatoes_Rating|Average_Rating|
|---|---|---|---|---|---|---|
|Aquaman|2018|3.50|3.56|2.75|3.25|3.27|
|Incredibles 2|2018|3.55|3.78|4.00|4.65|4.00|
|Game Night|2018|3.45|3.33|3.30|4.20|3.57|
