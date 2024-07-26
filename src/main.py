import json
from article_utils import get_article_urls_from_search
from read_news import get_text
from esg_utils import ESGRAG, ESG_PROMPT

def get_stock_values(stock: str):
    article_urls = get_article_urls_from_search(stock)
    articles = []
    for article_url in article_urls:
        print(f'Getting information about article: {article_url}')
        articles += [get_text(article_url)]
    print(f'Extracted articles: {articles}')
    
    rag = ESGRAG(prompt_template=ESG_PROMPT, company_name=stock)
    rag.index_documents(articles)
    query = f"What are the Environmental, Social, and Governmental aspects of stock: {stock}?"
    response = rag.retrieve_and_generate(query)
    
    esg_scores = json.loads(response.content)
    result = {
        "esg_scores": esg_scores,
        "sources": article_urls
    }
    return result
    
    
if __name__ == "__main__":
    print(get_stock_values("BlackRock Inc."))