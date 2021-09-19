#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 10:03:12 2021

@author: lukas
"""

import pandas as pd
#import numpy as np
import os
import timeit

# start = timeit.default_timer()

# Change working directoy

os.getcwd()

working_directoy = ""

os.chdir(working_directory)

# Get and import files in workingdirectoy

os.listdir()

lukas_netflix = pd.read_csv("NetflixViewingHistory.csv")

start = timeit.default_timer()

def series_titles():
    
    # Import the episode identifier Database
    
    dtype_ep = {"tconst":str, "parentTconst":str, "seasonNumber":float, "episodeNumber":float}

    episode_identifier = pd.read_csv('episode_identifier.tsv', sep = "\t", 
                                 dtype = dtype_ep, na_values = "\\N")

    episode_identifier["seasonNumber"] = episode_identifier["seasonNumber"].astype("Int64")

    episode_identifier["episodeNumber"] = episode_identifier["episodeNumber"].astype("Int64")

    # Import Episode info

    dtype = {"tconst": str, "titleType": str, "originalTitle":str} 

    col_list = ["tconst","titleType", "originalTitle"]

    netflix_titles_info = pd.read_csv('imdb_titles_info.tsv', sep = "\t", dtype = dtype, usecols = col_list)

    # Merge Episode identifier and imdb title information database

    series_titles = pd.merge(episode_identifier, netflix_titles_info, how = "left", on = "tconst")

    series_titles_parent = pd.merge(series_titles, netflix_titles_info,
                                how = "left", left_on = "parentTconst", right_on = "tconst")

    series_titles_parent = series_titles_parent.rename(columns = {"originalTitle_y":"Title",
                                       "originalTitle_x":"Episode_title", "tconst_x":"Id"})
    
    # series_titles_parent = series_titles_parent.rename(columns = {"tconst_episode":"Id"})

    return series_titles_parent[["Id", "Episode_title", "Title"]]

series_titles = series_titles()

def movie_titles():
    
    dtype = {"titleId" : str, "ordering" : int, "title" : str, "region" : str}

    col_list = ["titleId", "ordering", "title", "region"]

    imdb_titles = pd.read_csv('imdb_titles.tsv', sep = "\t", usecols = col_list, dtype = dtype) 

    imdb_us = imdb_titles[imdb_titles.region == "US"]
    
    imdb_us = imdb_us.rename(columns = {"titleId":"Id", "title":"Title"})
    
    return imdb_us[["Id", "Title"]]

movie_titles = movie_titles()

# Get imdb ratings

imdb_ratings = pd.read_csv('imdb_ratings.tsv', sep = "\t")

imdb_ratings = imdb_ratings.rename(columns = {"tconst" : "Id"})

def merge_ratings(database):
    
    return pd.merge(database, imdb_ratings, how = "left", on = "Id").iloc[:,1:]

movie_ratings, series_ratings = merge_ratings(movie_titles), merge_ratings(series_titles)

def merge_movie_ratings():
    
    global movie_ratings
    
    movie_ratings = movie_ratings.groupby("Title").max("numVotes")

    return lukas_netflix.merge(movie_ratings, how = "inner",on="Title")

lukas_netflix_movies = merge_movie_ratings()

# keep only the series in Netflix list

lukas_netflix = lukas_netflix[~lukas_netflix.Title.isin(lukas_netflix_movies.Title)]

# Add episode column

episode_title = str()

lukas_netflix["episode_title"] = episode_title

def change_structure(netflix_data):
    
    for i in range(len(netflix_data)):
        
        text = netflix_data.iloc[i,0]
                
        if text.find(":") != -1:
        
            lukas_netflix.iloc[i,0] = text[0:text.find(":")]
        
            lukas_netflix.iloc[i,2] = text[text.rfind(":")+2:]
    
        else:
        
            lukas_netflix.iloc[i,0] = text        
        
    return netflix_data

lukas_netflix_episodes = change_structure(lukas_netflix)

# Connecting the databases using panda

lukas_netflix_episodes = lukas_netflix_episodes.rename(columns = {"episode_title" : "Episode_title"})

lukas_netflix_episodes = pd.merge(lukas_netflix_episodes, series_ratings, how = "left", on = ["Title","Episode_title"])

stop = timeit.default_timer()

print('Time: ', stop - start)  

#def merge_series_rating():
    
lukas_netflix_movies.averageRating.plot.hist() 

lukas_netflix_series.averageRating.plot.hist() 
   
lukas_netflix_movies.numVotes.plot.hist() 

lukas_netflix_series.numVotes.plot.hist() 

lukas_netflix = lukas_netflix.join(ratings, lsuffix="_left", rsuffix="_right")
