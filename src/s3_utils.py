import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_ID'),
    region_name='us-east-1'
)


def get_processed_article_names(bucket_name, folder_name):
     # List objects in the specified bucket and folder
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    processed_names = []

    # Check if 'Contents' is in the response
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            # Use split to remove 'folder_name' prefix and '.txt' suffix
            if key.startswith(folder_name) and key.endswith('.txt'):
                processed_name = key.split(folder_name, 1)[1].rsplit('.txt', 1)[0]
                processed_names.append(processed_name)
    
    return processed_names

bucket_name = 'aquilabeezacr'
folder_name = 'nomura/'
article_names = get_processed_article_names(bucket_name, folder_name)
print(article_names)

def check_article_processed(article_name, article_url):
    # Implement your logic to check if the article has been processed
    pass

def mark_article_processed(article_name, article_url):
    # Implement your logic to mark the article as processed
    pass
