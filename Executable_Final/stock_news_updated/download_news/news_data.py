from bs4 import BeautifulSoup as BS
import requests as req
import pandas as pd

def news_download(url):
    date = []
    heading = []
    text = []

    response = req.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BS(response.text, 'html.parser')

    # Find all the <div> elements with class "widget-listing"
    listing_divs = soup.find_all('li', class_='clearfix')

    for div in listing_divs:
        date.append( div.find('span').text.strip() )

        # Extract the heading
        heading.append(div.find('h2').find('a').text.strip() )

        # Extract the text
        text.append(div.find('p').text.strip() )

    df = pd.DataFrame(
        {'date': date,
         'heading': heading,
         'text': text
        })
    return df

def news_df(config):
    final_news = pd.DataFrame()
    missing = []
    for i in config["stock_url"]:
        link = config["stock_url"][i]
        # print( link)
        try:
            df = news_download(link)
            print(df)
            df["SourceTag"] = i
            final_news = pd.concat([final_news, df])
            print(link)

        except:
            missing.append(link)

    return final_news, missing


