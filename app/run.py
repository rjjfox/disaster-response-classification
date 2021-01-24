import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
import joblib
from sqlalchemy import create_engine

# from app.plots import return_figures


app = Flask(__name__)


def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def return_figures(df):
    """Create Plotly figures object"""

    genres_plot = []
    genres_plot.append(
        go.Bar(
            x=df.genre.value_counts().index.tolist(),
            y=df.genre.value_counts().values.tolist(),
            hoverinfo="skip",
            marker_color="#BB764B",
        )
    )

    genres_layout = dict(
        {
            "title": {
                "text": "<b>Majority of messages come directly or via "
                "news</b><br>Small percentage of the data comes"
                " from social",
                "font": {"family": "Roboto", "size": 16},
            },
        }
    )

    label_tallies = df.iloc[:, 4:].sum().sort_values(ascending=True)
    label_plot = []
    label_plot.append(
        go.Bar(
            x=label_tallies.values.tolist(),
            y=label_tallies.index.tolist(),
            orientation="h",
            marker_color="#BB764B",
        )
    )

    label_layout = dict(
        {
            "title": {
                "text": "<b>Not all messages are relevant"
                "</b><br>75% of messages labelled <i>related</i> to mean"
                " relevant",
                "font": {"family": "Roboto", "size": 16},
            },
            "margin": {
                "pad": 10,
                "l": 140,
                "r": 40,
                "t": 80,
                "b": 40,
            },
            "hoverlabel": {
                "font_size": 18,
                "font_family": "Roboto",
            },
            "yaxis": {"dtick": 1},
        }
    )

    figures = []
    figures.append(dict(data=genres_plot, layout=genres_layout))
    figures.append(dict(data=label_plot, layout=label_layout))

    return figures


# load data
engine = create_engine("sqlite:///data/DisasterResponse.db")
df = pd.read_sql_table("messages", engine)

# load model
model = joblib.load("models/classifier.pkl")

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
        "master.html", ids=ids, graphJSON=graphJSON, sample_messages=sample_messages
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