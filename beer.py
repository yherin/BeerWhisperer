from __future__ import annotations
from typing import Tuple
import pandas as pd
import pickle
from scipy import spatial

ret_columns_rec = ('Numero', 'EAN', 'name', 'country_EN', 'taste_desc', 'avg_sim', 'weighted_avg', 'taste_sim',
                   'feel_sim', 'col_sim', 'country_sim', 'foods_sim', 'litre_price') 
ret_columns = ('Numero', 'EAN', 'name', 'price', 'alcohol_%', 'litre_price',
               'country_EN', 'taste_desc', 'beer_type', 'calories', 'gravity', 'bitterness_EBU',)


def get_beer(ean: int):
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    beer = beers.loc[beers['EAN'] == ean]

    output = beer.loc[:, ret_columns].to_json(orient='records')
    return output


def get_all_beers():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    output = beers.loc[:, ret_columns].to_json(orient='records')
    return output


def get_recommendations(ean: int, param_taste: float = 1.0, param_price: float = 1.0, n: int = 10):
    # Get recommendations by product EAN, options (non-important 0.5, neutral 1, important 1.5) that will effect the vectors
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))

    # foodVector to be added
    selectedBeer = beers[beers['EAN'] == ean]
    groundVect_taste = selectedBeer.taste_vect.values[0]
    groundVect_color = selectedBeer.col_vect.values[0]
    groundVect_feel = selectedBeer.feel_vect.values[0]
    groundVect_foods = selectedBeer.foods_vect.values[0]
    groundVect_country = selectedBeer.country_vect.values[0]

    weights = {
        'taste': 0.4,
        'color': 0.1,
        'feel': 0.2,
        'country': 0.1,
        'foods': 0.2,
    }
    
    compareBeers = beers.loc[:, ('Numero', 'name', 'litre_price', 'EAN', 'country_EN',
                                 'taste_desc', 'taste_vect', 'col_vect', 'feel_vect', 'foods_vect')]
    compareBeers['taste_sim'] = beers.loc[:, ('taste_vect')].apply(
        lambda x: cosine_sim(groundVect_taste, x))
    compareBeers['col_sim'] = beers.loc[:, ('col_vect')].apply(
        lambda x: cosine_sim(groundVect_color, x))
    compareBeers['feel_sim'] = beers.loc[:, ('feel_vect')].apply(
        lambda x: cosine_sim(groundVect_feel, x))
    compareBeers['foods_sim'] = beers.loc[:, ('foods_vect')].apply(
        lambda x: cosine_sim(groundVect_foods, x))
    compareBeers['country_sim'] = beers.loc[:, ('country_vect')].apply(
        lambda x: cosine_sim(groundVect_country, x))
    compareBeers['avg_sim'] = compareBeers[['taste_sim',
                                            'col_sim', 'feel_sim', 'foods_sim']].sum(axis=1)/4

    if param_taste != 1:
        temp = weights['taste']
        weights['taste'] = weights['taste']*param_taste
        temp = weights['taste'] - temp
        weights['feel'] = weights['feel'] - temp/3
        weights['color'] = weights['color'] - temp/3
        weights['foods'] = weights['foods'] - temp/3

    # Lower the value, the more similar price per litre
    # param_price 1 / no parameters returns full list
    if param_price != 1:
        price = selectedBeer['litre_price'].values[0]
        lower = price - 5 * param_price
        higher = price + 5 * param_price
        compareBeers = compareBeers[compareBeers['litre_price'].between(
            lower, higher)]

    compareBeers['taste_sim_W'] = compareBeers['taste_sim'] * weights['taste']
    compareBeers['col_sim_W'] = compareBeers['col_sim'] * weights['color']
    compareBeers['feel_sim_W'] = compareBeers['feel_sim'] * weights['feel']
    compareBeers['foods_sim_W'] = compareBeers['foods_sim'] * weights['foods']
    compareBeers['country_sim_W'] = compareBeers['country_sim'] * weights['country']
    compareBeers['weighted_avg'] = compareBeers[['taste_sim_W', 'col_sim_W',
                                                 'feel_sim_W', 'foods_sim_W', 'country_sim_W']].sum(axis=1)

    compareBeers = compareBeers.sort_values(
        by=['weighted_avg', 'taste_sim'], ascending=False).reset_index(drop=True)

    # beer at index 0 is always the beer we are matching against, so 1:n
    return compareBeers.loc[1:n, ret_columns_rec].to_json(orient='records', indent=4)

def print_headers():
    # Only used for debugging
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    for entry in beers:
        print(entry)


def get_random_by_category(cat):
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    beer = beers.loc[beers['beer_type'] == cat]
    return beers.sample().loc[:, ret_columns].to_json(orient='records')


def get_random():
    beers = pickle.load(open('dataframe/model_df_v2.bin', 'rb'))
    random = beers.sample().loc[:, ret_columns].to_json(orient='records')
    return random


def cosine_sim(a, b):
    return 1 - spatial.distance.cosine(a, b)


def similarity(a, b):
    return 1-(abs(a-b))

