from __future__ import annotations
from re import T
from typing import Tuple
import pandas as pd
import pickle
import numpy as np
from scipy import spatial
#import sklearn as skl


weights = {
    'taste': 0.4,
    'color': 0.2,
    #'price': 0.1,
    'feel': 0.2,
    'country': 0.05,
    'foods': 0.15
}

ret_columns = ( 'Numero', 'EAN', 'Nimi', 'country_EN', 'taste_desc','avg_sim','weighted_avg', 'taste_sim', 'feel_sim', 'col_sim', 'country_sim', 'foods_sim', )#need to add Litrahinta and price sim too


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


def get_recommendations(ean: int, param_taste: float = 1.0, param_price: float = 1.0, n: int = 10):
    #Get recommendations by product EAN, options (non-important 0.5, neutral 1, important 1.5) that will effect the vectors
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    

    #foodVector to be added
    selectedBeer = beers[beers['EAN'] == ean]
    groundVect_taste = selectedBeer.taste_vect.values[0] #* weights['taste'] * param_taste
    groundVect_color = selectedBeer.col_vect.values[0] #* weights['color']
    groundVect_feel = selectedBeer.feel_vect.values[0] #* weights['feel']
    groundVect_foods = selectedBeer.foods_vect.values[0] #* weights['foods']
    groundVect_country = selectedBeer.country_vect.values[0] #* weights['country']

    """Currently the weights are applied before the vector similarity is calcuated. The effect of this is super small."""
    compareBeers = beers.loc[:,('Numero', 'Nimi', 'EAN', 'country_EN', 'taste_desc', 'taste_vect', 'col_vect', 'feel_vect', 'foods_vect')]
    compareBeers['taste_sim']       =   beers.loc[:,('taste_vect')].apply(lambda x: cosine_sim(groundVect_taste, x))
    compareBeers['col_sim']         =   beers.loc[:,('col_vect')].apply(lambda x: cosine_sim(groundVect_color, x))
    compareBeers['feel_sim']        =   beers.loc[:,('feel_vect')].apply(lambda x: cosine_sim(groundVect_feel, x))
    compareBeers['foods_sim']     =   beers.loc[:,('foods_vect')].apply(lambda x: cosine_sim(groundVect_foods, x))
    compareBeers['country_sim']   =   beers.loc[:,('country_vect')].apply(lambda x: cosine_sim(groundVect_country, x))
    compareBeers['avg_sim'] = compareBeers[['taste_sim', 'col_sim', 'feel_sim', 'foods_sim']].sum(axis=1)/4
    
    if param_taste != 1:
        temp = weights['taste']
        weights['taste'] = weights['taste']*param_taste
        temp = weights['taste'] - temp
        weights['feel'] = weights['feel'] - temp/3
        weights['color'] = weights['color']- temp/3
        weights['foods'] = weights['foods']- temp/3

    compareBeers['taste_sim_W'] = compareBeers['taste_sim'] * weights['taste'] #* param_taste
    compareBeers['col_sim_W'] = compareBeers['col_sim'] * weights['color'] #/param_taste
    compareBeers['feel_sim_W'] = compareBeers['feel_sim'] * weights['feel'] #* param_taste
    compareBeers['foods_sim_W'] = compareBeers['foods_sim'] * weights['foods'] #/param_taste
    compareBeers['country_sim_W'] = compareBeers['country_sim'] * weights['country']
    compareBeers['weighted_avg'] =   compareBeers[['taste_sim_W', 'col_sim_W', 'feel_sim_W', 'foods_sim_W', 'country_sim_W']].sum(axis=1)

#    for b in beers.iterrows():
#        compareVect_taste = b[1].taste_vect
#        compareVect_color = b[1].col_vect
#        compareVect_feel = b[1].feel_vect
#        compare_id = b[1].Numero
#
#        try:
#            scores_taste[compare_id] = (cosine_sim(groundVect_taste, compareVect_taste))
#            scores_color[compare_id] = (cosine_sim(groundVect_color, compareVect_color))
#            scores_feel[compare_id] = (cosine_sim(groundVect_feel, compareVect_feel))
#            scores_avg[compare_id] = taste * scores_taste[compare_id] + color * scores_color[compare_id] + feel * scores_feel[compare_id]
#            success += 1
#        except ValueError as e:
#            errors += 1
#    if errors > 0:
#        print(f'{errors} errors')
#    errors = 0

#    sorted_avg = sorted(scores_avg.items(), key=lambda item: item[1])
#    sorted_avg.reverse()

    compareBeers = compareBeers.sort_values(by=['weighted_avg', 'taste_sim'], ascending=False).reset_index(drop=True)
    return compareBeers.loc[1:n,ret_columns].to_json(orient='records', indent=4) #beer at index 0 is always the beer we are matching against, so 1:n
    
    #AVG scores ARE NOT within 0 to 1 range, but other scores are. Recommended to give "Top 10" and for each
    #Rank X
    #Taste score XX%
    #Color score XX% ...


    #ATM returns only sorted list by avg score
    #TODO combine results into JSON
    #return sorted_avg[:n]

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


def cosine_sim(a,b):
    return 1 - spatial.distance.cosine(a,b)

#get_all_beers()
#print(get_beer(5425007658859))
#print_headers()
#print(get_recommendations(5425007658859, taste=2, country=0.2))
#get_random()
