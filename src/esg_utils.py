from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from llm_utils import initialize_llm

ESG_PROMPT = """
You are a helpful assistant. I need detailed information about the ESG (Environmental, Social, Governance) risk ratings for a specific company, according to the information provided below. Provide the scores in the following JSON format, including a final combined ESG risk rating which is the sum of the individual risk ratings.
The company I am interested in is {company_name}.

Here are the retrieved info: {retrieved_information}

Format:
{{
    "company": "Company Name",
    "environmental_risk": 0-15,
    "social_risk": 0-15,
    "governance_risk": 0-15,
    "final_esg_risk": 0-45
}}
Guidelines for Risk Levels (do not include in JSON):

0-5: "Low Risk" - Indicates low environmental/social/governance risk.
6-10: "Medium Risk" - Indicates medium environmental risk.
11-15: "High Risk" - Indicates high environmental risk.

Final ESG Risk:
Sum of the environmental, social, and governance risk ratings.
Please ensure the JSON output is correctly formatted.
"""

class ESGRAG:
    def __init__(self, prompt_template, company_name):
        self.prompt_template = prompt_template
        self.company_name = company_name
        self.vectorstore = None

    def index_documents(self, documents_list):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = []

        # Split each document and convert splits to Document objects
        for document in documents_list:
            splits = text_splitter.split_text(document)
            documents.extend([Document(page_content=split) for split in splits])
        
        # Initialize Chroma vector store with document chunks
        self.vectorstore = Chroma.from_documents(documents=documents, embedding=OpenAIEmbeddings())

    def retrieve_and_generate(self, query):
        if self.vectorstore is None:
            raise ValueError("The vector store is not initialized. Please index documents first.")

        retriever = self.vectorstore.as_retriever()
        
        # Retrieve relevant snippets
        retrieved_docs = retriever.get_relevant_documents(query)
        formatted_docs = self.format_docs(retrieved_docs)
        
        combined_retrieved_info = formatted_docs + "\n\n"
        
        # Generate response using OpenAI
        llm = initialize_llm()
        prompt = self.prompt_template.format(retrieved_information=combined_retrieved_info, company_name=self.company_name)
        
        response = llm.invoke(prompt, max_tokens=4096, stop=None)
        return response

    def format_docs(self, docs):
        # Implement your formatting logic here
        formatted_docs = "\n".join([doc.page_content for doc in docs])
        return formatted_docs
    
    