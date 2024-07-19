import json
from src.llm_utils import llm_invoke
from src.esg_utils import get_esg_scores, update_esg_scores
from src.qdrant_utils import get_stock_vector, search_stock_in_qdrant, add_stock_to_qdrant
from src.s3_utils import check_article_processed, mark_article_processed
from src.article_utils import get_article_text, extract_stocks_from_response

def main():
    # Load articles from JSON file
    with open('data/articles.json', 'r') as file:
        articles = json.load(file)

    # Filter articles by category
    business_articles = [article for article in articles if article['category'] == 'business']

    for article in business_articles:
        article_name = article['headline']
        article_url = article['link']

        if check_article_processed(article_name, article_url):
            continue

        article_text = get_article_text(article_url)
        llm_response = llm_invoke({"text": article_text})
        stocks = extract_stocks_from_response(llm_response)

        for stock in stocks:
            # Check if stock is in Qdrant DB
            stock_vector = get_stock_vector(stock)
            existing_stock = search_stock_in_qdrant(stock_vector)

            if existing_stock:
                stock_name = existing_stock['name']
                esg_scores = get_esg_scores(stock_name)
                update_esg_scores(stock_name, esg_scores)
            else:
                esg_scores = get_esg_scores(stock)
                add_stock_to_qdrant(stock, stock_vector, esg_scores)

        mark_article_processed(article_name, article_url)

if __name__ == "__main__":
    main()
