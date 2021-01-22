import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """Load and merge the messages and categories"""

    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    return messages.merge(categories, on="id")


def clean_data(df):
    """Split categories into separate columns and drop duplicates"""

    # split the category labels into separate columns
    categories = df.categories.str.split(";", expand=True)

    # extract category labels
    row = categories.loc[0]
    category_colnames = row.apply(lambda x: x.split("-")[0])
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1])

        # convert column from string to numeric
        categories[column] = categories[column].astype("int")

    # clip values to be either a 0 or 1
    categories = categories.clip(0, 1)

    # remove columns with only one value
    one_value_columns = [
        column for column in categories.columns if len(categories[column].unique()) == 1
    ]
    categories = categories.drop(one_value_columns, axis=1)

    # drop original categories column and add encoded features to dataframe
    df = df.drop("categories", axis=1)
    df = pd.concat([df, categories], axis=1)

    # Drop duplicates
    df = df.drop_duplicates()

    return df


def save_data(df, database_filename):
    """Save DataFrame to sqlite database"""

    connect_str = f"sqlite:///{database_filename}"
    engine = create_engine(connect_str)

    df.to_sql("messages", engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print(
            "Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}".format(
                messages_filepath, categories_filepath
            )
        )
        df = load_data(messages_filepath, categories_filepath)

        print("Cleaning data...")
        df = clean_data(df)

        print("Saving data...\n    DATABASE: {}".format(database_filepath))
        save_data(df, database_filepath)

        print("Cleaned data saved to database!")

    else:
        print(
            "Please provide the filepaths of the messages and categories "
            "datasets as the first and second argument respectively, as "
            "well as the filepath of the database to save the cleaned data "
            "to as the third argument. \n\nExample: python process_data.py "
            "disaster_messages.csv disaster_categories.csv "
            "DisasterResponse.db"
        )


if __name__ == "__main__":
    main()