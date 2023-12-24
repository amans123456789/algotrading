from config import config
import pandas as pd
import os
from datetime import datetime
import logging
from dateutil import parser


def postproc(df):
    # df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y %I:%M %p %Z')
    df['date_2'] = df['date'].apply(lambda x: parser.parse(x))

    df['year_month'] = df['date_2'].dt.strftime('%Y-%m-%d')

    latest_date = df['year_month'].max()

    latest_date_rows = df[df['year_month'] == latest_date]

    latest_date_rows['Text Sentiment Positive'] = latest_date_rows['Text Sentiment'].apply(lambda x: x['positive'])
    latest_date_rows['Text Sentiment Negative'] = latest_date_rows['Text Sentiment'].apply(lambda x: x['negative'])
    latest_date_rows['Heading Sentiment Positive'] = latest_date_rows['Heading Sentiment'].apply(lambda x: x['positive'])
    latest_date_rows['Heading Sentiment Negative'] = latest_date_rows['Heading Sentiment'].apply(lambda x: x['negative'])

    latest_date_rows["Text Sentiment Positive"] = latest_date_rows["Text Sentiment Positive"].astype(float)
    latest_date_rows["Text Sentiment Negative"] = latest_date_rows["Text Sentiment Negative"].astype(float)
    latest_date_rows["Heading Sentiment Positive"] = latest_date_rows["Heading Sentiment Positive"].astype(float)
    latest_date_rows["Heading Sentiment Negative"] = latest_date_rows["Heading Sentiment Negative"].astype(float)

    filtered_df = latest_date_rows[(latest_date_rows['Text Sentiment Positive'] > 0.7)
                                   | (latest_date_rows['Text Sentiment Negative'] > 0.7 ) | (latest_date_rows['Heading Sentiment Positive'] > 0.7)
                                   | (latest_date_rows['Heading Sentiment Negative'] > 0.7) ]
    filtered_df = filtered_df.drop(["date","date_2", "Text Sentiment", "Heading Sentiment"], axis=1)
    return filtered_df

