# Script saves issues with AttributeErrors
# https://www.stefaanlippens.net/python-pickling-and-dealing-with-attributeerror-module-object-has-no-attribute-thing.html
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def tokenize(text):
    "Extract features from text"

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens