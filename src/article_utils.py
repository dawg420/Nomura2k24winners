import requests

def get_article_text(url):
    response = requests.get(url)
    return response.text

def extract_stocks_from_response(response):
    # Implement your logic to extract stocks from LLM response
    pass
