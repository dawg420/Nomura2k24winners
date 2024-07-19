import pandas as pd
import json
import os
import requests
from bs4 import BeautifulSoup

bbc_news = pd.read_csv('./Downloads/Nomura Data/bbc_news.csv')
esg_ratings = pd.read_csv('./Downloads/Nomura Data/SP 500 ESG Risk Ratings.csv')
news_cat = pd.read_json('./Downloads/Nomura Data/News_Category_Dataset_v3.json', lines = True)

bbc_business = bbc_news[bbc_news['link'].apply(lambda x:'business' in x)].reset_index(drop = True)
categories = ['ENVIRONMENT', 'SCIENCE', 'IMPACT', 'GREEN', 'GOOD NEWS']
#news_cat['category'].unique()
huff_news = news_cat.loc[lambda x:x['category'].isin(categories)].reset_index(drop = 1)

def get_huff_content(url):
    # Fetch the web page
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the web page. Status code: {response.status_code}"

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the article content (specific to the website structure)
    # This example is tailored to HuffPost articles
    article = soup.find('section', {'class': 'entry__content-list js-entry-content js-cet-subunit'})
    if not article:
        return "Article content not found."

    # Extract text from the article content
    paragraphs = article.find_all('p')
    article_text = "\n\n".join([p.get_text() for p in paragraphs])

    return article_text

def get_bbc_article_content(url):
    # Fetch the web page
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the web page. Status code: {response.status_code}"

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements where data-component="text-block"
    text_blocks = soup.find_all(attrs={"data-component": "text-block"})
    if not text_blocks:
        return "Article content not found."

    # Extract text from the text blocks
    article_text = "\n\n".join([block.get_text() for block in text_blocks])

    return article_text

bbc_content = [get_bbc_article_content(bbc_business.loc[i, 'link']) for i in len(bbc_business)]
huff_content = [get_huff_content(huff_news.loc[i, 'link']) for i in len(huff_news)]