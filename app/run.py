import sys
from flask import Flask
from flask import render_template, request
import joblib
from sqlalchemy import create_engine

import pandas as pd
import json
import plotly

# import custom py files
from plots import return_figures

# append paths to reach cousin folder on local and cloud deploys
sys.path.append("C:/Users/ryanf/Projects/DisasterResponsePipeline/models")
sys.path.append("/home/ryanfox212/disaster-response-classification/models")
from custom_tokenizer import tokenize


app = Flask(__name__)


# try/except to work both for local builds and cloud deployment
try:
    # load data from database
    engine = create_engine("sqlite:///data/DisasterResponse.db")
    df = pd.read_sql_table("messages", engine)

    # load model from pickle file
    model = joblib.load("models/classifier.pkl")
except:
    # PythonAnywhere directories
    engine = create_engine(
        "sqlite:////home/ryanfox212/disaster-response-classification/data/DisasterResponse.db"
    )
    df = pd.read_sql_table("messages", engine)
    model = joblib.load(
        "/home/ryanfox212/disaster-response-classification/models/classifier.pkl"
    )


# index webpage displays cool visuals and receives user input text for model
@app.route("/")
@app.route("/index")
def index():

    figures = return_figures(df)

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(figures)]
    graphJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    messages_df = df[["message", "genre"]].copy()
    messages_df["shortened"] = messages_df.message.str[:250]
    sample_messages = messages_df.sample(3).values

    # render web page with plotly graphs
    return render_template(
        "master.html",
        ids=ids,
        graphJSON=graphJSON,
        sample_messages=sample_messages,
    )


# web page that handles user query and displays model results
@app.route("/go")
def go():
    # save user input in query
    query = request.args.get("query", "")

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file.
    return render_template(
        "go.html", query=query, classification_result=classification_results
    )


def main():
    app.run(host="0.0.0.0", port=3001, debug=True)


if __name__ == "__main__":
    main()