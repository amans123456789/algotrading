import pandas as pd
import os
import logging
import eng_spacysentiment
from analysis.ner import ner_detection

sent = eng_spacysentiment.load()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def sentiment_detection(df, column):
    fin = []
    for i in range(len(df)):
        # res = []
        sentiment_row = df[column][i]
        try:
            class_doc = sent(sentiment_row)
            fin.append(class_doc.cats)
        except:
            fin.append("missing")
    return fin

