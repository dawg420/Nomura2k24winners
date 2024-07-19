import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize a session using Amazon Bedrock
session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY_ID"),
    region_name='us-east-1'
)

bedrock_client = session.client('bedrock-runtime')

def llm_invoke(body_dict):
    # Convert the dictionary to a JSON string
    body_json = json.dumps(body_dict)

    # Define the kwargs with the formatted body
    kwargs = {
        "modelId": "meta.llama3-70b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": body_json
    }
    return bedrock_client.invoke_model(**kwargs)