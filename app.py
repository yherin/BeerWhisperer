from os import system
from flask import Flask, request
import pickle
import json

from werkzeug.utils import redirect
import beer as bw
import ean_scanner as cam
import cv2

app = Flask(__name__)
model = pickle.load(open('dataframe/model_df.bin', 'rb'))



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/beer/<ean>")
def get_beer_rec(ean: str) -> str:
    t = request.args.get('taste', default=1.0, type = float)
    p = request.args.get('price', default=1.0, type = float)
    n = request.args.get('n', default=5, type=int)
    return bw.get_recommendations(ean=int(ean),  param_taste=t, param_price=p, n=n)

@app.route("/beers")
def get_all_beers():
    return bw.get_all_beers()

@app.route("/scan")
def scan_ean():
    ean = cam.scan()
    return redirect("/beer/"+ean, code=302)

