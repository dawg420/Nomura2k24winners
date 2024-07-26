from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai

load_dotenv()

# Initialize OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')
def initialize_llm(api_key=openai_api_key):
    openai.api_key = api_key
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm

# Function to filter URLs using LangChain with OpenAI
def filter_urls_with_langchain(stock: str, articles: dict):
    llm = initialize_llm(openai_api_key)
    article_list = "\n".join([f"{title}: {url}" for title, url in articles.items()])
    prompt = f'''Here is a list of article titles and their URLs related to {stock}'s ESG performance:
    "{article_list}"

    Please select the top 5 URLs that are most likely to contain detailed and relevant information about the specific stock's environmental, social, and governance performance. Provide the output as a plain list of URLs without any numbers or bullet points, one title per line.
    '''
    response = llm.invoke(prompt, max_tokens=1024, stop=None)
    response = response.content
    print(response)
    # Extract URLs from the LLM response
    filtered_urls = [line.strip() for line in response.split('\n') if line.startswith('http')]
    return filtered_urls[:5]