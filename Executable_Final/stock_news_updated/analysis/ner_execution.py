import logging
from analysis.ner import ner_detection
import en_core_web_sm
import spacy
from analysis.sentiment import sentiment_detection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nlp = en_core_web_sm.load()
# spacy.cli.download("en_core_web_sm")
# nlp = spacy.load("en_core_web_sm")
def ner_exec(df):
    # news_df = read_latest_csv(folder_name="news_data", csv_prefix="data")

    df["Text NER"] = ner_detection(df, "text")
    df["Heading NER"] = ner_detection(df, "heading")

    return df

def sentiment_exec(df):
    # news_df = read_latest_csv(folder_name="news_data", csv_prefix="data")

    df["Text Sentiment"] = sentiment_detection(df, "text")
    df["Heading Sentiment"] = sentiment_detection(df, "heading")

    return df



