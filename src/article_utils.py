import json
import requests
import requests
import os
from dotenv import load_dotenv
from llm_utils import filter_urls_with_langchain

load_dotenv()
# Function to perform Google Search
def google_search(query, num_results=10):
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    api_url = f"https://www.googleapis.com/customsearch/v1"

    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': num_results
    }
    response = requests.get(api_url, params=params)
    results = response.json().get('items', [])
    
    articles = {result['title']: result['link'] for result in results}
    return articles

# Function to get article URLs from Google Search
def get_article_urls_from_search(stock: str):
    query = f"{stock} ESG performance OR {stock} environmental performance OR {stock} social performance OR {stock} governance performance OR {stock} sustainability report OR {stock} environmental report"
    articles = google_search(query)
    print(f'articles: {articles}')
    filtered_urls = filter_urls_with_langchain(stock, articles)
    print(f'filtered urls: {filtered_urls}')
    return filtered_urls
