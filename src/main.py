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

# Initialize the Bedrock client
bedrock_client = session.client('bedrock-runtime')

# Define the query
query = "Where do babies come from?"

# Define the prompt with the query
prompt = f"""You are an AI assistant that answers questions. Maintain a professional and helpful tone. Help the user with this problem: {query}"""

# Create the body dictionary
body_dict = {
    "prompt": prompt,
    "max_gen_len": 512,  # Using a smaller max length for debugging
    "temperature": 0,  # Adjusting temperature for variability
    "top_p": 0.9
}

# Convert the dictionary to a JSON string
body_json = json.dumps(body_dict)

# Define the kwargs with the formatted body
kwargs = {
    "modelId": "meta.llama3-70b-instruct-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": body_json
}

# Print the kwargs for debugging
print("Request Payload:", kwargs)

# Invoke the model
response = bedrock_client.invoke_model(**kwargs)

# Read and print the response
response_body = json.loads(response['body'].read().decode('utf-8'))
print("Response:", response_body)
