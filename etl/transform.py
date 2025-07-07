import re
from datetime import datetime

import nltk
import pandas as pd
import structlog
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from tqdm import tqdm

from config.config import load_yaml_config
from utilities import save_posts_to_csv

# Ensure necessary NLTK resources are downloaded
# Uncomment the following lines if you need to download NLTK data files
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# nltk.download('punkt', quiet=True, download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('punkt_tab', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('wordnet', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('omw-1.4', download_dir='/Users/michaelhammond/Documents/GitHub/tweetsent_env/nltk_data')
# nltk.download('averaged_perceptron_tagger_eng')


class RedditTransformer:
    """
    Class to transform raw Reddit data into a structured format.
    """

    def __init__(self):
        self.logger = structlog.get_logger()
        self.logger = self.logger.bind(module="transform")
        self.current_datetime = datetime.now()

    def text_cleanup(self, df) -> pd.DataFrame:
        """
        Perform basic text cleaning on the DataFrame.
        :param df: Pandas DataFrame containing Reddit post data.
        :return: DataFrame with cleaned text data.
        """

        self.logger.info("Starting Data Cleaning")

        # Perform necessary transformations
        df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")

        # Clean each title with a progress bar
        tqdm.pandas(desc="Cleaning text data")
        df["cleaned_title"] = df["title"].progress_apply(
            lambda x: re.sub(
                r"\s+",
                " ",
                re.sub(
                    r"[^\w\s]",
                    "",
                    re.sub(r"http\S+|www\S+|https\S+", "", x.lower().strip()),
                ),
            )
        )

        return df

    def fix_typos(self, df) -> pd.DataFrame:
        """
        Fix common typos in the DataFrame.

        :param
        df: Pandas DataFrame containing text data.
        :return: DataFrame with fixed typos.
        """
        tqdm.pandas(desc="Fixing Typos")
        df["cleaned_title"] = df["cleaned_title"].progress_apply(
            lambda x: str(TextBlob(x).correct())
        )
        return df

    def tokenization(self, df) -> pd.DataFrame:
        """
        Tokenizes the text data in the DataFrame.

        :param
        df: Pandas DataFrame containing text data.
        :return: DataFrame with tokenized text.
        """

        keepwords = load_yaml_config("keep_words")

        default_stopwords = set(stopwords.words("english"))
        stopwords_combined = default_stopwords - set(keepwords)

        tqdm.pandas(desc="Tokenizing text data")
        df["tokens"] = df["cleaned_title"].progress_apply(
            lambda x: [
                word for word in word_tokenize(x) if word not in stopwords_combined
            ]
        )

        return df

    def get_wordnet_pos(self, treebank_tag):
        """
        Convert Treebank POS tags to WordNet POS tags.
        :param treebank_tag: POS tag in Treebank format.
        :return: POS tag in WordNet format.
        """

        if treebank_tag.startswith("J"):
            return wordnet.ADJ
        elif treebank_tag.startswith("V"):
            return wordnet.VERB
        elif treebank_tag.startswith("N"):
            return wordnet.NOUN
        elif treebank_tag.startswith("R"):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lemmatization(self, df) -> pd.DataFrame:
        """
        Lemmatizes the tokens in the DataFrame.

        :param df: Pandas DataFrame containing tokenized text data.
        :return: DataFrame with lemmatized tokens.
        """
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))

        def lemmatize_row(tokens):
            tagged = pos_tag(tokens)
            return [
                lemmatizer.lemmatize(word, pos=self.get_wordnet_pos(tag))
                for word, tag in tagged
            ]

        tqdm.pandas(desc="Lemmatizing tokens")
        df["lemmatized_tokens"] = df["tokens"].progress_apply(lemmatize_row)
        df.drop(columns=["tokens"], inplace=True)
        return df

    def transform_data(self, df, save_to_csv=True):
        """
        Transforms raw Reddit data into a structured DataFrame.

        :param raw_data: List of dictionaries containing raw Reddit post data.
        :return: Pandas DataFrame with transformed data.
        """

        df = self.text_cleanup(df)
        df = self.fix_typos(df)
        df = self.tokenization(df)
        df = self.lemmatization(df)

        # Save to CSV if requested
        if save_to_csv:
            filename = save_posts_to_csv(
                df, current_datetime=self.current_datetime, filename="transformed"
            )

        return df
