from flask import Flask
import pickle
import json

app = Flask(__name__)
model = pickle.load(open('dataframe/model_df.bin', 'rb'))



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/beer/<id>")
#just some junk for testing
def get_beer_rec(id: str) -> str:
    ret = {}
    ret["beer"] = id
    ret["recommendations"] = str(list(model.index[:5]))
    return json.dumps(ret)
