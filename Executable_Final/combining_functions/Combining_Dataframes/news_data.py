import pandas as pd
import ast
from datetime import datetime, timedelta


columns_to_search = ['heading', 'text']
columns_to_add = ['date','heading', 'text','SourceTag','Text NER', 'Heading NER', 'Text Sentiment','Heading Sentiment']

def search_words(df, word_dict, columns):
    result_df = pd.DataFrame(columns=['Word', 'MatchingRow'])

    for category, words in word_dict.items():
        for word in words:
            # Check if the word is present in any of the specified columns
            mask = df[columns].apply(lambda row: any(word.lower() in str(cell).lower() for cell in row), axis=1)

            # If the word is found, append the corresponding rows to the result dataframe
            if mask.any():
                matching_rows = df[mask].copy()
                matching_rows['Word'] = word
                result_df = result_df.append(matching_rows[['Word', *columns]], ignore_index=True)

    return result_df

def news_df_create(news, keyword_mapping):
    result_df = pd.DataFrame(columns=['Word', 'Category'])
    for category, words in keyword_mapping.items():
        for word in words:
            mask = news[columns_to_search].apply(lambda row: any(word.lower() in str(cell).lower() for cell in row),
                                                 axis=1)
            if mask.any():
                matching_rows = news[mask].copy()
                matching_rows['Word'] = word
                matching_rows['Category'] = category

                # result_df = result_df.append(matching_rows[['Word', 'Category', *columns_to_add]], ignore_index=True)
                result_df = pd.concat([result_df, matching_rows[['Word', 'Category'] + columns_to_add]], ignore_index=True)

    return result_df

def sentiment_columns(row):
    sentiment_scores_a = ast.literal_eval(row['Text Sentiment'])
    sentiment_scores_b = ast.literal_eval(row['Heading Sentiment'])
    if (sentiment_scores_a['positive'] > 0.8)   or ( sentiment_scores_b['positive'] > 0.8):
        return 2
    if  (sentiment_scores_a['negative'] > 0.8) or ( sentiment_scores_b['negative'] > 0.8):
        return -2
    if (sentiment_scores_a['positive'] > 0.6)   or ( sentiment_scores_b['positive'] > 0.6):
        return 1
    if  (sentiment_scores_a['negative'] > 0.6) or ( sentiment_scores_b['negative'] > 0.6):
        return -1

    else:
        return 0

def grading_sentiment(result_df):
    result_df['Sentiment Rating'] = result_df.apply(sentiment_columns, axis=1)

    result_df['date'] = pd.to_datetime(result_df['date'], format='%B %d, %Y %I:%M %p IST')
    result_df['date_ymd'] = result_df['date'].dt.strftime('%Y-%m-%d')

    today = datetime.now()
    seven_days_ago = today - timedelta(days=90)

    filtered_df = result_df[result_df['date_ymd'] >= seven_days_ago.strftime('%Y-%m-%d')]


    fin_news = filtered_df.groupby('Category').agg({
        'date_ymd': 'first',
        'heading': lambda x: ' : '.join(x),
        'text': lambda x: ' : '.join(x),
        'SourceTag': lambda x: ' : '.join(x),
        'Text NER': lambda x: ' : '.join([' '.join(ner) for ner in x]),
        'Heading NER': lambda x: ' : '.join([' '.join(ner) for ner in x]),
        'Text Sentiment': lambda x: ' : '.join([' '.join(ner) for ner in x]),
        'Heading Sentiment': lambda x: ' : '.join([' '.join(ner) for ner in x]),
        'Sentiment Rating': lambda x: ' : '.join(map(str, x)),

    }).reset_index()

    return fin_news

def get_most_extreme_sentiment(sentiments):
    sentiment_values = [int(value) for value in sentiments.split(':')]
    return max(sentiment_values, key=abs)