import pandas as pd
import os
import logging
import en_core_web_sm


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nlp = en_core_web_sm.load()

def ner_detection(df, column):
    fin = []
    for i in range(len(df)):
        res = []
        ner_row = df[column][i]
        try:
            class_doc = nlp(ner_row)
            for ent in class_doc.ents:
                res.append(ent.text)
            fin.append(res)
        except:
            fin.append("missing")
    return fin


