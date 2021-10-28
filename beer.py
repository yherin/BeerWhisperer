from __future__ import annotations
from typing import Tuple
import pandas as pd
import pickle
import numpy as np
from scipy import spatial
import sklearn as skl
import os
import json
import fasttext
import fasttext.util
import string
import math

def get_beer(ean: int):
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    beer = beers.loc[beers['EAN'] == ean]
    #Drop unnecessary columns TODO
    #beers.drop(columns=[''])

    output = beer.to_json(orient = "table")
    return output


def get_all_beers():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    #Drop unnecessary columns TODO
    #beers.drop(columns=[''])
    output = beers.to_json(orient = "table")
    return output


def get_recommendations(ean: int, taste: float = 0.6, color: float = 0.05, feel: float = 0.05, price: float = 0.1, country: float = 0.05, food: float = 0.15, n: int = 5):
    #Get recommendations by product EAN, 3 options (non-important, neutral, important) that will effect the vectors
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    
    scores_taste = {}
    scores_feel = {}
    scores_color = {}
    scores_avg = {}
    errors = 0
    success = 0
    
    #foodVector to be added
    groundVect_taste = beers[beers['EAN'] == ean].taste_vect.values[0]
    groundVect_color = beers[beers['EAN'] == ean].col_vect.values[0]
    groundVect_feel = beers[beers['EAN'] == ean].feel_vect.values[0]

    for b in beers.iterrows():
        compareVect_taste = b[1].taste_vect
        compareVect_color = b[1].col_vect
        compareVect_feel = b[1].feel_vect
        compare_id = b[1].Numero

        try:
            scores_taste[compare_id] = ((1 - spatial.distance.cosine(groundVect_taste, compareVect_taste)))
            scores_color[compare_id] = ((1 - spatial.distance.cosine(groundVect_color, compareVect_color)))
            scores_feel[compare_id] = ((1 - spatial.distance.cosine(groundVect_feel, compareVect_feel)))
            scores_avg[compare_id] = taste * scores_taste[compare_id] + color * scores_color[compare_id] + feel * scores_feel[compare_id]
            success += 1
        except ValueError as e:
            errors += 1
    if errors > 0:
        print(f'{errors} errors')
    errors = 0

    sorted_avg = sorted(scores_avg.items(), key=lambda item: item[1])
    sorted_avg.reverse()

    #AVG scores ARE NOT within 0 to 1 range, but other scores are. Recommended to give "Top 10" and for each
    #Rank X
    #Taste score XX%
    #Color score XX% ...


    #ATM returns only sorted list by avg score
    #TODO combine results into JSON
    return sorted_avg[:n]

def print_headers():
    #Only used for debugging
      beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
      for entry in beers:
          print(entry)

def get_random_by_category(cat):
    #TODO
    #Subcategories are missing from dataframe
    return

def get_random():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    #Drop unnecessary columns TODO
    #beers.drop(columns=[''])
    random = beers.sample().to_json
    return random


#get_all_beers()
#print(get_beer(5425007658859))
#print_headers()
#print(get_recommendations(5425007658859, taste=2, country=0.2))
#get_random()
