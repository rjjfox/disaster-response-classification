import sys
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
import pickle

from custom_tokenizer import tokenize


def load_data(database_filepath):
    """Load data from SQLite database and parse into features and target variables"""

    connect_str = f"sqlite:///{database_filepath}"
    engine = create_engine(connect_str)
    df = pd.read_sql("SELECT * FROM messages", engine)
    X = df.message
    Y = df.iloc[:, 4:]
    categories = Y.columns.tolist()

    return X, Y, categories


def build_model():
    """Build machine learning pipeline"""

    pipeline = Pipeline(
        [
            (
                "vect",
                CountVectorizer(
                    tokenizer=tokenize,
                    max_df=1.0,
                    max_features=None,
                    ngram_range=(1, 2),
                ),
            ),
            ("tfidf", TfidfTransformer(use_idf=True)),
            (
                "clf",
                MultiOutputClassifier(
                    SGDClassifier(
                        loss="hinge",
                        alpha=0.00005,
                        tol=0.01,
                        n_iter_no_change=5,
                        penalty="l2",
                    )
                ),
            ),
        ]
    )
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """Print classification report for positive labels"""

    y_pred = model.predict(X_test)
    print(classification_report(Y_test, y_pred, target_names=category_names))


def save_model(model, model_filepath):
    """Pickle the model"""

    pickle.dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print("Loading data...\n    DATABASE: {}".format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print("Building model...")
        model = build_model()

        print("Training model...")
        model.fit(X_train, Y_train)

        print("Evaluating model...")
        evaluate_model(model, X_test, Y_test, category_names)

        print("Saving model...\n    MODEL: {}".format(model_filepath))
        save_model(model, model_filepath)

        print("Trained model saved!")

    else:
        print(
            "Please provide the filepath of the disaster messages database "
            "as the first argument and the filepath of the pickle file to "
            "save the model to as the second argument. \n\nExample: python "
            "train_classifier.py ../data/DisasterResponse.db classifier.pkl"
        )


if __name__ == "__main__":
    main()