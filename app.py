from flask import Flask, request
import pickle
import json
import beer as bw

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
