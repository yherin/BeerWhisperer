import numpy as np
import pickle
import pandas as pd
import json
from scipy import spatial
from typing import Tuple
import fasttext
import fasttext.util


def get_beer(ean: int):
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    beer = beers.loc[beers['EAN'] == ean]
    output = beer.to_json(orient = "table")
    print(output)
    return output


def get_all_beers():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    output = beers.to_json(orient = "table")
    print(output)
    return output



def get_recommendations(ean: int, taste: float = 1, color: float = 1, feel: float = 1, price: float = 1, country: float = 1, n: int = 25):
    #Get recommendations by product EAN, 3 options (non-important, neutral, important) that will effect the vectors
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    df = beers.reset_index()
    
    #Set weights
    beers['taste_vect'] = taste * beers['taste_vect']
    beers['col_vect'] = color * beers['col_vect']
    beers['feel_vect'] = feel * beers['feel_vect']
    beers['country_vect'] = country * beers['country_vect']
  

    ranking = {}
    errors = 0
    success = 0
    groundVect = beers.loc[beers['EAN'] == ean]
    for b in beers.keys():
        try:
            compareVect = beers[b]
            #print(compareVect.shape, groundVect.shape)
            ranking[b] = ((1 - spatial.distance.cosine(groundVect, compareVect)))
            success += 1
        except ValueError as e:
            #print(f'skipped processing for {b}')
            #print(e)
            errors += 1
    if errors > 0:
        print(f'{errors} errors')
    #print(f'{success} done')
    sorted_list = sorted(ranking.items(), key=lambda item: item[1])
    sorted_list.reverse()

    return sorted_list[:n]



def print_headers():
      beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
      for entry in beers:
          print(entry)

def get_random_by_category(cat):
    return

def get_random():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    random = beers.sample().EAN
    return random

#get_all_beers()
#get_beer(5425007658859)
#print_headers()
get_recommendations(5425007658859, taste=2, country=0.2)
#get_random()
