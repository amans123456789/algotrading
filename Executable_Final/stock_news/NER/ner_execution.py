import logging
from NER.ner import ner_detection
import en_core_web_sm
from NER.sentiment import sentiment_detection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nlp = en_core_web_sm.load()

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



